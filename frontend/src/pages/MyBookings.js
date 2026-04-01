import React, { useEffect, useState } from "react";
import { cancelBooking, myBookings } from "../services/api";

export default function MyBookings() {
  const [data, setData] = useState([]);
  const [message, setMessage] = useState("");
  const [reasonById, setReasonById] = useState({});

  const load = async () => {
    try {
      const res = await myBookings();
      setData(res.data);
    } catch (err) {
      setMessage(err?.response?.data?.detail || "Failed to load bookings");
    }
  };

  useEffect(() => {
    load();
  }, []);

  const onCancelBooking = async (bookingId) => {
    try {
      await cancelBooking(bookingId, reasonById[bookingId] || null);
      setMessage("Booking cancelled successfully");
      await load();
    } catch (err) {
      setMessage(err?.response?.data?.detail || "Failed to cancel booking");
    }
  };

  return (
    <div>
      <h2>My Bookings</h2>
      <p>{message}</p>
      {data.map((b) => (
        <div className="card" key={b.booking_id}>
          <p>Booking #{b.booking_id}</p>
          <p>Trip ID: {b.trip_id}</p>
          <p>Seats: {b.seats_booked}</p>
          <p>Total: Rs. {b.total_price}</p>
          <p>Status: {b.booking_status}</p>
          {b.cancel_reason ? <p>Cancel reason: {b.cancel_reason}</p> : null}
          {b.booking_status === "confirmed" ? (
            <>
              <input
                placeholder="Cancel reason (optional)"
                value={reasonById[b.booking_id] || ""}
                onChange={(e) => setReasonById({ ...reasonById, [b.booking_id]: e.target.value })}
              />
              <button onClick={() => onCancelBooking(b.booking_id)}>Cancel Booking</button>
              <small>Allowed only before 3 hours of trip start.</small>
            </>
          ) : null}
        </div>
      ))}
    </div>
  );
}
