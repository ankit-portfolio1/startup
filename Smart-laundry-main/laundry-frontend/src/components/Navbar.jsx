"use client";
import React, { useState, useEffect } from "react";
import { Menu, X, Sun, Moon, Globe, ShoppingCart } from "lucide-react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import { toggleTheme } from "../slices/themeSlice";
import { setLanguage } from "../slices/languageSlice";
import { setCart } from "../slices/cartSlice";
import { logout } from "../slices/authSlice";
import useT from "../hooks/useT";
import api from "../api";

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const t = useT();

  // Redux states
  const cartCount = useSelector((state) => state.cart.totalQty || 0);
  const theme = useSelector((state) => state.theme.mode || "light");
  const language = useSelector((state) => state.language.language || "en");
  const user = useSelector((state) => state.auth.user);

  // Close mobile menu on route change
  useEffect(() => setIsOpen(false), [location]);

  // Fetch cart from backend
  useEffect(() => {
    async function fetchCart() {
      try {
        const res = await api.get("/cart"); // ✅ backend ready
        dispatch(setCart(res.data));
      } catch (err) {
        console.error("Failed to fetch cart:", err);
      }
    }
    if (user) fetchCart();
  }, [dispatch, user]);

  // Languages
  const languages = [
    { code: "en", label: "EN" },
    { code: "hi", label: "हिंदी" },
    { code: "mr", label: "मराठी" },
  ];

  const nextLanguage = () => {
    const currentIndex = languages.findIndex((l) => l.code === language);
    const nextIndex = (currentIndex + 1) % languages.length;
    dispatch(setLanguage(languages[nextIndex].code));
  };

  // Book Now Button Handler
  const handleBookNow = () => {
    if (!user) {
      // Agar login nahi hai to login page bhejke services par redirect
      navigate("/login", { state: { from: "/services" } });
    } else {
      // Agar login hai to sidha services page
      navigate("/services");
    }
  };

  return (
    <nav
      className={`fixed top-0 left-0 w-full z-50 backdrop-blur-xl shadow-lg transition-colors duration-500 ${
        theme === "dark" ? "bg-gray-900/80" : "bg-white/80"
      }`}
    >
      <div className="max-w-7xl mx-auto flex justify-between items-center px-6 py-4">
        {/* Logo */}
        <Link
          to="/"
          className="flex items-center space-x-3 group transition-transform hover:scale-105"
        >
          <img
            src="https://cdn-icons-png.flaticon.com/512/679/679922.png"
            alt="Laundry Logo"
            className="w-12 h-12 drop-shadow-md group-hover:rotate-12 transition-transform"
          />
          <div>
            <h1 className="text-2xl font-extrabold tracking-wide text-gray-900 dark:text-white">
              Smart Laundry
            </h1>
            <p className="text-sm text-indigo-600 dark:text-yellow-300 italic">
              {t("navbar.tagline")}
            </p>
          </div>
        </Link>

        {/* Desktop Menu */}
        <ul className="hidden md:flex space-x-10 text-lg font-semibold text-gray-800 dark:text-gray-200 mx-auto">
          {[
            { path: "/", label: t("navbar.home") },
            { path: "/services", label: t("navbar.services") },
            { path: "/aboutus", label: t("navbar.about") },
            { path: "/contact", label: t("navbar.contact") },
          ].map((item) => (
            <li
              key={item.path}
              className={`transition-colors hover:text-blue-500 ${
                location.pathname === item.path ||
                location.pathname.startsWith(item.path)
                  ? "underline decoration-2 decoration-blue-500"
                  : ""
              }`}
            >
              <Link to={item.path}>{item.label}</Link>
            </li>
          ))}
        </ul>

        {/* Desktop Controls */}
        <div className="hidden md:flex items-center space-x-4">
          {/* Cart */}
          <Link
            to="/cart"
            className="relative w-11 h-11 flex items-center justify-center rounded-full 
                       bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white 
                       shadow hover:scale-110 transition"
          >
            <ShoppingCart size={22} />
            {cartCount > 0 && (
              <span className="absolute -top-1 -right-1 bg-red-500 text-white 
                               text-xs font-bold w-5 h-5 flex items-center justify-center rounded-full">
                {cartCount}
              </span>
            )}
          </Link>

          {/* Book Now */}
          <button
            onClick={handleBookNow}
            className="bg-gradient-to-r from-yellow-400 to-yellow-300 text-black px-5 py-2 rounded-full font-medium shadow hover:scale-105 transition"
          >
            {t("navbar.book")}
          </button>

          {/* Auth */}
          {user ? (
            <button
              onClick={() => {
                dispatch(logout());
                navigate("/");
              }}
              className="bg-red-500 text-white px-4 py-2 rounded-full shadow hover:bg-red-400 transition"
            >
              Logout
            </button>
          ) : (
            <Link
              to="/login"
              className="bg-blue-500 text-white px-4 py-2 rounded-full shadow hover:bg-blue-400 transition"
            >
              Login
            </Link>
          )}

          {/* Dark Mode Toggle */}
          <button
            onClick={() => dispatch(toggleTheme())}
            className="w-11 h-11 flex items-center justify-center rounded-full 
                       bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-yellow-300 
                       shadow hover:scale-110 transition"
          >
            {theme === "dark" ? <Sun size={22} /> : <Moon size={22} />}
          </button>

          {/* Language Switcher */}
          <button
            onClick={nextLanguage}
            className="flex items-center gap-2 px-4 py-2 rounded-full border border-gray-300 
                       dark:border-gray-600 bg-gray-100 dark:bg-gray-800 
                       text-gray-900 dark:text-white font-semibold shadow hover:scale-105 transition"
            title="Switch Language"
          >
            <Globe size={18} />
            <span>{languages.find((l) => l.code === language)?.label}</span>
          </button>
        </div>
      </div>
    </nav>
  );
}
