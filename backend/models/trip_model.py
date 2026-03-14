from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, DateTime
from sqlalchemy.orm import relationship

from app.database import Base


class Trip(Base):
    __tablename__ = "trips"

    trip_id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    source = Column(String(100), nullable=False, index=True)
    destination = Column(String(100), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    time = Column(Time, nullable=False)
    price_per_seat = Column(Integer, nullable=False)
    available_seats = Column(Integer, nullable=False)
    trip_status = Column(String(30), nullable=False, default="scheduled")
    cancelled_at = Column(DateTime, nullable=True)
    cancel_reason = Column(String(255), nullable=True)

    driver = relationship("User", back_populates="trips")
    bookings = relationship("Booking", back_populates="trip", cascade="all, delete-orphan")
