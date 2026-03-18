from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from models.car_model import Car
from models.user_model import User
from schemas.trip_schema import CarCreate, CarOut
from utils.auth import get_current_user

router = APIRouter()


@router.post("/cars", response_model=CarOut)
def add_car(payload: CarCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "driver":
        raise HTTPException(status_code=403, detail="Only drivers can add cars")

    if payload.total_seats < 1:
        raise HTTPException(status_code=400, detail="total_seats must be at least 1")

    existing = db.query(Car).filter(Car.car_number == payload.car_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Car number already exists")

    car = Car(driver_id=current_user.user_id, **payload.model_dump())
    db.add(car)
    db.commit()
    db.refresh(car)
    return car
