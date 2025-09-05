import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import api from "../api"; // centralized axios instance

// ✅ Async thunk to fetch services from backend
export const fetchServices = createAsyncThunk(
  "services/fetchServices",
  async () => {
    const res = await api.get("/services/services/"); // backend endpoint
    return res.data; // expected format: [{id, nameKey, descKey, icon, category}, ...]
  }
);

const initialState = {
  categories: ["All", "Clothes", "Home", "Special"],
  activeCategory: "All",
  services: [
    { id: 1, nameKey: "steam.name", descKey: "steam.desc", icon: "🧺", category: "Clothes" },
    { id: 2, nameKey: "dry.name", descKey: "dry.desc", icon: "👔", category: "Clothes" },
    { id: 3, nameKey: "bed.name", descKey: "bed.desc", icon: "🛏️", category: "Home" },
    { id: 4, nameKey: "carpet.name", descKey: "carpet.desc", icon: "🪄", category: "Home" },
    { id: 5, nameKey: "curtain.name", descKey: "curtain.desc", icon: "🪟", category: "Home" },
    { id: 6, nameKey: "shoe.name", descKey: "shoe.desc", icon: "👟", category: "Special" },
    { id: 7, nameKey: "bag.name", descKey: "bag.desc", icon: "👜", category: "Special" },
    { id: 8, nameKey: "couture.name", descKey: "couture.desc", icon: "👗", category: "Special" },
    { id: 9, nameKey: "leather.name", descKey: "leather.desc", icon: "🧥", category: "Special" },
  ],
  status: "idle", // idle | loading | failed
};

const servicesSlice = createSlice({
  name: "services",
  initialState,
  reducers: {
    setCategory: (state, action) => {
      state.activeCategory = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchServices.pending, (state) => {
        state.status = "loading";
      })
      .addCase(fetchServices.fulfilled, (state, action) => {
        state.status = "idle";
        state.services = action.payload;
      })
      .addCase(fetchServices.rejected, (state) => {
        state.status = "failed";
      });
  },
});

// Actions
export const { setCategory } = servicesSlice.actions;

// Selectors
export const selectServices = (state) => state.services.services;
export const selectCategories = (state) => state.services.categories;
export const selectActiveCategory = (state) => state.services.activeCategory;
export const selectFilteredServices = (state) => {
  if (state.services.activeCategory === "All") return state.services.services;
  return state.services.services.filter(
    (s) => s.category === state.services.activeCategory
  );
};
export const selectServicesStatus = (state) => state.services.status;

export default servicesSlice.reducer;
