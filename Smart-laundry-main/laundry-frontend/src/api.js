// src/api.js
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:5000/api",
  headers: { "Content-Type": "application/json" },
});

export const sendContactForm = async (formData) => {
  const res = await api.post("/contact", formData);
  return res.data;
};

export default api;
