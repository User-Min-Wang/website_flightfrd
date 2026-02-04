import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Aircraft } from '@/types/aircraft'

export const useAircraftStore = defineStore('aircraft', () => {
  // State
  const aircraftList = ref<Aircraft[]>([])
  const currentAircraft = ref<Aircraft | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const getAllAircraft = computed(() => aircraftList.value)
  
  const getAircraftById = computed(() => {
    return (id: number) => aircraftList.value.find(aircraft => aircraft.id === id)
  })

  const getAircraftByICAO = computed(() => {
    return (icao: string) => aircraftList.value.find(aircraft => aircraft.icao_code === icao)
  })

  // Actions
  const setLoading = (status: boolean) => {
    loading.value = status
  }

  const setError = (message: string | null) => {
    error.value = message
  }

  const setAircraftList = (aircraft: Aircraft[]) => {
    aircraftList.value = aircraft
  }

  const setCurrentAircraft = (aircraft: Aircraft | null) => {
    currentAircraft.value = aircraft
  }

  const addAircraft = (aircraft: Aircraft) => {
    aircraftList.value.push(aircraft)
  }

  const updateAircraft = (updatedAircraft: Aircraft) => {
    const index = aircraftList.value.findIndex(a => a.id === updatedAircraft.id)
    if (index !== -1) {
      aircraftList.value[index] = updatedAircraft
    }
  }

  const removeAircraft = (id: number) => {
    aircraftList.value = aircraftList.value.filter(a => a.id !== id)
  }

  // Clear error
  const clearError = () => {
    error.value = null
  }

  return {
    // State
    aircraftList,
    currentAircraft,
    loading,
    error,

    // Getters
    getAllAircraft,
    getAircraftById,
    getAircraftByICAO,

    // Actions
    setLoading,
    setError,
    setAircraftList,
    setCurrentAircraft,
    addAircraft,
    updateAircraft,
    removeAircraft,
    clearError
  }
})