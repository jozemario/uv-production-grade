import React, { useState } from "react";
import {
  useCreateTodoMutation,
  useGetCategoriesQuery,
  useGetPrioritiesQuery,
} from "../features/api/apiSlice";
const AddTodo: React.FC = () => {
  const [title, setTitle] = useState("");
  const [addTodo, { isLoading, error }] = useCreateTodoMutation();
  const { data: priorities } = useGetPrioritiesQuery();
  const { data: categories } = useGetCategoriesQuery({});

  console.log("categories", categories);
  console.log("priorities", priorities);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;
    try {
      await addTodo({
        content: title,
        priority_id:
          priorities?.find((priority) => priority.name === "Low")?.id || "",
        categories_ids:
          [
            categories?.find((category) => category.name === "Work")?.id || "",
          ] || [],
      }).unwrap();
      setTitle("");
    } catch (err) {
      console.error("Failed to add todo:", err);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mb-4">
      <input
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Add a new todo"
        className="border p-2 mr-2 rounded"
        disabled={isLoading}
      />
      <button
        type="submit"
        className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600 transition-colors"
        disabled={isLoading}
      >
        {isLoading ? "Adding..." : "Add Todo"}
      </button>
      {error && (
        <p className="text-red-500 mt-2">
          Error: {(error as any).data?.message || "Failed to add todo"}
        </p>
      )}
    </form>
  );
};

export default AddTodo;
