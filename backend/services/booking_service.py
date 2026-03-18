from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from models.booking_model import Booking
from models.trip_model import Trip


def create_booking_atomic(db: Session, trip: Trip, passenger_id: int, seats_booked: int) -> Booking:
    total_price = trip.price_per_seat * seats_booked

    # Atomic seat update to prevent overbooking under concurrent requests.
    update_stmt = text(
        """
        UPDATE trips
        SET available_seats = available_seats - :seats
        WHERE trip_id = :trip_id
          AND available_seats >= :seats
        """
    )

    result = db.execute(update_stmt, {"seats": seats_booked, "trip_id": trip.trip_id})
    if result.rowcount != 1:
        db.rollback()
        raise HTTPException(status_code=400, detail="Not enough seats")

    booking = Booking(
        trip_id=trip.trip_id,
        passenger_id=passenger_id,
        seats_booked=seats_booked,
        total_price=total_price,
        booking_status="confirmed",
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking
