import React from "react";
import { Link, useNavigate } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();
  let user = null;

  try {
    user = JSON.parse(localStorage.getItem("user") || "null");
  } catch {
    user = null;
  }

  const onLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    localStorage.removeItem("user");
    navigate("/switch-account");
    window.location.reload();
  };

  return (
    <nav className="nav">
      <h1>Babla Cars</h1>
      <div className="nav-links">
        <Link to="/search">Search</Link>
        <Link to="/create-trip">Create Trip</Link>
        <Link to="/my-bookings">My Bookings</Link>
        <Link to="/driver">Driver Dashboard</Link>
        <Link to="/register">Register</Link>
        <Link to="/switch-account">Switch Account</Link>
        {!user ? <Link to="/login">Login</Link> : null}
        {user ? (
          <>
            <span className="user-chip">{user.name} ({user.role})</span>
            <button type="button" className="link-button" onClick={onLogout}>Logout</button>
          </>
        ) : null}
      </div>
    </nav>
  );
}
