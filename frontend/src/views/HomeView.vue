<template>
  <div class="home">
    <div class="hero-section">
      <h1>Aircraft Tracking Dashboard</h1>
      <p>Real-time monitoring of aircraft movements and air traffic control communications</p>
    </div>

    <div class="dashboard-grid">
      <!-- Map Section -->
      <section class="map-section">
        <div class="section-header">
          <h2>Live Aircraft Map</h2>
          <div class="controls">
            <button @click="toggleLabels" class="btn btn-sm">
              {{ showLabels ? 'Hide Labels' : 'Show Labels' }}
            </button>
            <button @click="toggleTrails" class="btn btn-sm">
              {{ showTrails ? 'Hide Trails' : 'Show Trails' }}
            </button>
            <select v-model="selectedMapLayer" @change="changeMapLayer" class="form-select">
              <option value="osm">OpenStreetMap</option>
              <option value="satellite">Satellite</option>
              <option value="terrain">Terrain</option>
            </select>
          </div>
        </div>
        <div id="map-container" class="map-container">
          <!-- Map will be rendered here -->
          <div class="map-placeholder">
            <p>Interactive map showing live aircraft positions</p>
          </div>
        </div>
      </section>

      <!-- Aircraft List Section -->
      <section class="aircraft-list-section">
        <div class="section-header">
          <h2>Active Aircraft</h2>
          <div class="controls">
            <input 
              v-model="searchQuery" 
              placeholder="Search aircraft..." 
              class="form-input"
            />
            <select v-model="selectedStatus" class="form-select">
              <option value="">All Statuses</option>
              <option value="active">Active</option>
              <option value="scheduled">Scheduled</option>
              <option value="landed">Landed</option>
            </select>
          </div>
        </div>
        <div class="aircraft-list">
          <div 
            v-for="aircraft in filteredAircraft" 
            :key="aircraft.id" 
            class="aircraft-card"
            @click="selectAircraft(aircraft)"
          >
            <div class="aircraft-info">
              <h3>{{ aircraft.callsign || 'N/A' }}</h3>
              <p class="icao-code">{{ aircraft.icao_code }}</p>
              <p class="model">{{ aircraft.model || 'N/A' }}</p>
            </div>
            <div class="aircraft-status">
              <span class="status-badge" :class="aircraft.status">{{ aircraft.status }}</span>
              <p class="altitude">{{ formatAltitude(aircraft.altitude) }}</p>
            </div>
          </div>
          <div v-if="filteredAircraft.length === 0" class="no-results">
            <p>No aircraft found</p>
          </div>
        </div>
      </section>

      <!-- ATC Communications Section -->
      <section class="atc-section">
        <div class="section-header">
          <h2>ATC Communications</h2>
          <div class="controls">
            <select v-model="selectedFrequency" class="form-select">
              <option value="">All Frequencies</option>
              <option v-for="freq in frequencies" :key="freq" :value="freq">{{ freq }}</option>
            </select>
            <button @click="toggleATCStream" class="btn btn-sm">
              {{ atcStreamActive ? 'Pause Stream' : 'Resume Stream' }}
            </button>
          </div>
        </div>
        <div class="atc-messages">
          <div 
            v-for="message in displayedMessages" 
            :key="message.id" 
            class="atc-message"
          >
            <div class="message-header">
              <span class="frequency">{{ formatFrequency(message.frequency) }}</span>
              <span class="callsign">{{ message.callsign || 'N/A' }}</span>
              <span class="timestamp">{{ formatDate(message.received_at) }}</span>
            </div>
            <div class="message-content">
              {{ message.message_content }}
            </div>
            <div class="message-type" :class="message.message_type">
              {{ message.message_type }}
            </div>
          </div>
          <div v-if="displayedMessages.length === 0" class="no-results">
            <p>No ATC messages available</p>
          </div>
        </div>
      </section>

      <!-- Stats Section -->
      <section class="stats-section">
        <div class="stat-card">
          <h3>Total Aircraft</h3>
          <p class="stat-value">{{ totalAircraft }}</p>
        </div>
        <div class="stat-card">
          <h3>Active Flights</h3>
          <p class="stat-value">{{ activeFlights }}</p>
        </div>
        <div class="stat-card">
          <h3>ATC Messages (Last Hour)</h3>
          <p class="stat-value">{{ atcMessagesLastHour }}</p>
        </div>
        <div class="stat-card">
          <h3>Connected Users</h3>
          <p class="stat-value">{{ connectedUsers }}</p>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useMapStore } from '@/stores/useMapStore'
