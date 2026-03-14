from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine, run_startup_migrations
from routes import auth_routes, driver_routes, trip_routes, booking_routes, passenger_routes

load_dotenv()

run_startup_migrations()
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Babla Cars API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(driver_routes.router, prefix="/driver", tags=["driver"])
app.include_router(trip_routes.router, prefix="/trips", tags=["trips"])
app.include_router(booking_routes.router, prefix="/bookings", tags=["bookings"])
app.include_router(passenger_routes.router, prefix="/passenger", tags=["passenger"])


@app.get("/")
def health_check():
    return {"status": "ok", "service": "Babla Cars API"}
