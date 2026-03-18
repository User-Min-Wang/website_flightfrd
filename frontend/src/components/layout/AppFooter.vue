<template>
  <footer class="app-footer">
<<<<<<< HEAD:website_flightfrd/frontend/src/components/layout/AppFooter.vue
    <div class="footer-content">
      <p>&copy; 2024 FlightFRD - 航班追踪与管理系统</p>
=======
    <div class="footer-container">
      <p>&copy; 2024 FlightFRD. All rights reserved.</p>
      <div class="footer-links">
        <router-link to="/about">About</router-link>
        <a href="#">Privacy Policy</a>
        <a href="#">Terms of Service</a>
      </div>
>>>>>>> origin/qwen-code-e1a46bfa-6c37-401a-848f-f7993735917e:frontend/src/components/layout/AppFooter.vue
    </div>
  </footer>
</template>

<script setup lang="ts">
<<<<<<< HEAD:website_flightfrd/frontend/src/components/layout/AppFooter.vue
// 底部组件逻辑
=======
// Footer component
>>>>>>> origin/qwen-code-e1a46bfa-6c37-401a-848f-f7993735917e:frontend/src/components/layout/AppFooter.vue
</script>

<style scoped>
.app-footer {
  background-color: #2c3e50;
  color: white;
<<<<<<< HEAD:website_flightfrd/frontend/src/components/layout/AppFooter.vue
  padding: 1rem 2rem;
  text-align: center;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
=======
  padding: 20px 0;
  margin-top: auto;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-container p {
  margin: 0;
}

.footer-links {
  display: flex;
  gap: 20px;
}

.footer-links a,
.footer-links router-link {
  color: white;
  text-decoration: none;
  font-size: 0.9rem;
}

.footer-links a:hover,
.footer-links router-link:hover {
  text-decoration: underline;
>>>>>>> origin/qwen-code-e1a46bfa-6c37-401a-848f-f7993735917e:frontend/src/components/layout/AppFooter.vue
}
</style>
