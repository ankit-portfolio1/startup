import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import api from "../api"; // centralized axios instance

// Initial state
const initialState = {
  categories: ["All"], // default
  status: "idle",      // "idle" | "loading" | "failed"
};

// ✅ Async thunk to fetch categories from backend
export const fetchCategories = createAsyncThunk(
  "categories/fetchCategories",
  async () => {
    const res = await api.get("/categories"); // backend endpoint
    return res.data; // assume array of categories ["All", "Laundry", ...]
  }
);

// Slice
const categoriesSlice = createSlice({
  name: "categories",
  initialState,
  reducers: {
    setCategories: (state, action) => {
      state.categories = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchCategories.pending, (state) => {
        state.status = "loading";
      })
      .addCase(fetchCategories.fulfilled, (state, action) => {
        state.status = "idle";
        state.categories = action.payload;
      })
      .addCase(fetchCategories.rejected, (state) => {
        state.status = "failed";
      });
  },
});

// Exports
export const { setCategories } = categoriesSlice.actions;
export const selectCategories = (state) => state.categories.categories;
export const selectCategoriesStatus = (state) => state.categories.status;
export default categoriesSlice.reducer;
