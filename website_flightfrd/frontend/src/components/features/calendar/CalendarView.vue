<template>
  <div class="bg-white shadow rounded-lg overflow-hidden">
    <div class="px-4 py-5 sm:p-6">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-lg leading-6 font-medium text-gray-900">预约日历</h2>
        <div class="flex items-center space-x-4">
          <button
            @click="prevMonth"
            class="inline-flex items-center px-3 py-1 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
          >
            &larr; 上月
          </button>
          <h3 class="text-lg font-medium text-gray-900">{{ currentMonthYear }}</h3>
          <button
            @click="nextMonth"
            class="inline-flex items-center px-3 py-1 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
          >
            下月 &rarr;
          </button>
        </div>
      </div>

      <div class="grid grid-cols-7 gap-1 mb-2">
        <div v-for="day in weekdays" :key="day" class="text-center text-sm font-medium text-gray-500 py-2">
          {{ day }}
        </div>
      </div>

      <div class="grid grid-cols-7 gap-1">
        <div
          v-for="day in daysInCalendar"
          :key="day.date"
          :class="[
            'min-h-24 p-2 border rounded',
            day.isCurrentMonth ? 'bg-white' : 'bg-gray-50 text-gray-400',
            isSelected(day.date) ? 'bg-blue-50 border-blue-300' : '',
            isToday(day.date) ? 'bg-yellow-50 border-yellow-300' : ''
          ]"
        >
          <div class="flex justify-between">
            <span :class="['text-sm font-medium', isToday(day.date) ? 'text-red-600' : '']">
              {{ day.dayNumber }}
            </span>
            <button
              v-if="day.isCurrentMonth"
              @click="openBookingModal(day.date)"
              class="text-xs text-blue-600 hover:text-blue-800"
            >
              预约
            </button>
          </div>
          
          <div class="mt-1 space-y-1 max-h-20 overflow-y-auto">
            <div
              v-for="booking in getBookingsForDay(day.date)"
              :key="booking.id"
              :title="`${booking.title} - ${booking.timeRange}`"
              class="text-xs p-1 bg-blue-100 text-blue-800 rounded truncate"
            >
              {{ booking.title }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Booking Modal -->
  <Modal
    :is-open="showBookingModal"
    title="新建预约"
    @close="closeBookingModal"
  >
    <BookingForm
      :selected-date="selectedDate"
      @save-booking="handleSaveBooking"
      @cancel="closeBookingModal"
    />
  </Modal>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import Modal from '@/components/common/Modal.vue';
import BookingForm from './BookingForm.vue';

interface Booking {
  id: string;
  date: string; // YYYY-MM-DD
  title: string;
  timeRange: string; // e.g. "09:00-10:00"
  description: string;
}

interface Props {
  bookings: Booking[];
}

const props = withDefaults(defineProps<Props>(), {
  bookings: () => []
});

const emit = defineEmits<{
  (e: 'add-booking', booking: Omit<Booking, 'id'>): void;
}>();

const currentDate = new Date();
const currentMonth = ref(currentDate.getMonth());
const currentYear = ref(currentDate.getFullYear());
const showBookingModal = ref(false);
const selectedDate = ref('');

const weekdays = ['日', '一', '二', '三', '四', '五', '六'];

const currentMonthYear = computed(() => {
  return `${currentYear.value}年${currentMonth.value + 1}月`;
});

const daysInCalendar = computed(() => {
  const firstDayOfMonth = new Date(currentYear.value, currentMonth.value, 1);
  const lastDayOfMonth = new Date(currentYear.value, currentMonth.value + 1, 0);
  const startDate = new Date(firstDayOfMonth);
  startDate.setDate(startDate.getDate() - firstDayOfMonth.getDay()); // Start from Sunday

  const days = [];
  const tempDate = new Date(startDate);

  for (let i = 0; i < 42; i++) { // 6 weeks * 7 days
    days.push({
      date: tempDate.toISOString().split('T')[0],
      dayNumber: tempDate.getDate(),
      isCurrentMonth: tempDate.getMonth() === currentMonth.value
    });

    tempDate.setDate(tempDate.getDate() + 1);
  }

  return days;
});

const isToday = (dateString: string) => {
  const today = new Date();
  const date = new Date(dateString);
  return (
    date.getDate() === today.getDate() &&
    date.getMonth() === today.getMonth() &&
    date.getFullYear() === today.getFullYear()
  );
};

const isSelected = (dateString: string) => {
  return dateString === selectedDate.value;
};

const getBookingsForDay = (dateString: string) => {
  return props.bookings.filter(booking => booking.date === dateString);
};

const nextMonth = () => {
  if (currentMonth.value === 11) {
    currentMonth.value = 0;
    currentYear.value++;
  } else {
    currentMonth.value++;
  }
};

const prevMonth = () => {
  if (currentMonth.value === 0) {
    currentMonth.value = 11;
    currentYear.value--;
  } else {
    currentMonth.value--;
  }
};

const openBookingModal = (date: string) => {
  selectedDate.value = date;
  showBookingModal.value = true;
};

const closeBookingModal = () => {
  showBookingModal.value = false;
  selectedDate.value = '';
};

const handleSaveBooking = (bookingData: Omit<Booking, 'id'>) => {
  emit('add-booking', bookingData);
  closeBookingModal();
};
</script>