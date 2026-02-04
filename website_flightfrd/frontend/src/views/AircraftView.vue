<template>
  <div class="aircraft-view">
    <header class="view-header">
      <h1>{{ isDetailView ? 'Aircraft Details' : 'Aircraft List' }}</h1>
      <div class="header-actions">
        <button @click="refreshData" class="btn btn-primary" :disabled="loading">
          {{ loading ? 'Loading...' : 'Refresh' }}
        </button>
        <button @click="addNewAircraft" class="btn btn-secondary">
          Add Aircraft
        </button>
      </div>
    </header>

    <!-- Aircraft List View -->
    <div v-if="!isDetailView" class="aircraft-list-container">
      <div class="filters">
        <input 
          v-model="searchQuery" 
          placeholder="Search by ICAO, registration, model..." 
          class="form-input search-input"
        />
        <select v-model="statusFilter" class="form-select">
          <option value="">All Statuses</option>
          <option value="active">Active</option>
          <option value="retired">Retired</option>
          <option value="stored">Stored</option>
        </select>
        <select v-model="sortBy" class="form-select">
          <option value="icao_code">Sort by ICAO Code</option>
          <option value="registration">Sort by Registration</option>
          <option value="model">Sort by Model</option>
          <option value="updated_at">Sort by Last Updated</option>
        </select>
      </div>

      <div class="list-stats">
        <p>{{ filteredAircraft.length }} of {{ aircraftList.length }} aircraft shown</p>
      </div>

      <div class="aircraft-grid">
        <div 
          v-for="aircraft in paginatedAircraft" 
          :key="aircraft.id" 
          class="aircraft-card"
          @click="viewAircraftDetails(aircraft.id)"
        >
          <div class="card-header">
            <h3>{{ aircraft.registration || aircraft.icao_code }}</h3>
            <span class="status-badge" :class="aircraft.status">{{ aircraft.status }}</span>
          </div>
          <div class="card-body">
            <p><strong>Model:</strong> {{ aircraft.model || 'N/A' }}</p>
            <p><strong>ICAO:</strong> {{ aircraft.icao_code }}</p>
            <p><strong>Airline:</strong> {{ aircraft.airline || 'N/A' }}</p>
            <p><strong>Operator:</strong> {{ aircraft.operator || 'N/A' }}</p>
            <p><strong>Built:</strong> {{ formatDate(aircraft.built_date) || 'N/A' }}</p>
          </div>
          <div class="card-footer">
            <small>Last updated: {{ formatDate(aircraft.updated_at) }}</small>
          </div>
        </div>
      </div>

      <div v-if="aircraftList.length === 0 && !loading" class="empty-state">
        <p>No aircraft found. {{ isAuthenticated ? 'Add one to get started!' : 'Log in to see more details.' }}</p>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="pagination">
        <button 
          @click="goToPage(currentPage - 1)" 
          :disabled="currentPage === 1"
          class="btn btn-outline"
        >
          Previous
        </button>
        <span class="page-info">Page {{ currentPage }} of {{ totalPages }}</span>
        <button 
          @click="goToPage(currentPage + 1)" 
          :disabled="currentPage === totalPages"
          class="btn btn-outline"
        >
          Next
        </button>
      </div>
    </div>

    <!-- Aircraft Detail View -->
    <div v-else class="aircraft-detail-container">
      <button @click="goBackToList" class="btn btn-back">
        ← Back to Aircraft List
      </button>

      <div v-if="currentAircraft" class="detail-content">
        <div class="detail-header">
          <h2>{{ currentAircraft.registration || currentAircraft.icao_code }}</h2>
          <span class="status-badge" :class="currentAircraft.status">{{ currentAircraft.status }}</span>
        </div>

        <div class="detail-tabs">
          <button 
            v-for="tab in detailTabs" 
            :key="tab.key"
            @click="activeTab = tab.key"
            :class="{ active: activeTab === tab.key }"
            class="tab-button"
          >
            {{ tab.label }}
          </button>
        </div>

        <div class="tab-content">
          <!-- General Info Tab -->
          <div v-if="activeTab === 'general'" class="tab-pane">
            <div class="info-grid">
              <div class="info-item">
                <label>ICAO Code</label>
                <p>{{ currentAircraft.icao_code }}</p>
              </div>
              <div class="info-item">
                <label>Registration</label>
                <p>{{ currentAircraft.registration || 'N/A' }}</p>
              </div>
              <div class="info-item">
                <label>Model</label>
                <p>{{ currentAircraft.model || 'N/A' }}</p>
              </div>
              <div class="info-item">
                <label>Type Code</label>
                <p>{{ currentAircraft.type_code || 'N/A' }}</p>
              </div>
              <div class="info-item">
                <label>Airline</label>
                <p>{{ currentAircraft.airline || 'N/A' }}</p>
              </div>
              <div class="info-item">
                <label>Operator</label>
                <p>{{ currentAircraft.operator || 'N/A' }}</p>
              </div>
              <div class="info-item">
                <label>Serial Number</label>
                <p>{{ currentAircraft.serial_number || 'N/A' }}</p>
              </div>
              <div class="info-item">
                <label>Status</label>
                <p>{{ currentAircraft.status }}</p>
              </div>
              <div class="info-item">
                <label>Built Date</label>
                <p>{{ formatDate(currentAircraft.built_date) || 'N/A' }}</p>
              </div>
              <div class="info-item">
                <label>First Flight</label>
                <p>{{ formatDate(currentAircraft.first_flight_date) || 'N/A' }}</p>
              </div>
              <div class="info-item">
                <label>Registration Date</label>
                <p>{{ formatDate(currentAircraft.registration_date) || 'N/A' }}</p>
              </div>
              <div class="info-item">
                <label>Registration Expiry</label>
                <p>{{ formatDate(currentAircraft.registration_expiry) || 'N/A' }}</p>
              </div>
            </div>
          </div>

          <!-- Flights Tab -->
          <div v-if="activeTab === 'flights'" class="tab-pane">
            <h3>Recent Flights</h3>
            <div v-if="recentFlights.length > 0" class="flights-list">
              <div 
                v-for="flight in recentFlights" 
                :key="flight.id" 
                class="flight-item"
              >
                <div class="flight-header">
                  <h4>{{ flight.flight_number || 'N/A' }} ({{ flight.callsign || 'N/A' }})</h4>
                  <span class="status-badge" :class="flight.status">{{ flight.status }}</span>
                </div>
                <div class="flight-details">
                  <p><strong>Route:</strong> {{ flight.departure_airport || 'N/A' }} → {{ flight.arrival_airport || 'N/A' }}</p>
                  <p><strong>Scheduled:</strong> {{ formatDate(flight.departure_time, true) }} - {{ formatDate(flight.arrival_time, true) }}</p>
                  <p><strong>Actual:</strong> {{ formatDate(flight.actual_departure, true) }} - {{ formatDate(flight.actual_arrival, true) }}</p>
                  <p><strong>Altitude:</strong> {{ formatAltitude(flight.altitude) }}</p>
                  <p><strong>Speed:</strong> {{ formatSpeed(flight.ground_speed) }}</p>
                </div>
              </div>
            </div>
            <div v-else class="empty-tab">
              <p>No flight records found for this aircraft.</p>
            </div>
          </div>

          <!-- Images Tab -->
          <div v-if="activeTab === 'images'" class="tab-pane">
            <h3>Aircraft Images</h3>
            <div v-if="aircraftImages.length > 0" class="images-grid">
              <div 
                v-for="(image, index) in aircraftImages" 
                :key="image.id"
                class="image-card"
                @click="openImageModal(index)"
              >
                <img :src="image.thumbnail_path || image.filepath" :alt="`Image of ${currentAircraft.model}`" />
                <p>{{ image.description || 'No description' }}</p>
              </div>
            </div>
            <div v-else class="empty-tab">
              <p>No images available for this aircraft.</p>
            </div>
          </div>

          <!-- Activity Tab -->
          <div v-if="activeTab === 'activity'" class="tab-pane">
            <h3>Recent Activity</h3>
            <div class="activity-timeline">
              <div class="activity-item">
                <div class="activity-icon">📅</div>
                <div class="activity-content">
                  <h4>Last Updated</h4>
                  <p>{{ formatDate(currentAircraft.updated_at) }}</p>
                </div>
              </div>
              <div class="activity-item">
                <div class="activity-icon">✈️</div>
                <div class="activity-content">
                  <h4>Recent Flight Activity</h4>
                  <p>{{ recentFlights.length }} flights recorded</p>
                </div>
              </div>
              <div class="activity-item">
                <div class="activity-icon">📷</div>
                <div class="activity-content">
                  <h4>Images Added</h4>
                  <p>{{ aircraftImages.length }} images available</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="detail-actions">
          <button @click="editAircraft" class="btn btn-primary">Edit Aircraft</button>
          <button @click="deleteAircraft" class="btn btn-danger">Delete Aircraft</button>
        </div>
      </div>

      <div v-else-if="loading" class="loading-state">
        <p>Loading aircraft details...</p>
      </div>

      <div v-else class="error-state">
        <p>Aircraft not found or an error occurred.</p>
        <button @click="goBackToList" class="btn btn-primary">Back to List</button>
      </div>
    </div>

    <!-- Image Modal -->
    <div v-if="showImageModal" class="modal-overlay" @click="closeImageModal">
      <div class="modal-content" @click.stop>
        <button class="modal-close" @click="closeImageModal">&times;</button>
        <img :src="currentImage?.filepath" :alt="currentImage?.description || 'Aircraft image'" />
        <div class="image-modal-info">
          <p>{{ currentImage?.description || 'No description' }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAircraftStore } from '@/stores/useAircraftStore'