import { useAircraftStore } from '@/stores/useAircraftStore'
import { useATCStore } from '@/stores/useATCStore'
import { useSettingsStore } from '@/stores/useSettingsStore'
import { formatAltitude, formatFrequency, formatDate } from '@/utils/formatters'

// Stores
const mapStore = useMapStore()
const aircraftStore = useAircraftStore()
const atcStore = useATCStore()
const settingsStore = useSettingsStore()

// Reactive data
const showLabels = ref(true)
const showTrails = ref(false)
const selectedMapLayer = ref('osm')
const searchQuery = ref('')
const selectedStatus = ref('')
const selectedFrequency = ref('')
const atcStreamActive = ref(true)
const connectedUsers = ref(12)

// Mock data - these would come from the stores in a real implementation
const totalAircraft = ref(142)
const activeFlights = ref(86)
const atcMessagesLastHour = ref(342)

// Mock aircraft data
const mockAircraft = [
  { id: 1, icao_code: 'A2CDEF', callsign: 'AAL123', model: 'Boeing 737-800', status: 'active', altitude: 35000 },
  { id: 2, icao_code: 'B3F123', callsign: 'UAL456', model: 'Airbus A320', status: 'active', altitude: 28000 },
  { id: 3, icao_code: 'C4D5E6', callsign: 'DAL789', model: 'Boeing 777-300ER', status: 'scheduled', altitude: null },
  { id: 4, icao_code: 'D5E6F7', callsign: 'SWA101', model: 'Boeing 737-700', status: 'landed', altitude: 0 },
  { id: 5, icao_code: 'E6F7G8', callsign: 'ASA202', model: 'Boeing 737-900ER', status: 'active', altitude: 12000 }
]

// Mock ATC messages
const mockATCMessages = [
  { id: 1, frequency: '118.700', callsign: 'AAL123', message_content: 'Requesting taxi to runway 24L', message_type: 'taxi', received_at: '2023-05-15T10:30:00Z' },
  { id: 2, frequency: '120.900', callsign: 'UAL456', message_content: 'Cleared for takeoff runway 24L', message_type: 'takeoff', received_at: '2023-05-15T10:28:00Z' },
  { id: 3, frequency: '119.100', callsign: 'DAL789', message_content: 'Descending to 10,000 feet', message_type: 'position', received_at: '2023-05-15T10:25:00Z' },
  { id: 4, frequency: '121.900', callsign: 'SWA101', message_content: 'Emergency frequency monitor', message_type: 'emergency', received_at: '2023-05-15T10:20:00Z' },
  { id: 5, frequency: '118.100', callsign: 'ASA202', message_content: 'Requesting ILS approach runway 24R', message_type: 'landing', received_at: '2023-05-15T10:18:00Z' }
]

const frequencies = ['118.100', '118.700', '119.100', '120.900', '121.900']

// Computed properties
const filteredAircraft = computed(() => {
  return mockAircraft.filter(aircraft => {
    const matchesSearch = aircraft.icao_code.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                         (aircraft.callsign && aircraft.callsign.toLowerCase().includes(searchQuery.value.toLowerCase())) ||
                         (aircraft.model && aircraft.model.toLowerCase().includes(searchQuery.value.toLowerCase()))
    const matchesStatus = !selectedStatus.value || aircraft.status === selectedStatus.value
    return matchesSearch && matchesStatus
  })
})

const displayedMessages = computed(() => {
  if (!atcStreamActive.value) return []
  
  return mockATCMessages.filter(message => {
    return !selectedFrequency.value || message.frequency === selectedFrequency.value
  }).slice(0, 10) // Show only the latest 10 messages
})

// Methods
const toggleLabels = () => {
  showLabels.value = !showLabels.value
  // In a real app, this would update the map settings
}

const toggleTrails = () => {
  showTrails.value = !showTrails.value
  // In a real app, this would update the map settings
}

const changeMapLayer = () => {
  // In a real app, this would change the map tile layer
  console.log(`Changing map layer to: ${selectedMapLayer.value}`)
}

