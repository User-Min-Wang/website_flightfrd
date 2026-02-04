import apiClient from '.'
import type { Aircraft, Flight, AircraftSearchParams } from '@/types/aircraft'

export const aircraftApi = {
  /**
   * Get a list of aircraft with optional pagination and search
   */
  getAircraftList: async (params?: AircraftSearchParams) => {
    const response = await apiClient.get<{ aircraft: Aircraft[], pagination: any }>('/aircraft', {
      params: {
        page: 1,
        per_page: 20,
        ...params
      }
    })
    return response.data
  },

  /**
   * Get detailed information about a specific aircraft
   */
  getAircraftDetail: async (id: number) => {
    const response = await apiClient.get<Aircraft>(`/aircraft/${id}`)
    return response.data
  },

  /**
   * Get flights for a specific aircraft
   */
  getAircraftFlights: async (id: number, params?: { page?: number; per_page?: number }) => {
    const response = await apiClient.get<{
      flights: Flight[]
      pagination: any
    }>(`/aircraft/${id}/flights`, {
      params: {
        page: 1,
        per_page: 20,
        ...params
      }
    })
    return response.data
  },

  /**
   * Create a new aircraft record
   */
  createAircraft: async (data: Omit<Aircraft, 'id' | 'created_at' | 'updated_at'>) => {
    const response = await apiClient.post<Aircraft>('/aircraft', data)
    return response.data
  },

  /**
   * Update an existing aircraft record
   */
  updateAircraft: async (id: number, data: Partial<Aircraft>) => {
    const response = await apiClient.put<Aircraft>(`/aircraft/${id}`, data)
    return response.data
  },

  /**
   * Delete an aircraft record
   */
  deleteAircraft: async (id: number) => {
    const response = await apiClient.delete(`/aircraft/${id}`)
    return response.data
  },

  /**
   * Fetch live data for a specific aircraft from ADS-B
   */
  fetchAircraftData: async (icaoCode: string) => {
    const response = await apiClient.post<any>(`/aircraft/${icaoCode}/fetch`)
    return response.data
  }
}