import { useRoute, useRouter } from 'vue-router'
import { formatDate, formatAltitude, formatSpeed } from '@/utils/formatters'

// Props
const route = useRoute()
const router = useRouter()

// Stores
const aircraftStore = useAircraftStore()

// Reactive data
const loading = ref(false)
const searchQuery = ref('')
const statusFilter = ref('')
const sortBy = ref('icao_code')
const currentPage = ref(1)
const itemsPerPage = ref(12)
const activeTab = ref('general')

// Authentication mock
const isAuthenticated = ref(true) // This would come from your auth store

// Image modal
const showImageModal = ref(false)
const currentImageIndex = ref(0)

// Detail tabs
const detailTabs = [
  { key: 'general', label: 'General Information' },
  { key: 'flights', label: 'Flight History' },
  { key: 'images', label: 'Images' },
  { key: 'activity', label: 'Activity' }
]

// Computed properties
const isDetailView = computed(() => !!route.params.id)

const filteredAircraft = computed(() => {
  let result = [...aircraftStore.aircraftList]
  
  // Apply search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(aircraft => 
      aircraft.icao_code.toLowerCase().includes(query) ||
      (aircraft.registration && aircraft.registration.toLowerCase().includes(query)) ||
      (aircraft.model && aircraft.model.toLowerCase().includes(query)) ||
      (aircraft.airline && aircraft.airline.toLowerCase().includes(query)) ||
      (aircraft.operator && aircraft.operator.toLowerCase().includes(query))
    )
  }
  
  // Apply status filter
  if (statusFilter.value) {
    result = result.filter(aircraft => aircraft.status === statusFilter.value)
  }
  
  // Apply sorting
  result.sort((a, b) => {
    switch (sortBy.value) {
      case 'icao_code':
        return a.icao_code.localeCompare(b.icao_code)
      case 'registration':
        return (a.registration || '').localeCompare(b.registration || '')
      case 'model':
        return (a.model || '').localeCompare(b.model || '')
      case 'updated_at':
        return new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime()
      default:
        return 0
    }
  })
  
  return result
})

