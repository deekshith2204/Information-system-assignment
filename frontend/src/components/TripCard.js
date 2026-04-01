import React from "react";

export default function TripCard({ trip, onBook }) {
  return (
    <div className="card">
      <h3>{trip.source} -> {trip.destination}</h3>
      <p>Date: {trip.date}</p>
      <p>Time: {trip.time}</p>
      <p>Price per seat: Rs. {trip.price_per_seat}</p>
      <p>Available seats: {trip.available_seats}</p>
      {onBook ? <button onClick={() => onBook(trip)}>Book</button> : null}
    </div>
  );
}
