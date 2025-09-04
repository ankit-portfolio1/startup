"use client";
import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { loginUser } from "../slices/authSlice";
import { useNavigate, useLocation } from "react-router-dom";
import { FcGoogle } from "react-icons/fc";
import api from "../api";
import { motion } from "framer-motion";
import toast, { Toaster } from "react-hot-toast";

export default function Login() {
  const [formData, setFormData] = useState({ email: "" });
  const [otpSent, setOtpSent] = useState(false);
  const [otp, setOtp] = useState("");
  const [loading, setLoading] = useState(false);
  const [timer, setTimer] = useState(0);

  const dispatch = useDispatch();
  const navigate = useNavigate();
  const location = useLocation();
  const { error } = useSelector((state) => state.auth);

  // Countdown timer for OTP resend
  useEffect(() => {
    let interval;
    if (timer > 0) {
      interval = setInterval(() => setTimer((prev) => prev - 1), 1000);
    }
    return () => clearInterval(interval);
  }, [timer]);

  const handleChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const sendOtp = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.post("/auth/send-otp", { email: formData.email });
      setOtpSent(true);
      setTimer(30);
      toast.success("OTP sent successfully!");
    } catch (err) {
      console.error("OTP error:", err);
      toast.error("Failed to send OTP. Try again!");
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await dispatch(loginUser({ ...formData, otp }));
      setLoading(false);
      if (!res.error) {
        const user = res.payload.user;
        toast.success("Login successful!");
        if (user.role === "admin") {
          navigate("/admin", { replace: true });
        } else {
          const redirectTo = location.state?.from || "/services";
          navigate(redirectTo, { replace: true });
        }
      } else {
        toast.error("Invalid OTP. Try again.");
      }
    } catch (err) {
      setLoading(false);
      toast.error("Login error. Try again.");
    }
  };

  const handleGoogleLogin = () => {
    window.location.href = "http://localhost:5000/api/auth/google";
  };

  const handleBackToEmail = () => {
    setOtpSent(false);
    setOtp("");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-blue-100 dark:from-gray-900 dark:to-gray-850 px-4 transition-colors duration-500">
      <Toaster position="top-right" />
      <motion.div
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="bg-white dark:bg-gray-900 shadow-lg rounded-3xl w-full max-w-md p-8 sm:p-10 md:p-12 overflow-hidden"
      >
        {/* Logo */}
        <div className="flex flex-col items-center mb-8">
          <img
            src="https://cdn-icons-png.flaticon.com/512/679/679922.png"
            alt="Laundry Logo"
            className="w-16 h-16 mb-2 drop-shadow-sm"
          />
          <h1 className="text-3xl sm:text-4xl font-extrabold text-gray-900 dark:text-gray-100 text-center">
            Welcome Back 👕
          </h1>
          <p className="text-gray-600 dark:text-gray-400 text-sm sm:text-base mt-1 text-center">
            Login to <span className="text-blue-500 font-semibold">Smart Laundry</span>
          </p>
        </div>

        {/* Form */}
        {!otpSent ? (
          <form onSubmit={sendOtp} className="space-y-5">
            <input
              type="text"
              name="email"
              placeholder="Email or Phone"
              onChange={handleChange}
              className="w-full p-4 border border-gray-200 dark:border-gray-700 rounded-2xl bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-300 dark:focus:ring-blue-500 transition"
              required
            />
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-500 hover:bg-blue-600 dark:hover:bg-blue-700 text-white font-semibold py-3 rounded-2xl shadow-md transition-all duration-300"
            >
              {loading ? "Sending OTP..." : "Send OTP"}
            </button>
          </form>
        ) : (
          <form onSubmit={handleLogin} className="space-y-5">
            <input
              type="text"
              value={otp}
              onChange={(e) => setOtp(e.target.value)}
              placeholder="Enter OTP"
              className="w-full p-4 border border-gray-200 dark:border-gray-700 rounded-2xl bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-300 dark:focus:ring-green-500 transition"
              required
            />
            <div className="flex justify-between items-center text-sm text-gray-500 dark:text-gray-400">
              <button
                type="button"
                onClick={handleBackToEmail}
                className="underline hover:text-gray-700 dark:hover:text-gray-200 transition"
              >
                Change Email
              </button>
              <span>
                {timer > 0
                  ? `Resend in ${timer}s`
                  : (
                    <button
                      type="button"
                      onClick={sendOtp}
                      className="underline hover:text-gray-700 dark:hover:text-gray-200 transition"
                    >
                      Resend OTP
                    </button>
                  )}
              </span>
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-green-500 hover:bg-green-600 dark:hover:bg-green-700 text-white font-semibold py-3 rounded-2xl shadow-md transition-all duration-300"
            >
              {loading ? "Verifying..." : "Verify & Login"}
            </button>
          </form>
        )}

        {/* Divider */}
        <div className="flex items-center my-6">
          <div className="flex-grow h-px bg-gray-300 dark:bg-gray-700"></div>
          <span className="px-3 text-gray-500 text-sm">OR</span>
          <div className="flex-grow h-px bg-gray-300 dark:bg-gray-700"></div>
        </div>

        {/* Google Login */}
        <button
          onClick={handleGoogleLogin}
          className="w-full flex items-center justify-center gap-2 border border-gray-300 dark:border-gray-700 py-3 rounded-2xl hover:bg-gray-50 dark:hover:bg-gray-800 transition font-medium shadow-sm"
        >
          <FcGoogle size={22} /> Continue with Google
        </button>

        <p className="text-gray-400 text-xs mt-4 text-center sm:text-sm">
          Use your registered email or phone to login. OTP will be sent immediately.
        </p>
      </motion.div>
    </div>
  );
}
