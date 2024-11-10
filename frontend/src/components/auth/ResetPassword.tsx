import React, { useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { useResetPasswordMutation } from "../../features/auth/authApi";
const ResetPassword: React.FC = () => {
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [resetPassword, { isLoading }] = useResetPasswordMutation();

  const token = searchParams.get("token");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    if (!token) {
      setError("Invalid reset token");
      return;
    }

    try {
      await resetPassword({ token, password }).unwrap();
      navigate("/login");
    } catch (err: any) {
      if (err.data?.detail === "RESET_PASSWORD_BAD_TOKEN") {
        setError("Invalid or expired reset token");
      } else if (err.data?.detail?.code === "RESET_PASSWORD_INVALID_PASSWORD") {
        setError(err.data.detail.reason);
      } else {
        setError("An error occurred while resetting password");
      }
    }
  };

  return (
    <div className="max-w-md mx-auto mt-8">
      <div className="bg-white p-8 border rounded-lg shadow-sm">
        <h2 className="text-2xl font-bold mb-6 text-center">
          Set New Password
        </h2>

        {error && (
          <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-md">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label
              htmlFor="password"
              className="block text-sm font-medium text-gray-700"
            >
              New Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-1 block w-full rounded-md border border-gray-300 shadow-sm px-3 py-2"
              required
            />
          </div>

          <div>
            <label
              htmlFor="confirmPassword"
              className="block text-sm font-medium text-gray-700"
            >
              Confirm New Password
            </label>
            <input
              id="confirmPassword"
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              className="mt-1 block w-full rounded-md border border-gray-300 shadow-sm px-3 py-2"
              required
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className={`w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-white 
              ${isLoading ? "bg-blue-400" : "bg-blue-600 hover:bg-blue-700"}`}
          >
            {isLoading ? "Resetting..." : "Reset Password"}
          </button>
        </form>
      </div>
    </div>
  );
};

export default ResetPassword;
