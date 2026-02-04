import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Aircraft } from '@/types/aircraft'

export interface MapViewState {
  center: [number, number];  // [lat, lng]
  zoom: number;
  bounds: [[number, number], [number, number]] | null; // [[south, west], [north, east]]
}

export interface AircraftMarker {
  id: number;
  icao_code: string;
  latitude: number;
  longitude: number;
  altitude: number | null;
  ground_speed: number | null;
  heading: number | null;
  callsign: string | null;
  registration: string | null;
  model: string | null;
  last_seen: string | null;
}

export const useMapStore = defineStore('map', () => {
  // State
  const mapViewState = ref<MapViewState>({
    center: [39.8283, -98.5795], // Center of US
    zoom: 4,
    bounds: null
  })
  
  const aircraftMarkers = ref<AircraftMarker[]>([])
  const selectedAircraft = ref<AircraftMarker | null>(null)
  const mapReady = ref<boolean>(false)
  const loading = ref<boolean>(false)
  const error = ref<string | null>(null)

  // Getters
  const getCurrentCenter = computed(() => mapViewState.value.center)
  
  const getCurrentZoom = computed(() => mapViewState.value.zoom)
  
  const getVisibleAircraft = computed(() => {
    // Filter aircraft based on map bounds if available
    if (!mapViewState.value.bounds) {
      return aircraftMarkers.value
    }
    
    const [[south, west], [north, east]] = mapViewState.value.bounds
    
    return aircraftMarkers.value.filter(aircraft => {
      return (
        aircraft.latitude >= south &&
        aircraft.latitude <= north &&
        aircraft.longitude >= west &&
        aircraft.longitude <= east
      )
    })
  })

  const getAircraftCount = computed(() => aircraftMarkers.value.length)

  // Actions
  const setMapViewState = (state: Partial<MapViewState>) => {
    mapViewState.value = { ...mapViewState.value, ...state }
  }

  const setCenter = (center: [number, number]) => {
    mapViewState.value.center = center
  }

  const setZoom = (zoom: number) => {
    mapViewState.value.zoom = zoom
  }

  const setBounds = (bounds: [[number, number], [number, number]] | null) => {
    mapViewState.value.bounds = bounds
  }

  const setAircraftMarkers = (markers: AircraftMarker[]) => {
    aircraftMarkers.value = markers
  }

  const addAircraftMarker = (marker: AircraftMarker) => {
    // Check if aircraft already exists, update if so
    const existingIndex = aircraftMarkers.value.findIndex(m => m.id === marker.id)
    if (existingIndex !== -1) {
      aircraftMarkers.value[existingIndex] = marker
    } else {
      aircraftMarkers.value.push(marker)
    }
  }

  const removeAircraftMarker = (id: number) => {
    aircraftMarkers.value = aircraftMarkers.value.filter(marker => marker.id !== id)
  }

  const setSelectedAircraft = (aircraft: AircraftMarker | null) => {
    selectedAircraft.value = aircraft
  }

  const setMapReady = (ready: boolean) => {
    mapReady.value = ready
  }

  const setLoading = (status: boolean) => {
    loading.value = status
  }

  const setError = (message: string | null) => {
    error.value = message
  }

  const clearError = () => {
    error.value = null
  }

  // Action to update multiple aircraft at once
  const updateAircraftPositions = (aircraftList: Aircraft[]) => {
    const updatedMarkers = aircraftList.map(aircraft => ({
      id: aircraft.id,
      icao_code: aircraft.icao_code,
      latitude: aircraft.latitude || 0,
      longitude: aircraft.longitude || 0,
      altitude: aircraft.altitude || null,
      ground_speed: aircraft.ground_speed || null,
      heading: aircraft.heading || null,
      callsign: aircraft.callsign || null,
      registration: aircraft.registration || null,
      model: aircraft.model || null,
      last_seen: aircraft.updated_at || null
    }))
    
    setAircraftMarkers(updatedMarkers)
  }

  return {
    // State
    mapViewState,
    aircraftMarkers,
    selectedAircraft,
    mapReady,
    loading,
    error,

    // Getters
    getCurrentCenter,
    getCurrentZoom,
    getVisibleAircraft,
    getAircraftCount,

    // Actions
    setMapViewState,
    setCenter,
    setZoom,
    setBounds,
    setAircraftMarkers,
    addAircraftMarker,
    removeAircraftMarker,
    setSelectedAircraft,
    setMapReady,
    setLoading,
    setError,
    clearError,
    updateAircraftPositions
  }
})