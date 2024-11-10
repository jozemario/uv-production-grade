import React, { useEffect, useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { useVerifyEmailMutation } from "../../features/auth/authApi";
const VerifyEmail: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [verifyEmail] = useVerifyEmailMutation();
  const [status, setStatus] = useState<"verifying" | "success" | "error">(
    "verifying"
  );
  const [error, setError] = useState("");

  useEffect(() => {
    const token = searchParams.get("token");

    if (!token) {
      setStatus("error");
      setError("Verification token is missing");
      return;
    }

    const verify = async () => {
      try {
        await verifyEmail({ token }).unwrap();
        setStatus("success");
        setTimeout(() => navigate("/login"), 3000);
      } catch (err: any) {
        setStatus("error");
        if (err.data?.detail === "VERIFY_USER_BAD_TOKEN") {
          setError("Invalid verification token");
        } else if (err.data?.detail === "VERIFY_USER_ALREADY_VERIFIED") {
          setError("Email is already verified");
        } else {
          setError("An error occurred during verification");
        }
      }
    };

    verify();
  }, [searchParams, verifyEmail, navigate]);

  return (
    <div className="max-w-md mx-auto mt-8">
      <div className="bg-white p-8 border rounded-lg shadow-sm">
        <h2 className="text-2xl font-bold mb-6 text-center">
          Email Verification
        </h2>

        {status === "verifying" && (
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Verifying your email...</p>
          </div>
        )}

        {status === "success" && (
          <div className="text-center text-green-600">
            <svg
              className="w-16 h-16 mx-auto"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M5 13l4 4L19 7"
              />
            </svg>
            <p className="mt-4">
              Email verified successfully! Redirecting to login...
            </p>
          </div>
        )}

        {status === "error" && (
          <div className="text-center text-red-600">
            <svg
              className="w-16 h-16 mx-auto"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
            <p className="mt-4">{error}</p>
            <button
              onClick={() => navigate("/login")}
              className="mt-4 text-blue-600 hover:text-blue-800"
            >
              Return to login
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default VerifyEmail;
