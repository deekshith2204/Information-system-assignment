from app.database import Base

# Import models to ensure metadata registration
from models.user_model import User  # noqa: F401
from models.car_model import Car  # noqa: F401
from models.trip_model import Trip  # noqa: F401
from models.booking_model import Booking  # noqa: F401
