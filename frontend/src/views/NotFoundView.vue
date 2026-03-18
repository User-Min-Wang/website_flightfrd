<template>
<<<<<<< HEAD:website_flightfrd/frontend/src/views/NotFoundView.vue
  <div class="not-found-view">
    <h1>404 - Page Not Found</h1>
    <p>抱歉，您访问的页面不存在。</p>
    <router-link to="/">返回首页</router-link>
=======
  <div class="not-found-page">
    <div class="not-found-container">
      <h1>404</h1>
      <h2>Page Not Found</h2>
      <p>The page you're looking for doesn't exist or has been moved.</p>
      <router-link to="/" class="btn btn-primary">Go Home</router-link>
    </div>
>>>>>>> origin/qwen-code-e1a46bfa-6c37-401a-848f-f7993735917e:frontend/src/views/NotFoundView.vue
  </div>
</template>

<script setup lang="ts">
<<<<<<< HEAD:website_flightfrd/frontend/src/views/NotFoundView.vue
// 404 页面逻辑
</script>

<style scoped>
.not-found-view {
  padding: 20px;
  text-align: center;
=======
// 404 Not Found page component
</script>

<style scoped>
.not-found-page {
  min-height: calc(100vh - 120px);
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f6fa;
  padding: 40px 20px;
}

.not-found-container {
  text-align: center;
  background: white;
  padding: 60px 40px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 500px;
}

.not-found-container h1 {
  font-size: 6rem;
  color: #3498db;
  margin: 0;
  line-height: 1;
}

.not-found-container h2 {
  color: #2c3e50;
  margin: 20px 0 10px;
}

.not-found-container p {
  color: #7f8c8d;
  margin-bottom: 30px;
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
>>>>>>> origin/qwen-code-e1a46bfa-6c37-401a-848f-f7993735917e:frontend/src/views/NotFoundView.vue
}
</style>
