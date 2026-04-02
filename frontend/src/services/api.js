import axios from "axios";

const API = axios.create({ baseURL: "http://127.0.0.1:8000" });

API.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export const registerUser = (payload) => API.post("/auth/register", payload);
export const loginUser = (payload) => API.post("/auth/login", payload);
export const createTrip = (payload) => API.post("/trips", payload);
export const searchTrips = (params) => API.get("/trips/search", { params });
export const cancelTrip = (tripId, reason) => API.post(`/trips/${tripId}/cancel`, { reason });

export const createBooking = (payload) => API.post("/bookings", payload);
export const myBookings = () => API.get("/bookings/my");
export const tripBookings = (tripId) => API.get(`/bookings/trip/${tripId}`);
export const cancelBooking = (bookingId, reason) => API.post(`/bookings/${bookingId}/cancel`, { reason });

export default API;
