from datetime import datetime

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from models.booking_model import Booking
from models.trip_model import Trip
from models.user_model import User
from schemas.booking_schema import BookingCreate, BookingOut, BookingCancelRequest
from services.booking_service import create_booking_atomic
from services.cancellation_service import ensure_can_cancel
from utils.auth import get_current_user
from utils.email_service import send_email

router = APIRouter()


def _trip_start_label(trip: Trip) -> str:
    return f"{trip.date.isoformat()} {trip.time.strftime('%H:%M')}"


@router.post("", response_model=BookingOut)
def create_booking(
    payload: BookingCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "passenger":
        raise HTTPException(status_code=403, detail="Only passengers can book rides")
    if payload.seats_booked < 1:
        raise HTTPException(status_code=400, detail="seats_booked must be at least 1")

    trip = db.query(Trip).filter(Trip.trip_id == payload.trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    if trip.trip_status != "scheduled":
        raise HTTPException(status_code=400, detail="This trip is not available for booking")

    booking = create_booking_atomic(db, trip, current_user.user_id, payload.seats_booked)

    driver = db.query(User).filter(User.user_id == trip.driver_id).first()
    if driver and driver.email:
        subject = f"New booking for Trip #{trip.trip_id}"
        body = (
            f"Hello {driver.name},\n\n"
            f"Passenger {current_user.name} ({current_user.email}) booked {booking.seats_booked} seat(s).\n"
            f"Route: {trip.source} -> {trip.destination}\n"
            f"Trip Start: {_trip_start_label(trip)}\n"
            f"Booking ID: {booking.booking_id}\n"
            f"Total Price: Rs. {booking.total_price}\n"
        )
        background_tasks.add_task(send_email, driver.email, subject, body)

    return booking


@router.get("/my", response_model=list[BookingOut])
def my_bookings(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "passenger":
        raise HTTPException(status_code=403, detail="Only passengers can view this endpoint")

    return db.query(Booking).filter(Booking.passenger_id == current_user.user_id).order_by(Booking.booking_id.desc()).all()


@router.get("/trip/{trip_id}", response_model=list[BookingOut])
def trip_bookings(trip_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    trip = db.query(Trip).filter(Trip.trip_id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    if current_user.role not in {"admin", "driver"}:
        raise HTTPException(status_code=403, detail="Not allowed")
    if current_user.role == "driver" and trip.driver_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not your trip")

    return db.query(Booking).filter(Booking.trip_id == trip_id).order_by(Booking.booking_id.desc()).all()


@router.post("/{booking_id}/cancel", response_model=BookingOut)
def cancel_booking(
    booking_id: int,
    payload: BookingCancelRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    trip = db.query(Trip).filter(Trip.trip_id == booking.trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    if current_user.role not in {"passenger", "admin"}:
        raise HTTPException(status_code=403, detail="Only passenger or admin can cancel booking")
    if current_user.role == "passenger" and booking.passenger_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not your booking")

    if booking.booking_status != "confirmed":
        raise HTTPException(status_code=400, detail="Booking is already cancelled")

    ensure_can_cancel(trip.date, trip.time)

    booking.booking_status = "cancelled_by_passenger"
    booking.cancelled_at = datetime.now()
    booking.cancel_reason = payload.reason

    if trip.trip_status == "scheduled":
        trip.available_seats += booking.seats_booked

    db.commit()
    db.refresh(booking)

    driver = db.query(User).filter(User.user_id == trip.driver_id).first()
    passenger = db.query(User).filter(User.user_id == booking.passenger_id).first()
    if driver and driver.email:
        actor_name = passenger.name if passenger else f"user#{booking.passenger_id}"
        subject = f"Booking cancelled for Trip #{trip.trip_id}"
        body = (
            f"Hello {driver.name},\n\n"
            f"Passenger {actor_name} cancelled booking #{booking.booking_id}.\n"
            f"Route: {trip.source} -> {trip.destination}\n"
            f"Trip Start: {_trip_start_label(trip)}\n"
            f"Seats Cancelled: {booking.seats_booked}\n"
            f"Reason: {payload.reason or 'Not provided'}\n"
        )
        background_tasks.add_task(send_email, driver.email, subject, body)

    return booking
