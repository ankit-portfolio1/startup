// src/api.js
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api",
  headers: { "Content-Type": "application/json" },
});

// Attach JWT token from localStorage if present
api.interceptors.request.use((config) => {
  try {
    const authRaw = localStorage.getItem("auth");
    if (authRaw) {
      const { token } = JSON.parse(authRaw) || {};
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
  } catch {}
  return config;
});

export const sendContactForm = async (formData) => {
  const res = await api.post("/core/contact/", formData);
  return res.data;
};

export default api;
