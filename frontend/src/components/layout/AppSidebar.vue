<template>
  <aside class="app-sidebar">
    <nav class="sidebar-nav">
      <router-link to="/aircraft" class="nav-item">
        <span class="nav-icon">✈️</span>
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
      </router-link>
    </nav>
  </aside>
</template>

<script setup lang="ts">
// Sidebar navigation component
</script>

<style scoped>
.app-sidebar {
  width: 250px;
  background-color: #34495e;
  color: white;
  padding: 20px 0;
  min-height: calc(100vh - 120px);
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 20px;
  color: white;
  text-decoration: none;
  transition: background-color 0.3s;
}

.nav-item:hover,
.nav-item.router-link-active {
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-icon {
  font-size: 1.2rem;
}
</style>
