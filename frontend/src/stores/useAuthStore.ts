import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'
import type { LoginRequest, RegisterRequest, User } from '@/api/types'

export const useAuthStore = defineStore('auth', () => {
  // State
  const token = ref<string | null>(localStorage.getItem('authToken'))
  const user = ref<User | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const isAuthenticated = computed(() => !!token.value)
  const currentUser = computed(() => user.value)

  // Actions
  async function login(credentials: LoginRequest) {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await authApi.login(credentials)
      token.value = response.token
      user.value = response.user
      
      // Save token to localStorage
      localStorage.setItem('authToken', response.token)
      
      return response
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Login failed'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function register(userData: RegisterRequest) {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await authApi.register(userData)
      token.value = response.token
      user.value = response.user
      
      // Save token to localStorage
      localStorage.setItem('authToken', response.token)
      
      return response
    } catch (err: any) {
      error.value = err.response?.data?.errors || err.response?.data?.error || 'Registration failed'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function logout() {
    try {
      await authApi.logout()
    } catch (err) {
      console.error('Logout error:', err)
    } finally {
      // Clear local state regardless of API success
      token.value = null
      user.value = null
      localStorage.removeItem('authToken')
    }
  }

  async function fetchCurrentUser() {
    if (!token.value) return
    
    isLoading.value = true
    error.value = null
    
    try {
      const response = await authApi.getCurrentUser()
      user.value = response.user
      return response.user
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Failed to fetch user data'
      if (err.response?.status === 401) {
        // Token is invalid or expired, logout
        await logout()
      }
      throw err
    } finally {
      isLoading.value = false
    }
  }

  // Initialize auth state on app load
  function initializeAuth() {
    const savedToken = localStorage.getItem('authToken')
    if (savedToken) {
      token.value = savedToken
      // Fetch user data if token exists
      fetchCurrentUser().catch(() => {
        // Silently fail - user will be logged out if token is invalid
      })
    }
  }

  return {
    // State
    token,
    user,
    isLoading,
    error,
    // Getters
    isAuthenticated,
    currentUser,
    // Actions
    login,
    register,
    logout,
    fetchCurrentUser,
    initializeAuth
  }
})
