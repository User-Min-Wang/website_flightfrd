<template>
<<<<<<< HEAD:website_flightfrd/frontend/src/views/ATCView.vue
  <div class="atc-view">
    <h1>ATC View</h1>
    <p>空中交通管制界面 - 开发中...</p>
=======
  <div class="atc-page">
    <div class="atc-header">
      <h1>ATC Communications</h1>
      <div class="controls">
        <select v-model="selectedFrequency" class="form-select">
          <option value="">All Frequencies</option>
          <option v-for="freq in frequencies" :key="freq" :value="freq">{{ freq }}</option>
        </select>
        <button @click="toggleStream" class="btn" :class="streamActive ? 'btn-warning' : 'btn-success'">
          {{ streamActive ? 'Pause Stream' : 'Resume Stream' }}
        </button>
      </div>
    </div>

    <div class="messages-container">
      <div 
        v-for="message in filteredMessages" 
        :key="message.id" 
        class="message-card"
        :class="message.message_type"
      >
        <div class="message-header">
          <span class="frequency-badge">{{ formatFrequency(message.frequency) }}</span>
          <span class="callsign">{{ message.callsign || 'N/A' }}</span>
          <span class="timestamp">{{ formatDate(message.received_at) }}</span>
        </div>
        <div class="message-content">
          {{ message.message_content }}
        </div>
        <div class="message-footer">
          <span class="message-type-badge" :class="message.message_type">
            {{ message.message_type }}
          </span>
        </div>
      </div>
      
      <div v-if="filteredMessages.length === 0" class="no-messages">
        <p>No ATC messages available</p>
      </div>
    </div>
>>>>>>> origin/qwen-code-e1a46bfa-6c37-401a-848f-f7993735917e:frontend/src/views/ATCView.vue
  </div>
</template>

<script setup lang="ts">
<<<<<<< HEAD:website_flightfrd/frontend/src/views/ATCView.vue
// ATC 视图逻辑
</script>

<style scoped>
.atc-view {
  padding: 20px;
=======
import { ref, computed } from 'vue'
import { formatFrequency, formatDate } from '@/utils/formatters'

// Mock data - would be replaced with actual API calls
const frequencies = ['118.100', '118.700', '119.100', '120.900', '121.900']
const selectedFrequency = ref('')
const streamActive = ref(true)

const mockMessages = [
  { id: 1, frequency: '118.700', callsign: 'AAL123', message_content: 'Requesting taxi to runway 24L', message_type: 'taxi', received_at: new Date().toISOString() },
  { id: 2, frequency: '120.900', callsign: 'UAL456', message_content: 'Cleared for takeoff runway 24L', message_type: 'takeoff', received_at: new Date().toISOString() },
  { id: 3, frequency: '119.100', callsign: 'DAL789', message_content: 'Descending to 10,000 feet', message_type: 'position', received_at: new Date().toISOString() },
  { id: 4, frequency: '121.900', callsign: 'SWA101', message_content: 'Monitoring emergency frequency', message_type: 'emergency', received_at: new Date().toISOString() },
  { id: 5, frequency: '118.100', callsign: 'ASA202', message_content: 'Requesting ILS approach runway 24R', message_type: 'landing', received_at: new Date().toISOString() },
  { id: 6, frequency: '118.700', callsign: 'BAW303', message_content: 'Pushback approved', message_type: 'clearance', received_at: new Date().toISOString() },
  { id: 7, frequency: '120.900', callsign: 'AFR404', message_content: 'Contact departure on 120.9', message_type: 'contact', received_at: new Date().toISOString() },
]

const filteredMessages = computed(() => {
  if (!streamActive.value) return []
  
  return mockMessages.filter(message => {
    return !selectedFrequency.value || message.frequency === selectedFrequency.value
  })
})

const toggleStream = () => {
  streamActive.value = !streamActive.value
}
</script>

<style scoped>
.atc-page {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.atc-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #ecf0f1;
}

.atc-header h1 {
  color: #2c3e50;
  margin: 0;
}

.controls {
  display: flex;
  gap: 10px;
  align-items: center;
}

.form-select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
  background: white;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s;
}

.btn-success {
  background-color: #2ecc71;
  color: white;
}

.btn-warning {
  background-color: #f39c12;
  color: white;
}

.messages-container {
  display: grid;
  gap: 15px;
}

.message-card {
  background: white;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-left: 4px solid #bdc3c7;
}

.message-card.clearance { border-left-color: #27ae60; }
.message-card.contact { border-left-color: #2980b9; }
.message-card.taxi { border-left-color: #8e44ad; }
.message-card.takeoff { border-left-color: #2ecc71; }
.message-card.landing { border-left-color: #e74c3c; }
.message-card.position { border-left-color: #f39c12; }
.message-card.emergency { border-left-color: #c0392b; }

.message-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: 0.9rem;
}

.frequency-badge {
  font-weight: bold;
  color: #2980b9;
}

.callsign {
  font-weight: 600;
  color: #2c3e50;
}

.timestamp {
  color: #7f8c8d;
}

.message-content {
  color: #34495e;
  margin-bottom: 10px;
  line-height: 1.5;
}

.message-footer {
  display: flex;
  justify-content: flex-end;
}

.message-type-badge {
  font-size: 0.75rem;
  font-weight: bold;
  text-transform: uppercase;
  padding: 3px 8px;
  border-radius: 4px;
  background: #ecf0f1;
}

.message-type-badge.clearance { background: #d5f5e3; color: #27ae60; }
.message-type-badge.contact { background: #d4e6f1; color: #2980b9; }
.message-type-badge.taxi { background: #ebdef0; color: #8e44ad; }
.message-type-badge.takeoff { background: #d5f5e3; color: #2ecc71; }
.message-type-badge.landing { background: #fadbd8; color: #e74c3c; }
.message-type-badge.position { background: #fdebd0; color: #f39c12; }
.message-type-badge.emergency { background: #fadbd8; color: #c0392b; }

.no-messages {
  text-align: center;
  padding: 40px;
  color: #7f8c8d;
>>>>>>> origin/qwen-code-e1a46bfa-6c37-401a-848f-f7993735917e:frontend/src/views/ATCView.vue
}
</style>
