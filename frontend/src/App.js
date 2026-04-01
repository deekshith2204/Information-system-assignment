import React from "react";
import { Link, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import Login from "./pages/Login";
import Register from "./pages/Register";
import SearchTrips from "./pages/SearchTrips";
import CreateTrip from "./pages/CreateTrip";
import MyBookings from "./pages/MyBookings";
import DriverDashboard from "./pages/DriverDashboard";
import SwitchAccount from "./pages/SwitchAccount";

export default function App() {
  return (
    <div className="app-shell">
      <Navbar />
      <div className="page-wrap">
        <Routes>
          <Route path="/" element={<SearchTrips />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/switch-account" element={<SwitchAccount />} />
          <Route path="/search" element={<SearchTrips />} />
          <Route path="/create-trip" element={<CreateTrip />} />
          <Route path="/my-bookings" element={<MyBookings />} />
          <Route path="/driver" element={<DriverDashboard />} />
        </Routes>
      </div>
      <footer className="footer">
        <Link to="/search">Find rides</Link>
      </footer>
    </div>
  );
}
