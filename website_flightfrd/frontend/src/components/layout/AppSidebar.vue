<template>
  <aside class="app-sidebar">
    <nav class="sidebar-nav">
      <router-link to="/aircraft" class="nav-item">
        <span class="nav-icon">✈️</span>
        <span>飞机列表</span>
      </router-link>
      <router-link to="/atc" class="nav-item">
        <span class="nav-icon">📡</span>
        <span>ATC 消息</span>
      </router-link>
      <router-link to="/calendar" class="nav-item">
        <span class="nav-icon">📅</span>
        <span>日历</span>
      </router-link>
    </nav>
  </aside>
</template>

<script setup lang="ts">
// 侧边栏组件逻辑
</script>

<style scoped>
.app-sidebar {
  width: 250px;
  background-color: #34495e;
  padding: 1rem;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  color: white;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.nav-item:hover {
  background-color: #2c3e50;
}

.nav-item.router-link-active {
  background-color: #3498db;
}

.nav-icon {
  font-size: 1.2rem;
}
</style>
