from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BookingCreate(BaseModel):
    trip_id: int
    seats_booked: int


class BookingCancelRequest(BaseModel):
    reason: Optional[str] = None


class BookingOut(BaseModel):
    booking_id: int
    trip_id: int
    passenger_id: int
    seats_booked: int
    total_price: int
    booking_status: str
    cancelled_at: Optional[datetime] = None
    cancel_reason: Optional[str] = None

    class Config:
        from_attributes = True
