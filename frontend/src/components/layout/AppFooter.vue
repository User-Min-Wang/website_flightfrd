<template>
  <footer class="app-footer">
    <div class="footer-container">
      <p>&copy; 2024 FlightFRD. All rights reserved.</p>
      <div class="footer-links">
        <router-link to="/about">About</router-link>
        <a href="#">Privacy Policy</a>
        <a href="#">Terms of Service</a>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
// Footer component
</script>

<style scoped>
.app-footer {
  background-color: #2c3e50;
  color: white;
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
}
</style>
