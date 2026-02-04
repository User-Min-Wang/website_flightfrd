<template>
  <div id="app">
    <AppHeader />
    <div class="main-content">
      <AppSidebar v-if="showSidebar" />
      <main :class="{ 'full-width': !showSidebar }">
        <router-view />
      </main>
    </div>
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppSidebar from '@/components/layout/AppSidebar.vue'
import AppFooter from '@/components/layout/AppFooter.vue'

const route = useRoute()

// Define routes that should not show sidebar
const routesWithoutSidebar = ['/', '/about']

const showSidebar = computed(() => {
  return !routesWithoutSidebar.includes(route.path)
})
</script>

<style scoped>
.main-content {
  display: flex;
  min-height: calc(100vh - 120px); /* Adjust based on header/footer height */
}

.full-width {
  width: 100%;
  margin: 0 auto;
}

main {
  flex: 1;
  padding: 20px;
}
</style>