import axios from "axios";

const api = axios.create({
  baseURL: "https://project-israel-backend.onrender.com/api", // FastAPI backend URL
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
