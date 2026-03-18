import apiClient from './index'
import type { LoginRequest, RegisterRequest, AuthResponse, User } from './types'

export const authApi = {
  /**
   * Register a new user
   */
  async register(data: RegisterRequest): Promise<AuthResponse> {
    const response = await apiClient.post('/auth/register', data)
    return response.data
  },

  /**
   * Login user
   */
  async login(data: LoginRequest): Promise<AuthResponse> {
    const response = await apiClient.post('/auth/login', data)
    return response.data
  },

  /**
   * Logout user
   */
  async logout(): Promise<void> {
    await apiClient.post('/auth/logout')
  },

  /**
   * Get current user information
   */
  async getCurrentUser(): Promise<{ user: User }> {
    const response = await apiClient.get('/auth/me')
    return response.data
  }
}
