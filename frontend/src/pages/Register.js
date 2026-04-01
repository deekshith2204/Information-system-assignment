import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { registerUser } from "../services/api";

export default function Register() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: "", email: "", phone: "", password: "", role: "passenger" });
  const [message, setMessage] = useState("");

  const onSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await registerUser(form);
      localStorage.setItem("token", res.data.access_token);
      localStorage.setItem("role", res.data.user.role);
      localStorage.setItem("user", JSON.stringify(res.data.user));
      setMessage("Registration successful");
      navigate(res.data.user.role === "driver" ? "/create-trip" : "/search");
      window.location.reload();
    } catch (err) {
      setMessage(err?.response?.data?.detail || "Registration failed");
    }
  };

  return (
    <form className="card" onSubmit={onSubmit}>
      <h2>Register</h2>
      <input placeholder="Name" onChange={(e) => setForm({ ...form, name: e.target.value })} />
      <input placeholder="Email" type="email" onChange={(e) => setForm({ ...form, email: e.target.value })} />
      <input placeholder="Phone" onChange={(e) => setForm({ ...form, phone: e.target.value })} />
      <input placeholder="Password" type="password" onChange={(e) => setForm({ ...form, password: e.target.value })} />
      <select onChange={(e) => setForm({ ...form, role: e.target.value })}>
        <option value="passenger">Passenger</option>
        <option value="driver">Driver</option>
      </select>
      <button type="submit">Register</button>
      <p>{message}</p>
    </form>
  );
}
