<template>
  <aside class="app-sidebar">
    <nav class="sidebar-nav">
      <router-link to="/aircraft" class="nav-item">
        <span class="nav-icon">✈️</span>
<<<<<<< HEAD:website_flightfrd/frontend/src/components/layout/AppSidebar.vue
        <span>飞机列表</span>
      </router-link>
      <router-link to="/atc" class="nav-item">
        <span class="nav-icon">📡</span>
        <span>ATC 消息</span>
      </router-link>
      <router-link to="/calendar" class="nav-item">
        <span class="nav-icon">📅</span>
        <span>日历</span>
=======
        <span>Aircraft</span>
      </router-link>
      <router-link to="/atc" class="nav-item">
        <span class="nav-icon">📻</span>
        <span>ATC</span>
      </router-link>
      <router-link to="/calendar" class="nav-item">
        <span class="nav-icon">📅</span>
        <span>Calendar</span>
      </router-link>
      <router-link to="/about" class="nav-item">
        <span class="nav-icon">ℹ️</span>
        <span>About</span>
>>>>>>> origin/qwen-code-e1a46bfa-6c37-401a-848f-f7993735917e:frontend/src/components/layout/AppSidebar.vue
      </router-link>
    </nav>
  </aside>
</template>

<script setup lang="ts">
<<<<<<< HEAD:website_flightfrd/frontend/src/components/layout/AppSidebar.vue
// 侧边栏组件逻辑
=======
// Sidebar navigation component
>>>>>>> origin/qwen-code-e1a46bfa-6c37-401a-848f-f7993735917e:frontend/src/components/layout/AppSidebar.vue
</script>

<style scoped>
.app-sidebar {
  width: 250px;
  background-color: #34495e;
<<<<<<< HEAD:website_flightfrd/frontend/src/components/layout/AppSidebar.vue
  padding: 1rem;
=======
  color: white;
  padding: 20px 0;
  min-height: calc(100vh - 120px);
>>>>>>> origin/qwen-code-e1a46bfa-6c37-401a-848f-f7993735917e:frontend/src/components/layout/AppSidebar.vue
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
<<<<<<< HEAD:website_flightfrd/frontend/src/components/layout/AppSidebar.vue
  gap: 0.5rem;
=======
  gap: 5px;
>>>>>>> origin/qwen-code-e1a46bfa-6c37-401a-848f-f7993735917e:frontend/src/components/layout/AppSidebar.vue
}

.nav-item {
  display: flex;
  align-items: center;
<<<<<<< HEAD:website_flightfrd/frontend/src/components/layout/AppSidebar.vue
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
=======
  gap: 12px;
  padding: 12px 20px;
  color: white;
  text-decoration: none;
  transition: background-color 0.3s;
}

.nav-item:hover,
.nav-item.router-link-active {
  background-color: rgba(255, 255, 255, 0.1);
>>>>>>> origin/qwen-code-e1a46bfa-6c37-401a-848f-f7993735917e:frontend/src/components/layout/AppSidebar.vue
}

.nav-icon {
  font-size: 1.2rem;
}
</style>