const totalPages = computed(() => {
  return Math.ceil(filteredAircraft.value.length / itemsPerPage.value)
})

const paginatedAircraft = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredAircraft.value.slice(start, end)
})

const currentAircraft = computed(() => {
  if (!route.params.id) return null
  const id = parseInt(route.params.id as string)
  return aircraftStore.aircraftList.find(a => a.id === id) || null
})

const recentFlights = computed(() => {
  // In a real app, this would come from an API call
  // Mock data for demonstration
  if (!currentAircraft.value) return []
  
  return [
    { 
      id: 1, 
      flight_number: 'AA123', 
      callsign: 'AAL123', 
      status: 'landed', 
      departure_airport: 'KJFK', 
      arrival_airport: 'KLAX',
      departure_time: '2023-05-15T08:00:00Z',
      arrival_time: '2023-05-15T11:30:00Z',
      actual_departure: '2023-05-15T08:05:00Z',
      actual_arrival: '2023-05-15T11:25:00Z',
      altitude: 35000,
      ground_speed: 450
    },
    { 
      id: 2, 
      flight_number: 'AA456', 
      callsign: 'AAL456', 
      status: 'landed', 
      departure_airport: 'KLAX', 
      arrival_airport: 'KMIA',
      departure_time: '2023-05-10T14:00:00Z',
      arrival_time: '2023-05-10T19:30:00Z',
      actual_departure: '2023-05-10T14:05:00Z',
      actual_arrival: '2023-05-10T19:25:00Z',
      altitude: 37000,
      ground_speed: 470
    }
  ]
})

