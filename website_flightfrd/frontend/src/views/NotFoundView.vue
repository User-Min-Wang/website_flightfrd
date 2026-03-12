<template>
  <div class="not-found-view">
    <h1>404 - Page Not Found</h1>
    <p>抱歉，您访问的页面不存在。</p>
    <router-link to="/">返回首页</router-link>
  </div>
</template>

<script setup lang="ts">
// 404 页面逻辑
</script>

<style scoped>
.not-found-view {
  padding: 20px;
  text-align: center;
}
</style>
