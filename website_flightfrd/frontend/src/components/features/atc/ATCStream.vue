<template>
  <div class="bg-white shadow rounded-lg overflow-hidden h-full flex flex-col">
    <div class="px-4 py-5 sm:p-6 flex-grow overflow-y-auto">
      <h2 class="text-lg leading-6 font-medium text-gray-900 mb-4">ATC 通信流</h2>
      
      <div class="space-y-3">
        <div 
          v-for="(message, index) in sortedMessages" 
          :key="index" 
          :class="[
            'p-3 rounded-lg border',
            message.type === 'info' ? 'bg-blue-50 border-blue-200' : 
            message.type === 'warning' ? 'bg-yellow-50 border-yellow-200' : 
            message.type === 'error' ? 'bg-red-50 border-red-200' : 'bg-gray-50 border-gray-200'
          ]"
        >
          <div class="flex justify-between items-start">
            <div>
              <h3 class="font-semibold text-gray-900">{{ message.callsign }}</h3>
              <p class="text-sm text-gray-500 mt-1">{{ message.frequency }} MHz</p>
            </div>
            <div class="text-right">
              <p class="text-xs text-gray-500">{{ formatDate(message.timestamp) }}</p>
              <p class="text-xs text-gray-500">{{ formatTime(message.timestamp) }}</p>
            </div>
          </div>
          
          <p class="mt-2 text-gray-700">{{ message.content }}</p>
          
          <div class="mt-2 flex flex-wrap gap-2">
            <span 
              v-for="tag in message.tags" 
              :key="tag"
              class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800"
            >
              {{ tag }}
            </span>
          </div>
        </div>
        
        <div v-if="messages.length === 0" class="text-center py-8 text-gray-500">
          暂无通信记录
        </div>
      </div>
    </div>
    
    <div class="border-t bg-gray-50 px-4 py-3 sm:px-6">
      <div class="flex items-center justify-between">
        <div class="text-sm text-gray-700">
          共 {{ messages.length }} 条记录
        </div>
        <button
          @click="clearMessages"
          class="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
        >
          清空
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ATCMessage } from '@/types/atc';
import { formatDate, formatTime } from '@/utils/formatters';

interface Props {
  messages: ATCMessage[];
}

const props = defineProps<Props>();

const emit = defineEmits<{
  (e: 'clear'): void;
}>();

const sortedMessages = computed(() => {
  return [...props.messages].sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
});

const clearMessages = () => {
  emit('clear');
};
</script>