const selectAircraft = (aircraft: any) => {
  console.log(`Selected aircraft: ${aircraft.icao_code}`)
  // In a real app, this would highlight the aircraft on the map
  // and potentially show more details
}

const toggleATCStream = () => {
  atcStreamActive.value = !atcStreamActive.value
}

// Lifecycle hook
onMounted(() => {
  // Initialize settings from store
  showLabels.value = settingsStore.preferences.showLabels
  showTrails.value = settingsStore.preferences.showTrails
  selectedMapLayer.value = settingsStore.preferences.mapLayer
})
</script>

<style scoped>
.home {
  padding: 20px;
  font-family: Arial, sans-serif;
}

.hero-section {
  text-align: center;
  margin-bottom: 30px;
}

.hero-section h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
  color: #2c3e50;
}

.hero-section p {
  font-size: 1.2rem;
  color: #7f8c8d;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  grid-template-rows: auto auto auto;
  gap: 20px;
}

.map-section {
  grid-column: 1;
  grid-row: 1;
}

.aircraft-list-section {
  grid-column: 2;
  grid-row: 1;
}

.atc-section {
  grid-column: 1 / span 2;
  grid-row: 2;
}

.stats-section {
  grid-column: 1 / span 2;
  grid-row: 3;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.section-header h2 {
  margin: 0;
  color: #2c3e50;
}

.controls {
  display: flex;
  gap: 10px;
  align-items: center;
}

.map-container {
  height: 500px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  background-color: #ecf0f1;
}

.map-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #7f8c8d;
}

.aircraft-list {
  max-height: 500px;
  overflow-y: auto;
}

.aircraft-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  border-bottom: 1px solid #eee;
  cursor: pointer;
  transition: background-color 0.2s;
}

.aircraft-card:hover {
  background-color: #f8f9fa;
}

.aircraft-info h3 {
  margin: 0 0 5px 0;
  color: #2c3e50;
}

.icao-code {
  font-family: monospace;
  font-size: 0.9rem;
  color: #7f8c8d;
  margin: 0;
}

.model {
  font-size: 0.85rem;
  color: #95a5a6;
  margin: 0;
}

.aircraft-status {
  text-align: right;
}

.status-badge {
  display: inline-block;
  padding: 3px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
  text-transform: uppercase;
}

.status-badge.active {
  background-color: #2ecc71;
  color: white;
}

.status-badge.scheduled {
  background-color: #3498db;
  color: white;
}

.status-badge.landed {
  background-color: #95a5a6;
  color: white;
}

.altitude {
  font-weight: bold;
  color: #2c3e50;
  margin: 5px 0 0 0;
}

.atc-messages {
  max-height: 300px;
  overflow-y: auto;
}

.atc-message {
  padding: 10px;
  border-bottom: 1px solid #eee;
  background-color: #fff;
}

.message-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
  font-size: 0.9rem;
}

.frequency {
  font-weight: bold;
  color: #2980b9;
}

.callsign {
  color: #2c3e50;
}

.timestamp {
  color: #7f8c8d;
}

.message-content {
  margin-bottom: 5px;
  color: #34495e;
}

.message-type {
  font-size: 0.8rem;
  font-weight: bold;
  text-transform: uppercase;
}

.message-type.clearance { color: #27ae60; }
.message-type.contact { color: #2980b9; }
.message-type.taxi { color: #8e44ad; }
.message-type.takeoff { color: #2ecc71; }
.message-type.landing { color: #e74c3c; }
.message-type.position { color: #f39c12; }
.message-type.emergency { color: #c0392b; }

.stat-card {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.stat-card h3 {
  margin-top: 0;
  color: #7f8c8d;
  font-size: 0.9rem;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: #2c3e50;
  margin: 0;
}

.no-results {
  text-align: center;
  padding: 20px;
  color: #7f8c8d;
}

/* Form elements */
.form-input, .form-select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
}

.form-input:focus, .form-select:focus {
  outline: none;
  border-color: #3498db;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  background-color: #3498db;
  color: white;
  cursor: pointer;
  font-size: 0.9rem;
}

.btn:hover {
  background-color: #2980b9;
}

.btn-sm {
  padding: 5px 10px;
  font-size: 0.85rem;
}
</style>