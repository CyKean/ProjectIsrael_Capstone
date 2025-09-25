import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api",
  // baseURL: "http://192.168.43.101:8000/api", 
  // baseURL: "http://10.216.83.101:8000/api", 
  // baseURL: "https://qualify-cloudy-rack-cho.trycloudflare.com/api",
  // baseURL: "https://project-israel-backend.onrender.com/api", 
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
