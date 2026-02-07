<template>
  <div v-if="loading" class="flex items-center justify-center p-8">
    <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
    <span v-if="showText" class="ml-3 text-gray-600">Loading...</span>
  </div>
  <div v-else>
    <slot />
  </div>
</template>

<script setup lang="ts">
interface Props {
  loading: boolean;
  showText?: boolean;
}

withDefaults(defineProps<Props>(), {
  showText: true
});
</script>