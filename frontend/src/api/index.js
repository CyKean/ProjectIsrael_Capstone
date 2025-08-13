import axios from "axios";

const api = axios.create({
  // baseURL: "https://localhost:8000/api", // FastAPI backend URL
  baseURL: "https://project-israel-backend.onrender.com/api", // FastAPI backend URL
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
