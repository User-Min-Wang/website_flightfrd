<template>

  <div class="calendar-page">
    <div class="calendar-header">
      <h1>Flight Calendar</h1>
      <div class="controls">
        <button @click="previousMonth" class="btn btn-outline">&lt;</button>
        <span class="current-month">{{ currentMonthYear }}</span>
        <button @click="nextMonth" class="btn btn-outline">&gt;</button>
      </div>
    </div>

    <div class="calendar-grid">
      <!-- Weekday headers -->
      <div class="weekday-header" v-for="day in weekdays" :key="day">
        {{ day }}
      </div>

      <!-- Calendar days -->
      <div 
        v-for="day in calendarDays" 
        :key="day.date"
        class="calendar-day"
        :class="{ 'other-month': !day.currentMonth, 'today': day.isToday }"
      >
        <span class="day-number">{{ day.dayOfMonth }}</span>
        <div class="day-flights" v-if="day.flights.length > 0">
          <div 
            v-for="flight in day.flights.slice(0, 3)" 
            :key="flight.id"
            class="flight-indicator"
            :title="flight.callsign"
          >
            {{ flight.callsign }}
          </div>
          <div v-if="day.flights.length > 3" class="more-flights">
            +{{ day.flights.length - 3 }} more
          </div>
        </div>
      </div>
    </div>

    <!-- Selected day flights -->
    <div v-if="selectedDayFlights.length > 0" class="selected-day-flights">
      <h2>Flights for {{ selectedDate }}</h2>
      <div class="flights-list">
        <div v-for="flight in selectedDayFlights" :key="flight.id" class="flight-card">
          <div class="flight-info">
            <span class="flight-callsign">{{ flight.callsign }}</span>
            <span class="flight-route">{{ flight.origin }} → {{ flight.destination }}</span>
          </div>
          <div class="flight-times">
            <span>Departure: {{ flight.departure_time }}</span>
            <span>Arrival: {{ flight.arrival_time }}</span>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">

import { ref, computed } from 'vue'

const weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
const currentDate = ref(new Date())
const selectedDate = ref('')

// Mock flight data
const mockFlights = [
  { id: 1, callsign: 'AAL123', origin: 'JFK', destination: 'LAX', departure_time: '08:00', arrival_time: '11:30', date: new Date().toISOString().split('T')[0] },
  { id: 2, callsign: 'UAL456', origin: 'ORD', destination: 'SFO', departure_time: '09:15', arrival_time: '11:45', date: new Date().toISOString().split('T')[0] },
  { id: 3, callsign: 'DAL789', origin: 'ATL', destination: 'SEA', departure_time: '10:30', arrival_time: '13:00', date: new Date().toISOString().split('T')[0] },
]

const currentMonthYear = computed(() => {
  return currentDate.value.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })
})

const calendarDays = computed(() => {
  const year = currentDate.value.getFullYear()
  const month = currentDate.value.getMonth()
  
  const firstDay = new Date(year, month, 1)
  const lastDay = new Date(year, month + 1, 0)
  const prevLastDay = new Date(year, month, 0)
  
  const startDay = firstDay.getDay()
  const totalDays = lastDay.getDate()
  const prevMonthDays = prevLastDay.getDate()
  
  const days = []
  const today = new Date().toISOString().split('T')[0]
  
  // Previous month days
  for (let i = startDay - 1; i >= 0; i--) {
    days.push({
      date: `${year}-${String(month).padStart(2, '0')}-${prevMonthDays - i}`,
      dayOfMonth: prevMonthDays - i,
      currentMonth: false,
      isToday: false,
      flights: []
    })
  }
  
  // Current month days
  for (let i = 1; i <= totalDays; i++) {
    const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`
    days.push({
      date: dateStr,
      dayOfMonth: i,
      currentMonth: true,
      isToday: dateStr === today,
      flights: mockFlights.filter(f => f.date === dateStr)
    })
  }
  
  // Next month days
  const remainingDays = 42 - days.length
  for (let i = 1; i <= remainingDays; i++) {
    days.push({
      date: `${year}-${String(month + 2).padStart(2, '0')}-${i}`,
      dayOfMonth: i,
      currentMonth: false,
      isToday: false,
      flights: []
    })
  }
  
  return days
})

const selectedDayFlights = computed(() => {
  if (!selectedDate.value) return []
  return mockFlights.filter(f => f.date === selectedDate.value)
})

const previousMonth = () => {
  currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() - 1, 1)
}

const nextMonth = () => {
  currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() + 1, 1)
}
</script>

<style scoped>
.calendar-page {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.calendar-header h1 {
  color: #2c3e50;
  margin: 0;
}

.controls {
  display: flex;
  gap: 15px;
  align-items: center;
}

.current-month {
  font-size: 1.3rem;
  font-weight: 600;
  color: #2c3e50;
  min-width: 200px;
  text-align: center;
}

.btn {
  padding: 8px 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  background: white;
  font-size: 1rem;
}

.btn:hover {
  background: #f5f6fa;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 1px;
  background: #ddd;
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
}

.weekday-header {
  background: #34495e;
  color: white;
  padding: 10px;
  text-align: center;
  font-weight: 600;
}

.calendar-day {
  background: white;
  min-height: 100px;
  padding: 8px;
  cursor: pointer;
  transition: background 0.3s;
}

.calendar-day:hover {
  background: #f5f6fa;
}

.calendar-day.other-month {
  background: #f9f9f9;
  color: #bdc3c7;
}

.calendar-day.today {
  background: #e8f4fc;
  border: 2px solid #3498db;
}

.day-number {
  font-weight: 600;
  display: block;
  margin-bottom: 5px;
}

.day-flights {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.flight-indicator {
  background: #3498db;
  color: white;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 0.75rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.more-flights {
  font-size: 0.75rem;
  color: #7f8c8d;
  text-align: center;
}

.selected-day-flights {
  margin-top: 30px;
}

.selected-day-flights h2 {
  color: #2c3e50;
  margin-bottom: 20px;
}

.flights-list {
  display: grid;
  gap: 15px;
}

.flight-card {
  background: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.flight-callsign {
  font-weight: bold;
  color: #2c3e50;
  font-size: 1.1rem;
}

.flight-route {
  color: #7f8c8d;
  margin-left: 10px;
}

.flight-times {
  display: flex;
  gap: 20px;
  color: #34495e;
  font-size: 0.9rem;

}
</style>
