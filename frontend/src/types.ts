export interface Todo {
  id: string;
  content: string;
  is_completed: boolean;
  priority: Priority;
  categories: Category[];
}

export interface TodoCreate {
  content: string;
  priority_id: string;
  categories_ids: string[];
}

export interface TodoUpdate {
  content: string;
  priority_id: string;
  categories_ids: string[];
  is_completed: boolean;
}

export interface Priority {
  id: string;
  name: string;
}

export interface Category {
  id: string;
  name: string;
  created_by_id: string | null;
}

export interface CategoryCreate {
  name: string;
}

export interface CategoryUpdate {
  name: string;
}

export interface User {
  id: string;
  email: string;
  is_active: boolean;
  is_superuser: boolean;
  is_verified: boolean;
}

export interface UserCreate {
  email: string;
  password: string;
}

export interface UserLogin {
  username: string; // email is used as username
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface ForgotPasswordRequest {
  email: string;
}

export interface ResetPasswordRequest {
  token: string;
  password: string;
}

export interface ResetPasswordError {
  detail:
    | {
        code: "RESET_PASSWORD_BAD_TOKEN" | "RESET_PASSWORD_INVALID_PASSWORD";
        reason?: string;
      }
    | string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface Webhook {
  url: string;
  events: string[];
  is_active: boolean;
}
