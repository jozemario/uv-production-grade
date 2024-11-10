import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { User } from "../../types";

interface AuthState {
  token: string | null;
  user: User | null;
  isAuthenticated: boolean;
}

const initialState: AuthState = {
  token: localStorage.getItem("token"),
  user: localStorage.getItem("user")
    ? JSON.parse(localStorage.getItem("user") || "{}")
    : null,
  isAuthenticated: Boolean(localStorage.getItem("token")),
};

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    setCredentials: (
      state,
      action: PayloadAction<{ access_token: string; token_type: string }>
    ) => {
      state.token = action.payload.access_token;
      state.isAuthenticated = true;
      localStorage.setItem("token", action.payload.access_token);
    },
    setUser: (state, action: PayloadAction<any>) => {
      state.user = {
        id: action.payload.user_id,
        email: action.payload.user.email,
        is_active: action.payload.user.valid,
        is_superuser: action.payload.user.decoded.isSuperuser,
        is_verified: action.payload.user.validated,
      };
      localStorage.setItem("user", JSON.stringify(state.user));
    },
    logout: (state) => {
      state.token = null;
      state.user = null;
      state.isAuthenticated = false;
      localStorage.removeItem("token");
      localStorage.removeItem("user");
    },
  },
});

export const { setCredentials, setUser, logout } = authSlice.actions;
export default authSlice.reducer;
