import React, { useState } from "react";
import {
  useGetCategoriesQuery,
  useCreateCategoryMutation,
  useDeleteCategoryMutation,
} from "../../features/api/apiSlice";
import {
  PlusIcon,
  TrashIcon,
  ExclamationCircleIcon,
} from "@heroicons/react/24/outline";

export const CategoryManager: React.FC = () => {
  const [newCategoryName, setNewCategoryName] = useState("");
  const { data: categories = [], isLoading, error } = useGetCategoriesQuery({});
  const [createCategory] = useCreateCategoryMutation();
  const [deleteCategory] = useDeleteCategoryMutation();

  const categoryStyles = {
    system: "bg-gray-100 text-gray-800",
    user: "bg-blue-100 text-blue-800",
  };

  const handleCreateCategory = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newCategoryName.trim()) return;

    try {
      await createCategory({ name: newCategoryName }).unwrap();
      setNewCategoryName("");
    } catch (err) {
      console.error("Failed to create category:", err);
    }
  };

  const handleDeleteCategory = async (categoryId: string) => {
    try {
      await deleteCategory(categoryId).unwrap();
    } catch (err) {
      console.error("Failed to delete category:", err);
    }
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center p-4">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-md bg-red-50 p-4">
        <div className="flex">
          <ExclamationCircleIcon className="h-5 w-5 text-red-400" />
          <div className="ml-3">
            <h3 className="text-sm font-medium text-red-800">
              Error loading categories
            </h3>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <h2 className="text-lg font-medium text-gray-900 mb-4">Categories</h2>

      {/* Add Category Form */}
      <form onSubmit={handleCreateCategory} className="mb-6">
        <div className="flex gap-2">
          <input
            type="text"
            value={newCategoryName}
            onChange={(e) => setNewCategoryName(e.target.value)}
            placeholder="New category name"
            className="flex-1 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          />
          <button
            type="submit"
            className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            <PlusIcon className="-ml-1 mr-2 h-5 w-5" aria-hidden="true" />
            Add
          </button>
        </div>
      </form>

      {/* Categories List */}
      <div className="space-y-2">
        {categories.map((category) => (
          <div
            key={category.id}
            className={
              "flex items-center justify-between py-2 px-3 bg-gray-50 rounded-md"
            }
          >
            <span
              className={`text-gray-900 ${
                category.created_by_id
                  ? categoryStyles.user
                  : categoryStyles.system
              }`}
            >
              {category.name}
            </span>
            {/* Only show delete button for user-created categories */}
            {category.created_by_id && (
              <button
                onClick={() => handleDeleteCategory(category.id)}
                className="text-red-600 hover:text-red-800 p-1"
                title="Delete category"
              >
                <TrashIcon className="h-5 w-5" aria-hidden="true" />
              </button>
            )}
          </div>
        ))}
      </div>

      {categories.length === 0 && (
        <p className="text-gray-500 text-center py-4">
          No categories yet. Create one to get started!
        </p>
      )}
    </div>
  );
};
