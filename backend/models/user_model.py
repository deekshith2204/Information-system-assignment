from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False, index=True)
    phone = Column(String(20), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum("driver", "passenger", "admin", name="user_roles"), nullable=False)

    cars = relationship("Car", back_populates="driver", cascade="all, delete-orphan")
    trips = relationship("Trip", back_populates="driver", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="passenger")
