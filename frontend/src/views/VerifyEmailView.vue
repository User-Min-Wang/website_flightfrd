<template>
  <div class="verify-email-page">
    <div class="verify-container">
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>验证中...</p>
      </div>
      
      <div v-else-if="success" class="success-state">
        <div class="success-icon">✓</div>
        <h2>邮箱验证成功！</h2>
        <p>您的邮箱已成功验证，现在可以完全访问所有功能。</p>
        <router-link to="/" class="btn btn-primary">返回首页</router-link>
      </div>
      
      <div v-else class="error-state">
        <div class="error-icon">✗</div>
        <h2>验证失败</h2>
        <p>{{ errorMessage }}</p>
        <div class="action-buttons">
          <button @click="resendVerification" class="btn btn-secondary" :disabled="resending">
            {{ resending ? '发送中...' : '重新发送验证邮件' }}
          </button>
          <router-link to="/register" class="btn btn-primary">返回注册</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/api'

const route = useRoute()
const loading = ref(true)
const success = ref(false)
const errorMessage = ref('')
const resending = ref(false)

onMounted(async () => {
  const token = route.params.token as string
  
  if (!token) {
    loading.value = false
    errorMessage.value = '缺少验证令牌'
    return
  }
  
  try {
    const response = await api.get(`/auth/verify-email/${token}`)
    success.value = true
    loading.value = false
  } catch (error: any) {
    loading.value = false
    errorMessage.value = error.response?.data?.error || '验证链接无效或已过期'
  }
})

const resendVerification = async () => {
  resending.value = true
  
  try {
    // Get user email from localStorage or prompt user
    const email = prompt('请输入您注册时使用的邮箱地址：')
    if (!email) {
      resending.value = false
      return
    }
    
    await api.post('/auth/resend-verification', { email })
    alert('验证邮件已重新发送，请检查您的邮箱。')
  } catch (error: any) {
    alert(error.response?.data?.error || '发送失败，请稍后重试')
  } finally {
    resending.value = false
  }
}
</script>

<style scoped>
.verify-email-page {
  min-height: calc(100vh - 120px);
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f6fa;
  padding: 40px 20px;
}

.verify-container {
  background: white;
  padding: 50px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 450px;
  text-align: center;
}

.loading-state,
.success-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.success-icon {
  width: 70px;
  height: 70px;
  background-color: #27ae60;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  font-weight: bold;
}

.error-icon {
  width: 70px;
  height: 70px;
  background-color: #e74c3c;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  font-weight: bold;
}

h2 {
  color: #2c3e50;
  margin: 0;
}

p {
  color: #7f8c8d;
  margin: 0;
  line-height: 1.6;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  text-decoration: none;
  transition: all 0.3s;
  display: inline-block;
}

.btn-primary {
  background-color: #3498db;
  color: white;
}

.btn-primary:hover {
  background-color: #2980b9;
}

.btn-secondary {
  background-color: #95a5a6;
  color: white;
}

.btn-secondary:hover {
  background-color: #7f8c8d;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.action-buttons {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
  justify-content: center;
}
</style>
