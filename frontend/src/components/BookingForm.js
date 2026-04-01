import React, { useState } from "react";

export default function BookingForm({ trip, onSubmit }) {
  const [seats, setSeats] = useState(1);

  return (
    <div className="card">
      <h4>Book Trip #{trip.trip_id}</h4>
      <input
        type="number"
        min="1"
        value={seats}
        onChange={(e) => setSeats(Number(e.target.value))}
      />
      <button onClick={() => onSubmit(trip.trip_id, seats)}>Confirm Booking</button>
    </div>
  );
}
