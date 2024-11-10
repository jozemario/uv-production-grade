import React, { useState } from "react";
import { useRegisterMutation } from "../../features/auth/authApi";

interface RegisterFormData {
  email: string;
  password: string;
  confirmPassword: string;
}

interface FormErrors {
  email?: string;
  password?: string;
  confirmPassword?: string;
  general?: string;
}

const Register: React.FC = () => {
  const [formData, setFormData] = useState<RegisterFormData>({
    email: "",
    password: "",
    confirmPassword: "",
  });
  const [errors, setErrors] = useState<FormErrors>({});
  const [register, { isLoading }] = useRegisterMutation();
  const [isSuccess, setIsSuccess] = useState(false);

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};

    if (!formData.email) {
      newErrors.email = "Email is required";
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = "Please enter a valid email";
    }

    if (!formData.password) {
      newErrors.password = "Password is required";
    } else if (formData.password.length < 3) {
      newErrors.password = "Password must be at least 3 characters";
    }

    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = "Passwords do not match";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrors({});

    if (!validateForm()) return;

    try {
      await register({
        email: formData.email,
        password: formData.password,
      }).unwrap();

      setIsSuccess(true);
    } catch (err: any) {
      if (err.data?.detail === "REGISTER_USER_ALREADY_EXISTS") {
        setErrors({ email: "A user with this email already exists" });
      } else if (err.data?.detail?.code === "REGISTER_INVALID_PASSWORD") {
        setErrors({ password: err.data.detail.reason });
      } else {
        setErrors({ general: "An error occurred during registration" });
      }
      console.error("Failed to register:", err);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    if (errors[name as keyof FormErrors]) {
      setErrors((prev) => ({
        ...prev,
        [name]: undefined,
      }));
    }
  };

  if (isSuccess) {
    return (
      <div className="bg-green-50 p-4 rounded-md">
        <h3 className="text-green-800 font-medium">Registration Successful!</h3>
        <p className="text-green-700 mt-2">
          Please check your email to verify your account.
        </p>
      </div>
    );
  }

  return (
    <div className="max-w-md mx-auto mt-8">
      <div className="bg-white p-8 border rounded-lg shadow-sm">
        <h2 className="text-2xl font-bold mb-6 text-center">Register</h2>

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

          <div>
            <label
              htmlFor="confirmPassword"
              className="block text-sm font-medium text-gray-700"
            >
              Confirm Password
            </label>
            <input
              id="confirmPassword"
              type="password"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleInputChange}
              className={`mt-1 block w-full rounded-md border ${
                errors.confirmPassword ? "border-red-500" : "border-gray-300"
              } shadow-sm px-3 py-2 focus:border-blue-500 focus:ring focus:ring-blue-200`}
            />
            {errors.confirmPassword && (
              <p className="mt-1 text-sm text-red-600">
                {errors.confirmPassword}
              </p>
            )}
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className={`w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-white 
              ${isLoading ? "bg-blue-400" : "bg-blue-600 hover:bg-blue-700"} 
              focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500`}
          >
            {isLoading ? "Creating account..." : "Register"}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Register;
