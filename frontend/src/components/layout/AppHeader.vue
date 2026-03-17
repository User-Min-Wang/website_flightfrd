<template>
  <header class="app-header">
    <div class="header-container">
      <div class="logo">
        <router-link to="/">FlightFRD</router-link>
      </div>
      
      <nav class="main-nav" v-if="isAuthenticated">
        <router-link to="/aircraft">Aircraft</router-link>
        <router-link to="/atc">ATC</router-link>
        <router-link to="/calendar">Calendar</router-link>
        <router-link to="/about">About</router-link>
      </nav>
      
      <div class="auth-buttons" v-if="!isAuthenticated">
        <router-link to="/login" class="btn btn-outline">Login</router-link>
        <router-link to="/register" class="btn btn-primary">Register</router-link>
      </div>
      
      <div class="user-menu" v-else>
        <span class="username">{{ currentUser?.username }}</span>
        <button @click="handleLogout" class="btn btn-outline btn-sm">Logout</button>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/useAuthStore'

const router = useRouter()
const authStore = useAuthStore()

const isAuthenticated = computed(() => authStore.isAuthenticated)
const currentUser = computed(() => authStore.currentUser)

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.app-header {
  background-color: #2c3e50;
  color: white;
  padding: 15px 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo a {
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
  text-decoration: none;
}

.main-nav {
  display: flex;
  gap: 20px;
}

.main-nav a {
  color: white;
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.main-nav a:hover,
.main-nav a.router-link-active {
  background-color: rgba(255, 255, 255, 0.1);
}

.auth-buttons {
  display: flex;
  gap: 10px;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 15px;
}

.username {
  font-weight: 500;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  font-size: 0.9rem;
  transition: all 0.3s;
}

.btn-primary {
  background-color: #3498db;
  color: white;
}

.btn-primary:hover {
  background-color: #2980b9;
}

.btn-outline {
  background-color: transparent;
  border: 1px solid white;
  color: white;
}

.btn-outline:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.btn-sm {
  padding: 5px 12px;
  font-size: 0.85rem;
}
</style>
