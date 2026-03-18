from datetime import date, datetime
from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from models.booking_model import Booking
from models.trip_model import Trip
from models.user_model import User
from schemas.trip_schema import TripCreate, TripOut, TripCancelRequest
from services.cancellation_service import ensure_can_cancel
from utils.auth import get_current_user
from utils.email_service import send_email

router = APIRouter()


def _trip_start_label(trip: Trip) -> str:
    return f"{trip.date.isoformat()} {trip.time.strftime('%H:%M')}"


@router.post("", response_model=TripOut)
def create_trip(payload: TripCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "driver":
        raise HTTPException(status_code=403, detail="Only drivers can create trips")
    if payload.available_seats < 1 or payload.price_per_seat < 1:
        raise HTTPException(status_code=400, detail="Seats and price must be positive")

    trip = Trip(driver_id=current_user.user_id, trip_status="scheduled", **payload.model_dump())
    db.add(trip)
    db.commit()
    db.refresh(trip)
    return trip


@router.get("/search", response_model=List[TripOut])
def search_trips(
    source: str = Query(...),
    destination: str = Query(...),
    date_value: date = Query(..., alias="date"),
    db: Session = Depends(get_db),
):
    return (
        db.query(Trip)
        .filter(
            Trip.source == source,
            Trip.destination == destination,
            Trip.date == date_value,
            Trip.available_seats > 0,
            Trip.trip_status == "scheduled",
        )
        .order_by(Trip.time.asc())
        .all()
    )


@router.post("/{trip_id}/cancel")
def cancel_trip(
    trip_id: int,
    payload: TripCancelRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    trip = db.query(Trip).filter(Trip.trip_id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    if current_user.role not in {"driver", "admin"}:
        raise HTTPException(status_code=403, detail="Only driver or admin can cancel trip")

    if current_user.role == "driver" and trip.driver_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not your trip")

    if trip.trip_status != "scheduled":
        raise HTTPException(status_code=400, detail="Trip is already cancelled")

    ensure_can_cancel(trip.date, trip.time)

    trip.trip_status = "cancelled"
    trip.cancelled_at = datetime.now()
    trip.cancel_reason = payload.reason

    bookings = db.query(Booking).filter(Booking.trip_id == trip.trip_id, Booking.booking_status == "confirmed").all()
    for booking in bookings:
        booking.booking_status = "cancelled_by_driver"
        booking.cancelled_at = datetime.now()
        booking.cancel_reason = payload.reason or "Trip cancelled by driver"

    db.commit()

    passenger_ids = {booking.passenger_id for booking in bookings}
    if passenger_ids:
        passengers = db.query(User).filter(User.user_id.in_(passenger_ids)).all()
        for passenger in passengers:
            if not passenger.email:
                continue
            subject = f"Your trip #{trip.trip_id} was cancelled"
            body = (
                f"Hello {passenger.name},\n\n"
                f"Your booked trip was cancelled by the driver/admin.\n"
                f"Route: {trip.source} -> {trip.destination}\n"
                f"Trip Start: {_trip_start_label(trip)}\n"
                f"Reason: {payload.reason or 'Not provided'}\n"
            )
            background_tasks.add_task(send_email, passenger.email, subject, body)

    return {"message": "Trip cancelled successfully"}
