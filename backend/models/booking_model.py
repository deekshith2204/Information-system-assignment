from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    booking_id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.trip_id"), nullable=False, index=True)
    passenger_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    seats_booked = Column(Integer, nullable=False)
    total_price = Column(Integer, nullable=False)
    booking_status = Column(String(30), nullable=False, default="confirmed")
    cancelled_at = Column(DateTime, nullable=True)
    cancel_reason = Column(String(255), nullable=True)

    trip = relationship("Trip", back_populates="bookings")
    passenger = relationship("User", back_populates="bookings")