const aircraftImages = computed(() => {
  // In a real app, this would come from an API call
  // Mock data for demonstration
  if (!currentAircraft.value) return []
  
  return [
    { 
      id: 1, 
      filepath: '/demo-images/aircraft-exterior.jpg', 
      thumbnail_path: '/demo-images/aircraft-exterior-thumb.jpg',
      description: 'Exterior view of the aircraft' 
    },
    { 
      id: 2, 
      filepath: '/demo-images/cockpit.jpg', 
      thumbnail_path: '/demo-images/cockpit-thumb.jpg', 
      description: 'Cockpit interior' 
    },
    { 
      id: 3, 
      filepath: '/demo-images/cabin.jpg', 
      thumbnail_path: '/demo-images/cabin-thumb.jpg', 
      description: 'Passenger cabin' 
    }
  ]
})

const currentImage = computed(() => {
  if (aircraftImages.value.length === 0) return null
  return aircraftImages.value[currentImageIndex.value]
})

// Methods
const refreshData = async () => {
  loading.value = true
  try {
    // In a real app, this would fetch data from the API
    // await aircraftStore.fetchAircraftList()
  } catch (error) {
    console.error('Error refreshing aircraft data:', error)
  } finally {
    loading.value = false
  }
}

const addNewAircraft = () => {
  // Navigate to add aircraft form
  router.push('/aircraft/new')
}

const viewAircraftDetails = (id: number) => {
  router.push(`/aircraft/${id}`)
}

const goBackToList = () => {
  router.push('/aircraft')
}

const goToPage = (page: number) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    // Scroll to top when changing pages
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const editAircraft = () => {
  if (currentAircraft.value) {
    router.push(`/aircraft/${currentAircraft.value.id}/edit`)
  }
}

const deleteAircraft = async () => {
  if (currentAircraft.value && confirm(`Are you sure you want to delete aircraft ${currentAircraft.value.icao_code}?`)) {
    try {
      // In a real app, this would call the API to delete the aircraft
      console.log(`Deleting aircraft ${currentAircraft.value.id}`)
      // await aircraftApi.deleteAircraft(currentAircraft.value.id)
      goBackToList()
    } catch (error) {
      console.error('Error deleting aircraft:', error)
    }
  }
}

const openImageModal = (index: number) => {
  currentImageIndex.value = index
  showImageModal.value = true
}

const closeImageModal = () => {
  showImageModal.value = false
}

