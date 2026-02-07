<template>
  <div class="flex items-center">
    <span class="mr-2 text-sm font-medium text-gray-700">主题</span>
    <button
      @click="toggleTheme"
      class="relative inline-flex h-6 w-11 items-center rounded-full bg-gray-200 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
      :class="{ 'bg-blue-600': isDarkMode }"
    >
      <span
        class="inline-block h-4 w-4 transform rounded-full bg-white transition-transform"
        :class="{ 'translate-x-6': isDarkMode }"
      />
    </button>
    <span class="ml-2 text-sm text-gray-500">
      {{ isDarkMode ? '深色' : '浅色' }}
    </span>
  </div>
</template>

<script setup lang="ts">
import { useSettingsStore } from '@/stores/useSettingsStore';

const settingsStore = useSettingsStore();

const isDarkMode = computed(() => settingsStore.theme === 'dark');

const toggleTheme = () => {
  settingsStore.toggleTheme();
};
</script>