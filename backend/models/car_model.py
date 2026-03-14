from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Car(Base):
    __tablename__ = "cars"

    car_id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    car_model = Column(String(80), nullable=False)
    car_number = Column(String(20), unique=True, nullable=False, index=True)
    total_seats = Column(Integer, nullable=False)

    driver = relationship("User", back_populates="cars")
