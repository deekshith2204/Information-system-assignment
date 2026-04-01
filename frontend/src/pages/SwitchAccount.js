import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginUser } from "../services/api";

const DEMO_ACCOUNTS = [
  { label: "Login as Driver", email: "driver@babla.com", password: "Pass@123" },
  { label: "Login as Passenger", email: "rahul@babla.com", password: "Pass@123" },
  { label: "Login as Admin", email: "admin@babla.com", password: "Pass@123" },
];

export default function SwitchAccount() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "" });
  const [message, setMessage] = useState("");

  const clearSession = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    localStorage.removeItem("user");
  };

  const completeLogin = (res) => {
    localStorage.setItem("token", res.data.access_token);
    localStorage.setItem("role", res.data.user.role);
    localStorage.setItem("user", JSON.stringify(res.data.user));
    const next = res.data.user.role === "driver" ? "/create-trip" : "/search";
    navigate(next);
    window.location.reload();
  };

  const loginWith = async (email, password) => {
    try {
      clearSession();
      const res = await loginUser({ email, password });
      completeLogin(res);
    } catch (err) {
      setMessage(err?.response?.data?.detail || "Login failed");
    }
  };

  const onCustomLogin = async (e) => {
    e.preventDefault();
    await loginWith(form.email, form.password);
  };

  return (
    <div className="card">
      <h2>Switch Account</h2>
      <p>Choose a demo account or login with custom credentials.</p>

      <div className="switch-grid">
        {DEMO_ACCOUNTS.map((acct) => (
          <button key={acct.label} type="button" onClick={() => loginWith(acct.email, acct.password)}>
            {acct.label}
          </button>
        ))}
      </div>

      <form onSubmit={onCustomLogin} className="switch-form">
        <input
          placeholder="Email"
          type="email"
          value={form.email}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
        />
        <input
          placeholder="Password"
          type="password"
          value={form.password}
          onChange={(e) => setForm({ ...form, password: e.target.value })}
        />
        <button type="submit">Login with custom account</button>
      </form>

      {message ? <p>{message}</p> : null}
    </div>
  );
}
