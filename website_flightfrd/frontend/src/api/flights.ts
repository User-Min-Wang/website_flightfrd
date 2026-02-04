import apiClient from '.'
import type { Flight } from '@/types/aircraft'

export const flightsApi = {
  /**
   * Get a list of flights with optional pagination and filtering
   */
  getFlightsList: async (params?: {
    page?: number
    per_page?: number
    status?: string
    aircraft_id?: number
    departure_airport?: string
    arrival_airport?: string
  }) => {
    const response = await apiClient.get<{ flights: Flight[], pagination: any }>('/flights', {
      params: {
        page: 1,
        per_page: 20,
        ...params
      }
    })
    return response.data
  },

  /**
   * Get detailed information about a specific flight
   */
  getFlightDetail: async (id: number) => {
    const response = await apiClient.get<Flight>(`/flights/${id}`)
    return response.data
  },

  /**
   * Create a new flight record
   */
  createFlight: async (data: Omit<Flight, 'id' | 'created_at' | 'updated_at'>) => {
    const response = await apiClient.post<Flight>('/flights', data)
    return response.data
  },

  /**
   * Update an existing flight record
   */
  updateFlight: async (id: number, data: Partial<Flight>) => {
    const response = await apiClient.put<Flight>(`/flights/${id}`, data)
    return response.data
  },

  /**
   * Delete a flight record
   */
  deleteFlight: async (id: number) => {
    const response = await apiClient.delete(`/flights/${id}`)
    return response.data
  },

  /**
   * Search for flights based on various criteria
   */
  searchFlights: async (params: {
    departure_airport?: string
    arrival_airport?: string
    date?: string  // Format: YYYY-MM-DD
    callsign?: string
    limit?: number
  }) => {
    const response = await apiClient.get<{ flights: Flight[], count: number }>('/flights/search', {
      params
    })
    return response.data
  },

  /**
   * Get all currently active flights
   */
  getActiveFlights: async () => {
    const response = await apiClient.get<{ flights: Flight[], count: number }>('/flights/active')
    return response.data
  },

  /**
   * Get position history for a flight identified by ICAO code
   */
  getFlightPositions: async (icaoCode: string) => {
    const response = await apiClient.get<{ 
      flight_id: number, 
      positions: any[], 
      count: number 
    }>(`/flights/${icaoCode}/positions`)
    return response.data
  }
}