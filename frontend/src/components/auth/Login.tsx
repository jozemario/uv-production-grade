import React, { useState } from "react";
import { useLoginMutation } from "../../features/auth/authApi";
import { useDispatch } from "react-redux";
import { setCredentials, setUser } from "../../features/auth/authSlice";

interface LoginFormData {
  email: string;
  password: string;
}

interface FormErrors {
  email?: string;
  password?: string;
  general?: string;
}

const Login: React.FC = () => {
  const [formData, setFormData] = useState<LoginFormData>({
    email: "",
    password: "",
  });
  const [errors, setErrors] = useState<FormErrors>({});
  const [login, { isLoading }] = useLoginMutation();
  const dispatch = useDispatch();

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};

    if (!formData.email) {
      newErrors.email = "Email is required";
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = "Please enter a valid email";
    }

    if (!formData.password) {
      newErrors.password = "Password is required";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrors({});

    if (!validateForm()) return;

    try {
      // API expects username (email) and password
      const authResponse = await login({
        username: formData.email,
        password: formData.password,
      }).unwrap();

      dispatch(setCredentials(authResponse));
      dispatch(setUser(authResponse));
    } catch (err: any) {
      if (err.data?.detail === "LOGIN_BAD_CREDENTIALS") {
        setErrors({ general: "Invalid email or password" });
      } else if (err.data?.detail === "LOGIN_USER_NOT_VERIFIED") {
        setErrors({ general: "Please verify your email first" });
      } else {
        setErrors({ general: "An error occurred during login" });
      }
      console.error("Failed to log in:", err);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    // Clear error when user starts typing
    if (errors[name as keyof FormErrors]) {
      setErrors((prev) => ({
        ...prev,
        [name]: undefined,
      }));
    }
  };

  return (
    <div className="max-w-md mx-auto mt-8">
      <div className="bg-white p-8 border rounded-lg shadow-sm">
        <h2 className="text-2xl font-bold mb-6 text-center">Login</h2>

        {errors.general && (
          <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-md">
            {errors.general}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label
              htmlFor="email"
              className="block text-sm font-medium text-gray-700"
            >
              Email
            </label>
            <input
              id="email"
              type="email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              className={`mt-1 block w-full rounded-md border ${
                errors.email ? "border-red-500" : "border-gray-300"
              } shadow-sm px-3 py-2 focus:border-blue-500 focus:ring focus:ring-blue-200`}
              placeholder="your@email.com"
            />
            {errors.email && (
              <p className="mt-1 text-sm text-red-600">{errors.email}</p>
            )}
          </div>

          <div>
            <label
              htmlFor="password"
              className="block text-sm font-medium text-gray-700"
            >
              Password
            </label>
            <input
              id="password"
              type="password"
              name="password"
              value={formData.password}
              onChange={handleInputChange}
              className={`mt-1 block w-full rounded-md border ${
                errors.password ? "border-red-500" : "border-gray-300"
              } shadow-sm px-3 py-2 focus:border-blue-500 focus:ring focus:ring-blue-200`}
            />
            {errors.password && (
              <p className="mt-1 text-sm text-red-600">{errors.password}</p>
            )}
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className={`w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-white 
              ${isLoading ? "bg-blue-400" : "bg-blue-600 hover:bg-blue-700"} 
              focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500`}
          >
            {isLoading ? (
              <span className="flex items-center justify-center">
                <svg
                  className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  ></circle>
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
                Signing in...
              </span>
            ) : (
              "Sign in"
            )}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login;
