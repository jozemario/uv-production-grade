import React, { useState } from "react";
import { useForgotPasswordMutation } from "../../features/auth/authApi";
const ForgotPassword: React.FC = () => {
  const [email, setEmail] = useState("");
  const [isSuccess, setIsSuccess] = useState(false);
  const [forgotPassword, { isLoading }] = useForgotPasswordMutation();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      await forgotPassword({ email }).unwrap();
      setIsSuccess(true);
    } catch (err) {
      console.error("Failed to send reset email:", err);
    }
  };

  if (isSuccess) {
    return (
      <div className="bg-green-50 p-4 rounded-md">
        <h3 className="text-green-800 font-medium">Reset Email Sent!</h3>
        <p className="text-green-700 mt-2">
          Please check your email for password reset instructions.
        </p>
      </div>
    );
  }

  return (
    <div className="max-w-md mx-auto mt-8">
      <div className="bg-white p-8 border rounded-lg shadow-sm">
        <h2 className="text-2xl font-bold mb-6 text-center">Reset Password</h2>
        <p className="text-gray-600 mb-6 text-center">
          Enter your email address and we'll send you instructions to reset your
          password.
        </p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label
              htmlFor="email"
              className="block text-sm font-medium text-gray-700"
            >
              Email Address
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
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
            {isLoading ? "Sending..." : "Send Reset Instructions"}
          </button>
        </form>
      </div>
    </div>
  );
};

export default ForgotPassword;
