import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { RootState } from "../../store";
import {
  AuthResponse,
  ForgotPasswordRequest,
  ResetPasswordError,
  ResetPasswordRequest,
  User,
  UserCreate,
  UserLogin,
} from "../../types";

export const authApi = createApi({
  reducerPath: "authApi",
  baseQuery: fetchBaseQuery({
    baseUrl: "http://localhost:8000/api/v1/",
    prepareHeaders: (headers, { getState }) => {
      const token = (getState() as RootState).auth.token;
      if (token) {
        headers.set("Authorization", `Bearer ${token}`);
      }
      return headers;
    },
  }),
  tagTypes: ["User"],
  endpoints: (builder) => ({
    // Auth endpoints
    register: builder.mutation<User, UserCreate>({
      query: (credentials) => ({
        url: "/auth/register",
        method: "POST",
        body: credentials,
      }),
    }),
    login: builder.mutation<AuthResponse, UserLogin>({
      query: (credentials) => ({
        url: "/auth/login",
        method: "POST",
        body: new URLSearchParams({
          username: credentials.username,
          password: credentials.password,
        }),
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      }),
    }),
    logout: builder.mutation<void, void>({
      query: () => ({
        url: "/auth/custom-logout",
        method: "POST",
      }),
    }),
    requestVerification: builder.mutation<void, { email: string }>({
      query: (data) => ({
        url: "/auth/request-verify-token",
        method: "POST",
        body: data,
      }),
    }),
    verifyEmail: builder.mutation<void, { token: string }>({
      query: (data) => ({
        url: "/auth/verify",
        method: "POST",
        body: data,
      }),
    }),
    forgotPassword: builder.mutation<void, { email: string }>({
      query: (data) => ({
        url: "/auth/forgot-password",
        method: "POST",
        body: data,
      }),
    }),
    resetPassword: builder.mutation<void, ResetPasswordRequest>({
      query: (data) => ({
        url: "/auth/reset-password",
        method: "POST",
        body: data,
      }),
    }),
    getCurrentUser: builder.query<User, void>({
      query: () => "/users/me",
      providesTags: ["User"],
    }),
  }),
});

export const {
  useRegisterMutation,
  useLoginMutation,
  useLogoutMutation,
  useRequestVerificationMutation,
  useVerifyEmailMutation,
  useGetCurrentUserQuery,
  useForgotPasswordMutation,
  useResetPasswordMutation,
} = authApi;
