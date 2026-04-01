import React, { useState } from "react";
import { createTrip } from "../services/api";

export default function CreateTrip() {
  const [form, setForm] = useState({
    source: "Nizamabad",
    destination: "Hyderabad",
    date: "",
    time: "12:00:00",
    price_per_seat: 500,
    available_seats: 5,
  });
  const [message, setMessage] = useState("");

  const onSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");
    const role = localStorage.getItem("role");

    if (!token) {
      setMessage("Please login first.");
      return;
    }

    if (role !== "driver") {
      setMessage("Only driver accounts can create trips. Please switch account.");
      return;
    }

    try {
      await createTrip({ ...form, price_per_seat: Number(form.price_per_seat), available_seats: Number(form.available_seats) });
      setMessage("Trip created");
    } catch (err) {
      if (err?.response?.status === 403) {
        setMessage("Only driver accounts can create trips.");
        return;
      }
      setMessage(err?.response?.data?.detail || "Trip creation failed");
    }
  };

  return (
    <form className="card" onSubmit={onSubmit}>
      <h2>Create Trip</h2>
      <input value={form.source} onChange={(e) => setForm({ ...form, source: e.target.value })} />
      <input value={form.destination} onChange={(e) => setForm({ ...form, destination: e.target.value })} />
      <input type="date" value={form.date} onChange={(e) => setForm({ ...form, date: e.target.value })} />
      <input type="time" step="1" value={form.time} onChange={(e) => setForm({ ...form, time: e.target.value })} />
      <input type="number" value={form.price_per_seat} onChange={(e) => setForm({ ...form, price_per_seat: e.target.value })} />
      <input type="number" value={form.available_seats} onChange={(e) => setForm({ ...form, available_seats: e.target.value })} />
      <button type="submit">Create</button>
      <p>{message}</p>
    </form>
  );
}
