import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginUser } from "../services/api";

export default function Login() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "" });
  const [message, setMessage] = useState("");

  const onSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await loginUser(form);
      localStorage.setItem("token", res.data.access_token);
      localStorage.setItem("role", res.data.user.role);
      localStorage.setItem("user", JSON.stringify(res.data.user));
      setMessage("Login successful");
      navigate(res.data.user.role === "driver" ? "/create-trip" : "/search");
      window.location.reload();
    } catch (err) {
      setMessage(err?.response?.data?.detail || "Login failed");
    }
  };

  return (
    <form className="card" onSubmit={onSubmit}>
      <h2>Login</h2>
      <input placeholder="Email" type="email" onChange={(e) => setForm({ ...form, email: e.target.value })} />
      <input placeholder="Password" type="password" onChange={(e) => setForm({ ...form, password: e.target.value })} />
      <button type="submit">Login</button>
      <p>{message}</p>
    </form>
  );
}
