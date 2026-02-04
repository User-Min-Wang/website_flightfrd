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

// Authentication related types
export interface LoginCredentials {
  username: string
  password: string
}

export interface AuthResponse {
  access_token: string
  refresh_token?: string
  user: {
    id: number
    username: string
    email: string
    role: string
  }
}

// Error response type
export interface ApiErrorResponse {
  error: string
  message?: string
  statusCode: number
}