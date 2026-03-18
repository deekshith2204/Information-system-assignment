from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from models.user_model import User
from schemas.user_schema import UserRegister, UserLogin, AuthResponse
from utils.auth import hash_password, verify_password, create_access_token

router = APIRouter()


@router.post("/register", response_model=AuthResponse)
def register_user(payload: UserRegister, db: Session = Depends(get_db)):
    if payload.role not in {"driver", "passenger", "admin"}:
        raise HTTPException(status_code=400, detail="Invalid role")

    existing = db.query(User).filter((User.email == payload.email) | (User.phone == payload.phone)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email or phone already exists")

    user = User(
        name=payload.name,
        email=payload.email,
        phone=payload.phone,
        password=hash_password(payload.password),
        role=payload.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": str(user.user_id), "role": user.role})
    return {"access_token": token, "user": user}


@router.post("/login", response_model=AuthResponse)
def login_user(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.user_id), "role": user.role})
    return {"access_token": token, "user": user}
