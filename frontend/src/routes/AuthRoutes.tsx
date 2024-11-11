import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { useSelector } from "react-redux";
import { RootState } from "../store";
import Login from "../components/auth/Login";
import Register from "../components/auth/Register";
import ForgotPassword from "../components/auth/ForgotPassword";
import ResetPassword from "../components/auth/ResetPassword";
import VerifyEmail from "../components/auth/VerifyEmail";
import AuthLayout from "../components/auth/AuthLayout";
import TodoApp from "../components/TodoApp";
import DashboardLayout from "../components/DashboardLayout";
// Protected Route component
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const isAuthenticated = useSelector(
    (state: RootState) => state.auth.isAuthenticated
  );
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" />;
};

// Public Route component (accessible only when not authenticated)
const PublicRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const isAuthenticated = useSelector(
    (state: RootState) => state.auth.isAuthenticated
  );
  return !isAuthenticated ? <>{children}</> : <Navigate to="/tasks" />;
};

const AuthRoutes: React.FC<{ sx?: string }> = ({ sx }) => {
  return (
    <Routes className={sx}>
      {/* Public Routes */}
      <Route
        path="/login"
        element={
          <PublicRoute>
            <AuthLayout
              title="Sign In"
              subtitle="Welcome back to Todo App"
              links={[
                { text: "Register", to: "/register" },
                { text: "Forgot Password?", to: "/forgot-password" },
              ]}
            >
              <Login />
            </AuthLayout>
          </PublicRoute>
        }
      />

      <Route
        path="/register"
        element={
          <PublicRoute>
            <AuthLayout
              title="Create Account"
              subtitle="Start organizing your tasks today"
              links={[
                { text: "Already have an account? Sign in", to: "/login" },
              ]}
            >
              <Register />
            </AuthLayout>
          </PublicRoute>
        }
      />

      <Route
        path="/forgot-password"
        element={
          <PublicRoute>
            <AuthLayout
              title="Reset Password"
              subtitle="We'll send you a link to reset your password"
              links={[{ text: "Back to Login", to: "/login" }]}
            >
              <ForgotPassword />
            </AuthLayout>
          </PublicRoute>
        }
      />

      <Route
        path="/reset-password"
        element={
          <PublicRoute>
            <AuthLayout
              title="Set New Password"
              subtitle="Choose a new password for your account"
              links={[{ text: "Back to Login", to: "/login" }]}
            >
              <ResetPassword />
            </AuthLayout>
          </PublicRoute>
        }
      />

      <Route
        path="/verify-email"
        element={
          <AuthLayout
            title="Verify Email"
            subtitle="Confirming your email address"
            links={[{ text: "Back to Login", to: "/login" }]}
          >
            <VerifyEmail />
          </AuthLayout>
        }
      />

      {/* Protected Routes */}
      <Route
        path="/*"
        element={
          <ProtectedRoute>
            <DashboardLayout>
              <TodoApp />
            </DashboardLayout>
          </ProtectedRoute>
        }
      />

      {/* Catch all route */}
      <Route path="*" element={<Navigate to="/tasks" replace />} />
    </Routes>
  );
};

export default AuthRoutes;
