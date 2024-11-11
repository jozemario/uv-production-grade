import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { RootState } from "../../store";
import {
  Todo,
  TodoCreate,
  TodoUpdate,
  Priority,
  Category,
  CategoryCreate,
  Webhook,
} from "../../types";

export const apiSlice = createApi({
  reducerPath: "api",
  baseQuery: fetchBaseQuery({
    baseUrl: "http://localhost:8000/api/v1",
    prepareHeaders: (headers, { getState }) => {
      const token = (getState() as RootState).auth.token;
      if (token) {
        headers.set("Authorization", `Bearer ${token}`);
      }
      return headers;
    },
    credentials: "include",
  }),
  tagTypes: ["Todo", "Category", "Priority", "Webhook"],
  endpoints: (builder) => ({
    // Todo endpoints
    getTodos: builder.query<Todo[], { skip?: number; limit?: number }>({
      query: ({ skip = 0, limit = 100 } = {}) =>
        `/todos?skip=${skip}&limit=${limit}`,
      providesTags: ["Todo"],
    }),
    createTodo: builder.mutation<Todo, TodoCreate>({
      query: (todo) => ({
        url: "/todos",
        method: "POST",
        body: todo,
      }),
      invalidatesTags: ["Todo"],
    }),
    updateTodo: builder.mutation<Todo, { todo_id: string; todo: TodoUpdate }>({
      query: ({ todo_id, todo }) => ({
        url: `/todos/${todo_id}`,
        method: "PUT",
        body: todo,
      }),
      invalidatesTags: ["Todo"],
    }),
    deleteTodo: builder.mutation<void, string>({
      query: (todo_id) => ({
        url: `/todos/${todo_id}`,
        method: "DELETE",
      }),
      invalidatesTags: ["Todo"],
    }),

    // Priority endpoints
    getPriorities: builder.query<Priority[], void>({
      query: () => "/priorities",
      providesTags: ["Priority"],
    }),

    // Category endpoints
    getCategories: builder.query<Category[], { skip?: number; limit?: number }>(
      {
        query: ({ skip = 0, limit = 100 } = {}) =>
          `/categories?skip=${skip}&limit=${limit}`,
        providesTags: ["Category"],
      }
    ),
    createCategory: builder.mutation<Category, CategoryCreate>({
      query: (category) => ({
        url: "/categories",
        method: "POST",
        body: category,
      }),
      invalidatesTags: ["Category"],
    }),
    deleteCategory: builder.mutation<void, string>({
      query: (category_id) => ({
        url: `/categories/${category_id}`,
        method: "DELETE",
      }),
      invalidatesTags: ["Category"],
    }),

    // Webhook endpoints
    getWebhooks: builder.query<Webhook[], {}>({
      query: () => ({
        url: "/webhooks",
        method: "GET",
      }),
    }),

    createWebhook: builder.mutation<Webhook, Partial<Webhook>>({
      query: (webhook) => ({
        url: "/webhooks",
        method: "POST",
        body: webhook,
      }),
      invalidatesTags: ["Webhook"],
    }),
  }),
});

export const {
  useGetTodosQuery,
  useCreateTodoMutation,
  useUpdateTodoMutation,
  useDeleteTodoMutation,
  useGetPrioritiesQuery,
  useGetCategoriesQuery,
  useCreateCategoryMutation,
  useDeleteCategoryMutation,
  useGetWebhooksQuery,
  useCreateWebhookMutation,
} = apiSlice;
