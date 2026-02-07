<template>
  <div class="bg-white shadow rounded-lg p-6">
    <h2 class="text-lg font-medium text-gray-900 mb-4">过滤器</h2>
    
    <div class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">频率 (MHz)</label>
        <select 
          v-model="localFilters.frequencies"
          multiple
          class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
        >
          <option value="118.0">118.0 - Ground Control</option>
          <option value="118.7">118.7 - Tower</option>
          <option value="119.1">119.1 - Approach</option>
          <option value="120.9">120.9 - Departure</option>
          <option value="121.5">121.5 - Emergency</option>
          <option value="124.0">124.0 - Center</option>
        </select>
        <p class="mt-1 text-sm text-gray-500">按住 Ctrl 键可多选</p>
      </div>
      
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">消息类型</label>
        <div class="space-y-2">
          <label class="flex items-center">
            <input
              v-model="localFilters.types"
              type="checkbox"
              value="info"
              class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
            <span class="ml-2 text-sm text-gray-700">信息 (蓝色)</span>
          </label>
          <label class="flex items-center">
            <input
              v-model="localFilters.types"
              type="checkbox"
              value="warning"
              class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
            <span class="ml-2 text-sm text-gray-700">警告 (黄色)</span>
          </label>
          <label class="flex items-center">
            <input
              v-model="localFilters.types"
              type="checkbox"
              value="error"
              class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
            <span class="ml-2 text-sm text-gray-700">错误 (红色)</span>
          </label>
        </div>
      </div>
      
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">标签</label>
        <div class="flex flex-wrap gap-2">
          <label class="inline-flex items-center">
            <input
              v-model="localFilters.tags"
              type="checkbox"
              value="climb"
              class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
            <span class="ml-2 text-sm text-gray-700">爬升</span>
          </label>
          <label class="inline-flex items-center">
            <input
              v-model="localFilters.tags"
              type="checkbox"
              value="descent"
              class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
            <span class="ml-2 text-sm text-gray-700">下降</span>
          </label>
          <label class="inline-flex items-center">
            <input
              v-model="localFilters.tags"
              type="checkbox"
              value="approach"
              class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
            <span class="ml-2 text-sm text-gray-700">进近</span>
          </label>
          <label class="inline-flex items-center">
            <input
              v-model="localFilters.tags"
              type="checkbox"
              value="departure"
              class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
            <span class="ml-2 text-sm text-gray-700">起飞</span>
          </label>
          <label class="inline-flex items-center">
            <input
              v-model="localFilters.tags"
              type="checkbox"
              value="emergency"
              class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
            <span class="ml-2 text-sm text-gray-700">紧急</span>
          </label>
        </div>
      </div>
      
      <button
        @click="applyFilters"
        class="w-full inline-flex justify-center items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
      >
        应用过滤器
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';

interface FilterOptions {
  frequencies: number[];
  tags: string[];
  types: string[];
}

interface Props {
  filters: FilterOptions;
}

interface Emits {
  (e: 'filter-change', filters: FilterOptions): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const localFilters = ref<FilterOptions>({ ...props.filters });

const applyFilters = () => {
  emit('filter-change', { ...localFilters.value });
};

// Watch for changes in props and update local state
watch(
  () => props.filters,
  (newFilters) => {
    localFilters.value = { ...newFilters };
  },
  { deep: true }
);
</script>