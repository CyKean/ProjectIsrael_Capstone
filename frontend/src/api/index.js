import axios from "axios";

const api = axios.create({
  // baseURL: "http://localhost:8000/api", // FastAPI backend URL
  baseURL: "http://192.168.43.128:8000/api", // FastAPI backend URL
  // baseURL: "https://qualify-cloudy-rack-cho.trycloudflare.com/api", // FastAPI backend URL
  // baseURL: "https://project-israel-backend.onrender.com/api", // FastAPI backend URL
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
