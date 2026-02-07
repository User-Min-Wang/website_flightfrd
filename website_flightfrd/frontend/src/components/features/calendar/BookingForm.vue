<template>
  <form @submit.prevent="handleSubmit">
    <div class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">预约日期</label>
        <input
          type="date"
          v-model="formData.date"
          class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          required
          :min="today"
        />
      </div>
      
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">标题</label>
        <input
          type="text"
          v-model="formData.title"
          class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          placeholder="请输入预约标题"
          required
        />
      </div>
      
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">时间段</label>
        <div class="flex space-x-2">
          <input
            type="time"
            v-model="formData.startTime"
            class="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            required
          />
          <span class="self-center">至</span>
          <input
            type="time"
            v-model="formData.endTime"
            class="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            required
          />
        </div>
      </div>
      
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">描述</label>
        <textarea
          v-model="formData.description"
          rows="3"
          class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          placeholder="请输入预约描述（可选）"
        ></textarea>
      </div>
    </div>
    
    <div class="mt-6 flex justify-end space-x-3">
      <Button variant="secondary" @click="$emit('cancel')">取消</Button>
      <Button variant="primary" type="submit">保存预约</Button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue';
import Button from '@/components/common/Button.vue';

interface FormData {
  date: string;
  title: string;
  startTime: string;
  endTime: string;
  description: string;
}

interface Props {
  selectedDate?: string;
}

const props = withDefaults(defineProps<Props>(), {
  selectedDate: ''
});

const emit = defineEmits<{
  (e: 'save-booking', booking: Omit<FormData, never>): void;
  (e: 'cancel'): void;
}>();

const today = computed(() => {
  const date = new Date();
  return date.toISOString().split('T')[0];
});

const formData = reactive<FormData>({
  date: props.selectedDate || today.value,
  title: '',
  startTime: '09:00',
  endTime: '10:00',
  description: ''
});

const handleSubmit = () => {
  // Combine date and time for the booking
  const bookingData = {
    ...formData,
    timeRange: `${formData.startTime}-${formData.endTime}`
  };
  
  emit('save-booking', bookingData);
};
</script>