<template>
  <header class="bg-white shadow-sm border-b">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16 items-center">
        <div class="flex items-center">
          <h1 class="text-xl font-bold text-gray-900">FlightFRD</h1>
        </div>
        <nav class="hidden md:flex space-x-8">
          <router-link 
            to="/" 
            class="text-gray-500 hover:text-gray-700 px-3 py-2 rounded-md text-sm font-medium"
            active-class="text-blue-600 bg-blue-50"
          >
            首页
          </router-link>
          <router-link 
            to="/atc" 
            class="text-gray-500 hover:text-gray-700 px-3 py-2 rounded-md text-sm font-medium"
            active-class="text-blue-600 bg-blue-50"
          >
            ATC 通信
          </router-link>
          <router-link 
            to="/calendar" 
            class="text-gray-500 hover:text-gray-700 px-3 py-2 rounded-md text-sm font-medium"
            active-class="text-blue-600 bg-blue-50"
          >
            预约日历
          </router-link>
          <router-link 
            to="/about" 
            class="text-gray-500 hover:text-gray-700 px-3 py-2 rounded-md text-sm font-medium"
            active-class="text-blue-600 bg-blue-50"
          >
            关于
          </router-link>
        </nav>
        <div class="flex items-center">
          <button 
            @click="toggleTheme"
            class="p-2 rounded-full text-gray-500 hover:text-gray-700 focus:outline-none"
          >
            <svg v-if="!isDarkMode" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useSettingsStore } from '@/stores/useSettingsStore';

const settingsStore = useSettingsStore();

const isDarkMode = computed(() => settingsStore.theme === 'dark');

const toggleTheme = () => {
  settingsStore.toggleTheme();
};
</script>