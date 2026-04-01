import React, { useState } from "react";
import TripCard from "../components/TripCard";
import BookingForm from "../components/BookingForm";
import { createBooking, searchTrips } from "../services/api";

export default function SearchTrips() {
  const [query, setQuery] = useState({ source: "Nizamabad", destination: "Hyderabad", date: "" });
  const [trips, setTrips] = useState([]);
  const [selectedTrip, setSelectedTrip] = useState(null);
  const [message, setMessage] = useState("");

  const onSearch = async (e) => {
    e.preventDefault();
    try {
      const res = await searchTrips(query);
      setTrips(res.data);
      setMessage(`Found ${res.data.length} trips`);
    } catch (err) {
      setMessage(err?.response?.data?.detail || "Search failed");
    }
  };

  const openBooking = (trip) => {
    const token = localStorage.getItem("token");
    const role = localStorage.getItem("role");
    if (!token) {
      setMessage("Please login first to book seats.");
      return;
    }
    if (role !== "passenger") {
      setMessage("Only passenger accounts can book seats. Please switch account.");
      return;
    }
    setSelectedTrip(trip);
  };

  const onBook = async (tripId, seats) => {
    try {
      await createBooking({ trip_id: tripId, seats_booked: seats });
      setMessage("Booking successful");
      setSelectedTrip(null);
    } catch (err) {
      if (err?.response?.status === 403) {
        setMessage("Booking is allowed only for passenger accounts.");
        return;
      }
      setMessage(err?.response?.data?.detail || "Booking failed");
    }
  };

  return (
    <div>
      <form className="card" onSubmit={onSearch}>
        <h2>Search Trips</h2>
        <input placeholder="Source" value={query.source} onChange={(e) => setQuery({ ...query, source: e.target.value })} />
        <input placeholder="Destination" value={query.destination} onChange={(e) => setQuery({ ...query, destination: e.target.value })} />
        <input type="date" value={query.date} onChange={(e) => setQuery({ ...query, date: e.target.value })} />
        <button type="submit">Search</button>
      </form>
      <p>{message}</p>
      {trips.map((trip) => (
        <TripCard key={trip.trip_id} trip={trip} onBook={openBooking} />
      ))}
      {selectedTrip ? <BookingForm trip={selectedTrip} onSubmit={onBook} /> : null}
    </div>
  );
}
