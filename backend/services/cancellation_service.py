from datetime import datetime, timedelta

from fastapi import HTTPException


def ensure_can_cancel(trip_date, trip_time) -> None:
    departure = datetime.combine(trip_date, trip_time)
    deadline = departure - timedelta(hours=3)
    now = datetime.now()

    if now > deadline:
        raise HTTPException(
            status_code=400,
            detail="Cancellation is allowed only up to 3 hours before trip start",
        )
