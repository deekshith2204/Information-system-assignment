-- Babla Cars relational schema

CREATE TABLE IF NOT EXISTS users (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(120) NOT NULL UNIQUE,
  phone VARCHAR(20) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  role VARCHAR(20) NOT NULL CHECK (role IN ('driver', 'passenger', 'admin'))
);

CREATE TABLE IF NOT EXISTS cars (
  car_id INTEGER PRIMARY KEY AUTOINCREMENT,
  driver_id INTEGER NOT NULL,
  car_model VARCHAR(80) NOT NULL,
  car_number VARCHAR(20) NOT NULL UNIQUE,
  total_seats INTEGER NOT NULL CHECK (total_seats > 0),
  FOREIGN KEY (driver_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS trips (
  trip_id INTEGER PRIMARY KEY AUTOINCREMENT,
  driver_id INTEGER NOT NULL,
  source VARCHAR(100) NOT NULL,
  destination VARCHAR(100) NOT NULL,
  date DATE NOT NULL,
  time TIME NOT NULL,
  price_per_seat INTEGER NOT NULL CHECK (price_per_seat > 0),
  available_seats INTEGER NOT NULL CHECK (available_seats >= 0),
  trip_status VARCHAR(30) NOT NULL DEFAULT 'scheduled',
  cancelled_at DATETIME,
  cancel_reason VARCHAR(255),
  FOREIGN KEY (driver_id) REFERENCES users(user_id)
);

CREATE INDEX IF NOT EXISTS idx_trips_search ON trips(source, destination, date);

CREATE TABLE IF NOT EXISTS bookings (
  booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
  trip_id INTEGER NOT NULL,
  passenger_id INTEGER NOT NULL,
  seats_booked INTEGER NOT NULL CHECK (seats_booked > 0),
  total_price INTEGER NOT NULL CHECK (total_price >= 0),
  booking_status VARCHAR(30) NOT NULL DEFAULT 'confirmed',
  cancelled_at DATETIME,
  cancel_reason VARCHAR(255),
  FOREIGN KEY (trip_id) REFERENCES trips(trip_id),
  FOREIGN KEY (passenger_id) REFERENCES users(user_id)
);
