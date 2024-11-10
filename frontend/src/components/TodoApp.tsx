import React from "react";
import TodoList from "./TodoList";
import AddTodo from "./AddTodo";
import { useLogoutMutation } from "../features/auth/authApi";
import { logout } from "../features/auth/authSlice";
import { useAppDispatch } from "../hooks/useAppDispatch";
import AuthDebug from "./AuthDebug";
import { CategoryManager } from "./categories/CategoryManager";
import {
  NavLink,
  useLocation,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import { ListBulletIcon, TagIcon } from "@heroicons/react/24/outline";

const TodoApp: React.FC = () => {
  const [logoutMutation] = useLogoutMutation();
  const dispatch = useAppDispatch();
  const location = useLocation();

  const handleLogout = async () => {
    try {
      await logoutMutation().unwrap();
      dispatch(logout());
    } catch (error) {
      console.error("Logout failed:", error);
      // Still logout on the client side even if the server request fails
      dispatch(logout());
    }
  };

  const NavButton: React.FC<{
    to: string;
    icon: React.ReactNode;
    label: string;
  }> = ({ to, icon, label }) => (
    <NavLink
      to={to}
      className={({ isActive }) =>
        `inline-flex items-center px-4 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
          isActive
            ? "bg-blue-100 text-blue-700"
            : "text-gray-600 hover:bg-gray-100"
        }`
      }
    >
      <span className="mr-2">{icon}</span>
      {label}
    </NavLink>
  );

  return (
    //<div className="min-h-screen bg-gray-50">
    <div className="h-full bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-6">
          <h1 className="text-3xl font-bold text-gray-900">Todo App</h1>
          <div className="flex items-center space-x-4">
            <AuthDebug />
            <button
              onClick={handleLogout}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
            >
              Logout
            </button>
          </div>
        </div>

        <div className="border-b border-gray-200 mb-6">
          <nav className="flex space-x-4">
            <NavButton
              to="/tasks"
              icon={<ListBulletIcon className="h-5 w-5" />}
              label="Tasks"
            />
            <NavButton
              to="/categories"
              icon={<TagIcon className="h-5 w-5" />}
              label="Categories"
            />
          </nav>
        </div>

        <div className="space-y-6">
          <Routes>
            <Route
              path="/tasks"
              element={
                <>
                  <AddTodo />
                  <TodoList />
                </>
              }
            />
            <Route path="/categories" element={<CategoryManager />} />
            <Route path="/" element={<Navigate to="/tasks" replace />} />
          </Routes>
        </div>
      </div>
    </div>
  );
};

export default TodoApp;
