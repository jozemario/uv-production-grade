import React, { useState } from "react";
import {
  useGetTodosQuery,
  useUpdateTodoMutation,
  useDeleteTodoMutation,
  useGetPrioritiesQuery,
  useGetCategoriesQuery,
} from "../features/api/apiSlice";
import { Todo, Category, Priority } from "../types";
import {
  TrashIcon,
  PencilSquareIcon,
  CheckCircleIcon,
  XCircleIcon,
  ExclamationCircleIcon,
} from "@heroicons/react/24/outline";
import { CheckIcon } from "@heroicons/react/24/solid";
import { TodoEditForm } from "./TodoEditForm";
interface TodoItemProps {
  todo: Todo;
  priorities: Priority[];
  categories: Category[];
  onEdit: (todo: Todo) => void;
}

const TodoItem: React.FC<TodoItemProps> = ({
  todo,
  priorities,
  categories,
  onEdit,
}) => {
  const [updateTodo] = useUpdateTodoMutation();
  const [deleteTodo] = useDeleteTodoMutation();

  const handleToggleComplete = async () => {
    try {
      await updateTodo({
        todo_id: todo.id,
        todo: {
          content: todo.content,
          priority_id: todo.priority.id,
          categories_ids: todo.categories.map((cat) => cat.id),
          is_completed: !todo.is_completed,
        },
      }).unwrap();
    } catch (error) {
      console.error("Failed to update todo:", error);
    }
  };

  const handleDelete = async () => {
    try {
      await deleteTodo(todo.id).unwrap();
    } catch (error) {
      console.error("Failed to delete todo:", error);
    }
  };

  const getPriorityColor = (priorityName: string) => {
    switch (priorityName.toLowerCase()) {
      case "high":
        return "text-red-600 bg-red-100";
      case "medium":
        return "text-yellow-600 bg-yellow-100";
      case "low":
        return "text-green-600 bg-green-100";
      default:
        return "text-gray-600 bg-gray-100";
    }
  };

  return (
    <div className="flex items-center justify-between p-4 bg-white rounded-lg shadow mb-2 hover:shadow-md transition-shadow duration-200">
      <div className="flex items-center space-x-4 flex-grow">
        <button onClick={handleToggleComplete} className="focus:outline-none">
          {todo.is_completed ? (
            <CheckCircleIcon className="h-6 w-6 text-green-500" />
          ) : (
            <div className="h-6 w-6 rounded-full border-2 border-gray-300 hover:border-gray-400" />
          )}
        </button>

        <div className="flex-grow">
          <p
            className={`text-gray-800 ${
              todo.is_completed ? "line-through text-gray-500" : ""
            }`}
          >
            {todo.content}
          </p>

          <div className="flex flex-wrap gap-2 mt-2">
            <span
              className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getPriorityColor(
                todo.priority.name
              )}`}
            >
              {todo.priority.name}
            </span>

            {todo.categories.map((category) => (
              <span
                key={category.id}
                className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium text-gray-600 bg-gray-100"
              >
                {category.name}
              </span>
            ))}
          </div>
        </div>
      </div>

      <div className="flex items-center space-x-2">
        <button
          onClick={() => onEdit(todo)}
          className="p-2 text-blue-600 hover:text-blue-800 transition-colors duration-200"
          aria-label="Edit todo"
        >
          <PencilSquareIcon className="h-5 w-5" />
        </button>

        <button
          onClick={handleDelete}
          className="p-2 text-red-600 hover:text-red-800 transition-colors duration-200"
          aria-label="Delete todo"
        >
          <TrashIcon className="h-5 w-5" />
        </button>
      </div>
    </div>
  );
};

const TodoList: React.FC = () => {
  const [editingTodo, setEditingTodo] = useState<Todo | null>(null);
  const { data: todos = [], isLoading, error } = useGetTodosQuery({});
  const { data: priorities = [] } = useGetPrioritiesQuery();
  const { data: categories = [] } = useGetCategoriesQuery({});
  const [updateTodo] = useUpdateTodoMutation();

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-[200px]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-md p-4">
        <div className="flex">
          <ExclamationCircleIcon className="h-5 w-5 text-red-600 mr-2" />
          <div>
            <h3 className="text-sm font-medium text-red-800">
              Error loading todos
            </h3>
            <p className="mt-1 text-sm text-red-700">
              {(error as any).data?.detail || "An unexpected error occurred"}
            </p>
          </div>
        </div>
      </div>
    );
  }

  const activeTodos = todos.filter((todo) => !todo.is_completed);
  const completedTodos = todos.filter((todo) => todo.is_completed);

  const handleEditSubmit = async (todo: Todo) => {
    console.log("handleEditSubmit", todo);
    if (!editingTodo) return;

    try {
      await updateTodo({
        todo_id: editingTodo.id,
        todo: {
          content: todo.content,
          priority_id: todo.priority.id,
          categories_ids: todo.categories.map((cat) => cat.id),
          is_completed: todo.is_completed,
        },
      }).unwrap();
      setEditingTodo(null);
    } catch (error) {
      console.error("Failed to update todo:", error);
    }
  };

  return (
    // <div className="space-y-4">
    <div className="">
      {todos.length === 0 ? (
        <div className="text-center py-12 bg-white rounded-lg shadow">
          <CheckIcon className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No todos</h3>
          <p className="mt-1 text-sm text-gray-500">
            Get started by creating a new todo.
          </p>
        </div>
      ) : (
        <div>
          {/* Active Todos */}
          <div className="mb-8">
            <h2 className="text-lg font-semibold text-gray-700 mb-4">
              Active Tasks
            </h2>
            {activeTodos.map((todo) => (
              <TodoItem
                key={todo.id}
                todo={todo}
                priorities={priorities}
                categories={categories}
                onEdit={setEditingTodo}
              />
            ))}
          </div>

          {/* Completed Todos */}
          {completedTodos.length > 0 && (
            <div>
              <h2 className="text-lg font-semibold text-gray-700 mb-4">
                Completed Tasks
              </h2>
              {completedTodos.map((todo) => (
                <TodoItem
                  key={todo.id}
                  todo={todo}
                  priorities={priorities}
                  categories={categories}
                  onEdit={setEditingTodo}
                />
              ))}
            </div>
          )}
        </div>
      )}

      {/* Edit Modal */}
      {editingTodo && (
        <>
          {/* Overlay */}
          <div
            className={`fixed inset-0 bg-black transition-opacity duration-300 ease-in-out ${
              editingTodo ? "opacity-50" : "opacity-0"
            }`}
            onClick={() => setEditingTodo(null)}
          />

          {/* Modal */}
          <div
            className={`fixed inset-0 flex items-center justify-center p-4 z-50 transition-all duration-300 ease-in-out ${
              editingTodo ? "scale-100 opacity-100" : "scale-95 opacity-0"
            }`}
          >
            <div
              className="bg-white rounded-lg shadow-xl p-6 max-w-md w-full"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-medium">Edit Todo</h3>
                <button
                  onClick={() => setEditingTodo(null)}
                  className="text-gray-400 hover:text-gray-500"
                >
                  <XCircleIcon className="h-6 w-6" />
                </button>
              </div>

              <TodoEditForm
                todo={editingTodo}
                priorities={priorities}
                categories={categories}
                onSave={handleEditSubmit}
                onCancel={() => setEditingTodo(null)}
              />

              {/* <div className="mt-4 flex justify-end space-x-2">
              <button
                onClick={() => setEditingTodo(null)}
                className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-800"
              >
                Cancel
              </button>
              <button
                onClick={() => handleEditSubmit(editingTodo)}
                className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Save Changes
              </button>
            </div> */}
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default TodoList;
