import React from "react";
import { Todo } from "../types";
import {
  useDeleteTodoMutation,
  useUpdateTodoMutation,
} from "../features/api/apiSlice";

interface TodoItemProps {
  todo: Todo;
}

const TodoItem: React.FC<TodoItemProps> = ({ todo }) => {
  const [updateTodo] = useUpdateTodoMutation();
  const [deleteTodo] = useDeleteTodoMutation();

  return (
    <div className="flex items-center justify-between p-2 border-b">
      <div className="flex items-center">
        <input
          type="checkbox"
          checked={todo.is_completed}
          onChange={() =>
            updateTodo({
              todo_id: todo.id,
              todo: {
                is_completed: !todo.is_completed,
                content: todo.content,
                priority_id: todo.priority.id,
                categories_ids: todo.categories.map((category) => category.id),
              },
            })
          }
          className="mr-2"
        />
        <span className={todo.is_completed ? "line-through" : ""}>
          {todo.content}
        </span>
      </div>
      <button
        onClick={() => deleteTodo(todo.id)}
        className="bg-red-500 text-white p-1 rounded"
      >
        Delete
      </button>
    </div>
  );
};

export default TodoItem;
