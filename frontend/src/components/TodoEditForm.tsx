import React, { useState, useEffect } from "react";
import { Todo, Priority, Category } from "../types";
import { XMarkIcon } from "@heroicons/react/24/outline";

interface TodoEditFormProps {
  todo: Todo;
  priorities: Priority[];
  categories: Category[];
  onSave: (updatedTodo: Todo) => void;
  onCancel: () => void;
}

export const TodoEditForm: React.FC<TodoEditFormProps> = ({
  todo,
  priorities,
  categories,
  onSave,
  onCancel,
}) => {
  const [formData, setFormData] = useState({
    content: todo.content,
    priority_id: todo.priority.id,
    categories_ids: todo.categories.map((cat) => cat.id),
    is_completed: todo.is_completed,
  });
  const [error, setError] = useState<string>("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.content.trim()) {
      setError("Content cannot be empty");
      return;
    }
    onSave({
      ...todo,
      content: formData.content,
      priority: priorities.find((p) => p.id === formData.priority_id)!,
      categories: categories.filter((c) =>
        formData.categories_ids.includes(c.id)
      ),
      is_completed: formData.is_completed,
    });
  };

  const handleCategoryToggle = (categoryId: string) => {
    setFormData((prev) => ({
      ...prev,
      categories_ids: prev.categories_ids.includes(categoryId)
        ? prev.categories_ids.filter((id) => id !== categoryId)
        : [...prev.categories_ids, categoryId],
    }));
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <div className="text-red-600 bg-red-50 p-2 rounded">{error}</div>
      )}

      {/* Content Input */}
      <div>
        <label className="block text-sm font-medium text-gray-700">
          Content
        </label>
        <input
          type="text"
          value={formData.content}
          onChange={(e) =>
            setFormData((prev) => ({ ...prev, content: e.target.value }))
          }
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
        />
      </div>

      {/* Priority Selection */}
      <div>
        <label className="block text-sm font-medium text-gray-700">
          Priority
        </label>
        <select
          value={formData.priority_id}
          onChange={(e) =>
            setFormData((prev) => ({
              ...prev,
              priority_id: e.target.value,
            }))
          }
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
        >
          {priorities.map((priority) => (
            <option key={priority.id} value={priority.id}>
              {priority.name}
            </option>
          ))}
        </select>
      </div>

      {/* Categories Selection */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Categories
        </label>
        <div className="space-y-2">
          {categories.map((category) => (
            <label key={category.id} className="flex items-center space-x-2">
              <input
                type="checkbox"
                checked={formData.categories_ids.includes(category.id)}
                onChange={() => handleCategoryToggle(category.id)}
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <span className="text-sm text-gray-700">{category.name}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Status Toggle */}
      <div>
        <label className="flex items-center space-x-2">
          <input
            type="checkbox"
            checked={formData.is_completed}
            onChange={(e) =>
              setFormData((prev) => ({
                ...prev,
                is_completed: e.target.checked,
              }))
            }
            className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
          />
          <span className="text-sm text-gray-700">Mark as completed</span>
        </label>
      </div>

      {/* Form Actions */}
      {/* <div className="flex justify-end space-x-2 pt-4 border-t">
        <button
          type="button"
          onClick={onCancel}
          className="inline-flex justify-center py-2 px-4 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          Cancel
        </button>
        <button
          type="submit"
          className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          Save Changes
        </button>
      </div> */}
      <div className="flex justify-end space-x-3 pt-6">
        <button
          type="button"
          onClick={onCancel}
          className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          Cancel
        </button>
        <button
          type="submit"
          className="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          Save Changes
        </button>
      </div>
    </form>
  );
};
