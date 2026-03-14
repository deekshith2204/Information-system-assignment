from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./babla_cars.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def _column_exists(connection, table_name: str, column_name: str) -> bool:
    rows = connection.execute(text(f"PRAGMA table_info({table_name})")).fetchall()
    return any(row[1] == column_name for row in rows)


def run_startup_migrations() -> None:
    # Lightweight SQLite migrations for new cancellation fields.
    with engine.begin() as connection:
        has_trips = connection.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name='trips'")
        ).fetchone()
        if has_trips:
            if not _column_exists(connection, "trips", "trip_status"):
                connection.execute(
                    text("ALTER TABLE trips ADD COLUMN trip_status VARCHAR(30) NOT NULL DEFAULT 'scheduled'")
                )
            if not _column_exists(connection, "trips", "cancelled_at"):
                connection.execute(text("ALTER TABLE trips ADD COLUMN cancelled_at DATETIME"))
            if not _column_exists(connection, "trips", "cancel_reason"):
                connection.execute(text("ALTER TABLE trips ADD COLUMN cancel_reason VARCHAR(255)"))

        has_bookings = connection.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name='bookings'")
        ).fetchone()
        if has_bookings:
            if not _column_exists(connection, "bookings", "cancelled_at"):
                connection.execute(text("ALTER TABLE bookings ADD COLUMN cancelled_at DATETIME"))
            if not _column_exists(connection, "bookings", "cancel_reason"):
                connection.execute(text("ALTER TABLE bookings ADD COLUMN cancel_reason VARCHAR(255)"))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
