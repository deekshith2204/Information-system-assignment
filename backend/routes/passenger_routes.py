from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from models.booking_model import Booking
from models.user_model import User
from utils.auth import get_current_user

router = APIRouter()


@router.get("/bookings")
def booking_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "passenger":
        raise HTTPException(status_code=403, detail="Only passengers can view booking history")

    data = db.query(Booking).filter(Booking.passenger_id == current_user.user_id).all()
    return {"count": len(data), "items": data}
