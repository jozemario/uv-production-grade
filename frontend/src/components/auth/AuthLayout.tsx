import React from "react";
import { Link } from "react-router-dom";
import AuthDebug from "../AuthDebug";

interface AuthLayoutProps {
  children: React.ReactNode;
  title: string;
  subtitle?: string;
  links?: Array<{
    text: string;
    to: string;
  }>;
}

const AuthLayout: React.FC<AuthLayoutProps> = ({
  children,
  title,
  subtitle,
  links,
}) => {
  return (
    // <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div className="h-full bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 className="text-center text-3xl font-extrabold text-gray-900">
          {title}
        </h2>
        {subtitle && (
          <p className="mt-2 text-center text-sm text-gray-600">{subtitle}</p>
        )}
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          {children}
        </div>

        {links && links.length > 0 && (
          <div className="mt-4 text-center space-x-4">
            {links.map((link, index) => (
              <Link
                key={index}
                to={link.to}
                className="text-sm text-blue-600 hover:text-blue-500"
              >
                {link.text}
              </Link>
            ))}
          </div>
        )}
      </div>
      <AuthDebug />
    </div>
  );
};

export default AuthLayout;
