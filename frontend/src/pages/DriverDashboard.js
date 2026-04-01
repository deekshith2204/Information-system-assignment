import React, { useState } from "react";
import { cancelTrip, tripBookings } from "../services/api";

export default function DriverDashboard() {
  const [tripId, setTripId] = useState("");
  const [bookings, setBookings] = useState([]);
  const [message, setMessage] = useState("");
  const [cancelReason, setCancelReason] = useState("");

  const loadBookings = async () => {
    try {
      const res = await tripBookings(tripId);
      setBookings(res.data);
      setMessage("");
    } catch (err) {
      setMessage(err?.response?.data?.detail || "Failed to load trip bookings");
    }
  };

  const onCancelTrip = async () => {
    try {
      await cancelTrip(tripId, cancelReason || null);
      setMessage("Trip cancelled successfully");
      setBookings([]);
    } catch (err) {
      setMessage(err?.response?.data?.detail || "Failed to cancel trip");
    }
  };

  return (
    <div>
      <div className="card">
        <h2>Driver Dashboard</h2>
        <input placeholder="Trip ID" value={tripId} onChange={(e) => setTripId(e.target.value)} />
        <button onClick={loadBookings}>Load Bookings</button>
        <input
          placeholder="Trip cancel reason (optional)"
          value={cancelReason}
          onChange={(e) => setCancelReason(e.target.value)}
        />
        <button onClick={onCancelTrip}>Cancel Trip</button>
        <small>Trip cancellation is allowed only before 3 hours of trip start.</small>
      </div>
      <p>{message}</p>
      {bookings.map((b) => (
        <div key={b.booking_id} className="card">
          <p>Booking #{b.booking_id}</p>
          <p>Passenger ID: {b.passenger_id}</p>
          <p>Seats: {b.seats_booked}</p>
          <p>Status: {b.booking_status}</p>
        </div>
      ))}
    </div>
  );
}
