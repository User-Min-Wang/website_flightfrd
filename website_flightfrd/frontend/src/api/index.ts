import axios from 'axios'

// Create axios instance with base configuration
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
  timeout: 10000, // 10 seconds timeout
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor to add auth token if available
apiClient.interceptors.request.use(
  (config) => {
    // Get token from localStorage or Vuex/Pinia store
    const token = localStorage.getItem('authToken')
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle common errors
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // Handle specific error cases
    if (error.response?.status === 401) {
      // Unauthorized - possibly redirect to login
      console.error('Unauthorized access - token may be expired')
      // Could dispatch logout action here
    } else if (error.response?.status === 403) {
      console.error('Forbidden access')
    } else if (error.response?.status >= 500) {
      console.error('Server error occurred')
    }
    
    return Promise.reject(error)
  }
)

export default apiClient