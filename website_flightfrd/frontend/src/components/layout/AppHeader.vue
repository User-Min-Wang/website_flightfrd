<template>
  <header class="app-header">
    <div class="header-content">
      <div class="logo">
        <router-link to="/">FlightFRD</router-link>
      </div>
      <nav class="header-nav">
        <router-link to="/aircraft">飞机</router-link>
        <router-link to="/atc">ATC</router-link>
        <router-link to="/calendar">日历</router-link>
        <router-link to="/about">关于</router-link>
      </nav>
    </div>
  </header>
</template>

<script setup lang="ts">
// 头部组件逻辑
</script>

<style scoped>
.app-header {
  background-color: #2c3e50;
  color: white;
  padding: 1rem 2rem;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

.logo a {
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
}

.header-nav {
  display: flex;
  gap: 1.5rem;
}

.header-nav a {
  color: white;
  transition: opacity 0.3s;
}

.header-nav a:hover {
  opacity: 0.8;
}
</style>
