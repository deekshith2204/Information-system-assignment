from datetime import date, time, datetime
from typing import Optional

from pydantic import BaseModel


class CarCreate(BaseModel):
    car_model: str
    car_number: str
    total_seats: int


class CarOut(BaseModel):
    car_id: int
    driver_id: int
    car_model: str
    car_number: str
    total_seats: int

    class Config:
        from_attributes = True


class TripCreate(BaseModel):
    source: str
    destination: str
    date: date
    time: time
    price_per_seat: int
    available_seats: int


class TripCancelRequest(BaseModel):
    reason: Optional[str] = None


class TripOut(BaseModel):
    trip_id: int
    driver_id: int
    source: str
    destination: str
    date: date
    time: time
    price_per_seat: int
    available_seats: int
    trip_status: str
    cancelled_at: Optional[datetime] = None
    cancel_reason: Optional[str] = None

    class Config:
        from_attributes = True