// Lifecycle
onMounted(async () => {
  loading.value = true
  try {
    // In a real app, this would fetch data from the API
    // await aircraftStore.fetchAircraftList()
    
    // Mock data for demonstration
    aircraftStore.setAircraftList([
      {
        id: 1,
        icao_code: 'A2CDEF',
        registration: 'N123AB',
        airline: 'Example Airlines',
        model: 'Boeing 737-800',
        type_code: '738',
        serial_number: '29012',
        operator: 'Example Airlines',
        built_date: '2018-05-15',
        status: 'active',
        first_flight_date: '2018-06-20',
        registration_date: '2018-07-01',
        registration_expiry: '2028-07-01',
        created_at: '2023-01-01T00:00:00Z',
        updated_at: '2023-05-15T10:30:00Z'
      },
      {
        id: 2,
        icao_code: 'B3F123',
        registration: 'N456CD',
        airline: 'Another Airlines',
        model: 'Airbus A320',
        type_code: '320',
        serial_number: '12345',
        operator: 'Another Airlines',
        built_date: '2019-03-10',
        status: 'active',
        first_flight_date: '2019-04-15',
        registration_date: '2019-05-01',
        registration_expiry: '2029-05-01',
        created_at: '2023-01-01T00:00:00Z',
        updated_at: '2023-05-14T09:15:00Z'
      }
    ])
  } catch (error) {
    console.error('Error loading aircraft data:', error)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.aircraft-view {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.view-header h1 {
  margin: 0;
  color: #2c3e50;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.filters {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.search-input {
  flex: 1;
  min-width: 250px;
}

.list-stats {
  margin-bottom: 15px;
  color: #7f8c8d;
}

.aircraft-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.aircraft-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.aircraft-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.card-header h3 {
  margin: 0;
  color: #2c3e50;
}

.card-body p {
  margin: 5px 0;
  font-size: 0.9rem;
}

.card-footer {
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid #eee;
  font-size: 0.8rem;
  color: #7f8c8d;
}

.status-badge {
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

.status-badge.retired {
  background-color: #95a5a6;
  color: white;
}

.status-badge.stored {
  background-color: #f39c12;
  color: white;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
  margin-top: 20px;
}

.page-info {
  color: #7f8c8d;
}

.detail-content {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.detail-header h2 {
  margin: 0;
  color: #2c3e50;
}

.detail-tabs {
  display: flex;
  border-bottom: 1px solid #ddd;
  margin-bottom: 20px;
}

.tab-button {
  padding: 10px 20px;
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 1rem;
  color: #7f8c8d;
  border-bottom: 2px solid transparent;
}

.tab-button.active {
  color: #3498db;
  border-bottom: 2px solid #3498db;
}

.tab-content {
  min-height: 400px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 15px;
}

.info-item {
  margin-bottom: 15px;
}

.info-item label {
  display: block;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 5px;
}

.info-item p {
  margin: 0;
  color: #34495e;
}

.flights-list {
  margin-top: 15px;
}

.flight-item {
  border: 1px solid #eee;
  border-radius: 6px;
  padding: 15px;
  margin-bottom: 15px;
}

.flight-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.flight-header h4 {
  margin: 0;
  color: #2c3e50;
}

.flight-details p {
  margin: 5px 0;
  font-size: 0.9rem;
}

.images-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 15px;
  margin-top: 15px;
}

.image-card {
  cursor: pointer;
  text-align: center;
}

.image-card img {
  width: 100%;
  height: 150px;
  object-fit: cover;
  border-radius: 4px;
  margin-bottom: 5px;
}

.activity-timeline {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.activity-item {
  display: flex;
  gap: 15px;
  align-items: flex-start;
}

.activity-icon {
  font-size: 1.5rem;
  min-width: 40px;
  text-align: center;
}

.activity-content h4 {
  margin: 0 0 5px 0;
  color: #2c3e50;
}

.activity-content p {
  margin: 0;
  color: #7f8c8d;
}

.detail-actions {
  display: flex;
  gap: 10px;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.loading-state, .error-state, .empty-state {
  text-align: center;
  padding: 40px;
  color: #7f8c8d;
}

.empty-tab {
  padding: 20px;
  text-align: center;
  color: #7f8c8d;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  position: relative;
  max-width: 90%;
  max-height: 90%;
}

.modal-close {
  position: absolute;
  top: 10px;
  right: 10px;
  background: white;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content img {
  max-width: 100%;
  max-height: 80vh;
  object-fit: contain;
}

.image-modal-info {
  margin-top: 10px;
  text-align: center;
  color: white;
}

/* Responsive design */
@media (max-width: 768px) {
  .aircraft-grid {
    grid-template-columns: 1fr;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .view-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .filters {
    flex-direction: column;
  }
  
  .search-input {
    min-width: 100%;
  }
  
  .detail-tabs {
    overflow-x: auto;
  }
}
</style>