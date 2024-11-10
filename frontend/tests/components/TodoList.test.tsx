import React from "react";
import { render, screen } from "@testing-library/react";
import { Provider } from "react-redux";
import { configureStore } from "@reduxjs/toolkit";
import TodoList from "../../src/components/TodoList";
import { todoApi } from "../../src/features/todos/todoApi";

const mockStore = configureStore({
  reducer: {
    [todoApi.reducerPath]: todoApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(todoApi.middleware),
});

test("renders loading state", () => {
  render(
    <Provider store={mockStore}>
      <TodoList />
    </Provider>
  );
  expect(screen.getByText(/loading/i)).toBeInTheDocument();
});
