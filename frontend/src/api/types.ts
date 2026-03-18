// Common API response types

export interface ApiResponse<T> {
  data: T
  message?: string
  success: boolean
}

export interface PaginationInfo {
  page: number
  pages: number
  total: number
  has_next: boolean
  has_prev: boolean
}

export interface ListResponse<T> {
  items: T[]
  pagination: PaginationInfo
}

// User related types
export interface User {
  id: number
  username: string
  email: string
  first_name?: string
  last_name?: string
  role: string
  is_active: boolean
  is_verified: boolean
  created_at: string
  updated_at: string
}

// Authentication related types
export interface LoginRequest {
  identity: string  // Can be username or email
  password: string
}

export interface RegisterRequest {
  username: string
  email: string
  password: string
  first_name?: string
  last_name?: string
}

export interface AuthResponse {
  message: string
  token: string
  user: User
}

// Error response type
export interface ApiErrorResponse {
  error: string
  message?: string
  statusCode: number
}