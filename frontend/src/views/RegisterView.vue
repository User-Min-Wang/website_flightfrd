<template>
  <div class="register-page">
    <div class="register-container">
      <h1>Create Account</h1>
      
      <form @submit.prevent="handleRegister" class="register-form">
        <div class="form-row">
          <div class="form-group">
            <label for="username">Username *</label>
            <input 
              type="text" 
              id="username" 
              v-model="formData.username" 
              required
              minlength="3"
              placeholder="Choose a username"
              class="form-input"
            />
          </div>
          
          <div class="form-group">
            <label for="email">Email *</label>
            <input 
              type="email" 
              id="email" 
              v-model="formData.email" 
              required
              placeholder="your@email.com"
              class="form-input"
            />
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="first_name">First Name</label>
            <input 
              type="text" 
              id="first_name" 
              v-model="formData.first_name"
              placeholder="John"
              class="form-input"
            />
          </div>
          
          <div class="form-group">
            <label for="last_name">Last Name</label>
            <input 
              type="text" 
              id="last_name" 
              v-model="formData.last_name"
              placeholder="Doe"
              class="form-input"
            />
          </div>
        </div>
        
        <div class="form-group">
          <label for="password">Password *</label>
          <input 
            type="password" 
            id="password" 
            v-model="formData.password" 
            required
            minlength="6"
            placeholder="At least 6 characters"
            class="form-input"
          />
        </div>
        
        <div class="form-group">
          <label for="confirm_password">Confirm Password *</label>
          <input 
            type="password" 
            id="confirm_password" 
            v-model="formData.confirm_password" 
            required
            minlength="6"
            placeholder="Confirm your password"
            class="form-input"
          />
        </div>
        
        <div class="verification-info">
          <p>📧 注册后需要验证邮箱才能激活完整账户功能。</p>
        </div>
        
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        
        <button type="submit" class="btn btn-primary btn-block" :disabled="isLoading">
          {{ isLoading ? 'Creating account...' : 'Register' }}
        </button>
      </form>
      
      <div class="register-footer">
        <p>Already have an account? <router-link to="/login">Login here</router-link></p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/useAuthStore'
import type { RegisterRequest } from '@/api/types'

const router = useRouter()
const authStore = useAuthStore()

const formData = reactive<RegisterRequest & { confirm_password: string }>({
  username: '',
  email: '',
  password: '',
  first_name: '',
  last_name: '',
  confirm_password: ''
})

const isLoading = ref(false)
const error = ref<string | null>(null)

const handleRegister = async () => {
  // Validate passwords match
  if (formData.password !== formData.confirm_password) {
    error.value = 'Passwords do not match'
    return
  }
  
  // Validate password length
  if (formData.password.length < 6) {
    error.value = 'Password must be at least 6 characters long'
    return
  }
  
  isLoading.value = true
  error.value = null
  
  try {
    const registerData: RegisterRequest = {
      username: formData.username,
      email: formData.email,
      password: formData.password,
      first_name: formData.first_name || undefined,
      last_name: formData.last_name || undefined
    }
    
    await authStore.register(registerData)
    // Show success message and redirect to home or verification page
    alert('注册成功！请检查您的邮箱以验证账户。')
    router.push('/')
  } catch (err: any) {
    const errors = err.response?.data?.errors
    if (errors) {
      // Format validation errors
      error.value = Object.values(errors).flat().join(', ')
    } else {
      error.value = err.response?.data?.error || 'Registration failed. Please try again.'
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.register-page {
  min-height: calc(100vh - 120px);
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f6fa;
  padding: 40px 20px;
}

.register-container {
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 500px;
}

.register-container h1 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 30px;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-weight: 500;
  color: #2c3e50;
}

.form-group label span {
  color: #e74c3c;
}

.form-input {
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-input:focus {
  outline: none;
  border-color: #3498db;
}

.error-message {
  background-color: #fee;
  color: #c0392b;
  padding: 10px;
  border-radius: 4px;
  font-size: 0.9rem;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s;
}

.btn-primary {
  background-color: #3498db;
  color: white;
}

.btn-primary:hover {
  background-color: #2980b9;
}

.btn-primary:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}

.btn-block {
  width: 100%;
}

.register-footer {
  margin-top: 20px;
  text-align: center;
}

.register-footer a {
  color: #3498db;
  text-decoration: none;
  font-weight: 500;
}

.register-footer a:hover {
  text-decoration: underline;
}

@media (max-width: 600px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}

.verification-info {
  background-color: #e8f4fd;
  border-left: 4px solid #3498db;
  padding: 12px 15px;
  border-radius: 4px;
  margin-top: 10px;
}

.verification-info p {
  margin: 0;
  color: #2c3e50;
  font-size: 0.9rem;
}
</style>
