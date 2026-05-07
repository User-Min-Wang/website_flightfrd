<template>
  <div class="login-page">
    <div class="login-container">
      <h1>{{ $t('auth.login') }}</h1>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="identity">{{ $t('auth.username') }} / {{ $t('auth.email') }}</label>
          <input 
            type="text" 
            id="identity" 
            v-model="formData.identity" 
            required
            :placeholder="$t('auth.username')"
            class="form-input"
          />
        </div>
        
        <div class="form-group">
          <label for="password">{{ $t('auth.password') }}</label>
          <input 
            type="password" 
            id="password" 
            v-model="formData.password" 
            required
            :placeholder="$t('auth.password')"
            class="form-input"
          />
        </div>
        
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        
        <button type="submit" class="btn btn-primary btn-block" :disabled="isLoading">
          {{ isLoading ? $t('common.loading') : $t('auth.login') }}
        </button>
      </form>
      
      <div class="login-footer">
        <p>{{ $t('auth.noAccount') }} <router-link to="/register">{{ $t('nav.register') }}</router-link></p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/useAuthStore'
import type { LoginRequest } from '@/api/types'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const formData = reactive<LoginRequest>({
  identity: '',
  password: ''
})

const isLoading = ref(false)
const error = ref<string | null>(null)

const handleLogin = async () => {
  isLoading.value = true
  error.value = null

  try {
    await authStore.login(formData)
    // 登录成功后拉取用户信息，确保状态已刷新
    await authStore.fetchCurrentUser()
    // Redirect to the intended page or home
    const redirectPath = route.query.redirect as string || '/aircraft'
    router.push(redirectPath)
  } catch (err: any) {
    error.value = err.response?.data?.error || 'Login failed. Please check your credentials.'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: calc(100vh - 120px);
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f6fa;
  padding: 40px 20px;
}

.login-container {
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.login-container h1 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 30px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
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

.login-footer {
  margin-top: 20px;
  text-align: center;
}

.login-footer a {
  color: #3498db;
  text-decoration: none;
  font-weight: 500;
}

.login-footer a:hover {
  text-decoration: underline;
}
</style>
