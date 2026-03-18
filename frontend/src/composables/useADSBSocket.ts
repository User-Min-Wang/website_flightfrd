import { ref, watch } from 'vue'
import { useWebSocket } from './useWebSocket'
import type { Aircraft } from '@/types/aircraft'

export const useADSBSocket = (onUpdate?: (aircraft: Aircraft[]) => void) => {
  // Get WebSocket connection
  const {
    ws,
    isConnected,
    connect,
    disconnect,
    send,
    reconnect
  } = useWebSocket('/ws/adsb', {
    onMessage: (data) => {
      // Handle incoming ADS-B data
      if (data.type === 'aircraft_update') {
        // Process aircraft data
        const aircraftArray: Aircraft[] = Array.isArray(data.payload) ? data.payload : [data.payload]
        
        // Update local state if needed
        if (onUpdate) {
          onUpdate(aircraftArray)
        }
      } else if (data.type === 'connection_status') {
        console.log('ADS-B connection status:', data.status)
      } else {
        console.warn('Unknown message type from ADS-B socket:', data.type)
      }
    },
    onOpen: (event) => {
      console.log('ADS-B WebSocket connected:', event)
    },
    onClose: (event) => {
      console.log('ADS-B WebSocket disconnected:', event)
    },
    onError: (event) => {
      console.error('ADS-B WebSocket error:', event)
    }
  })

  // Refs for tracking aircraft data
  const aircraftData = ref<Aircraft[]>([])
  const lastUpdate = ref<Date | null>(null)

  // Function to subscribe to specific aircraft
  const subscribeToAircraft = (icaoCodes: string[]) => {
    if (isConnected.value) {
      send({
        type: 'subscribe',
        icao_codes: icaoCodes
      })
    } else {
      console.warn('Cannot subscribe - ADS-B WebSocket not connected')
    }
  }

  // Function to unsubscribe from specific aircraft
  const unsubscribeFromAircraft = (icaoCodes: string[]) => {
    if (isConnected.value) {
      send({
        type: 'unsubscribe',
        icao_codes: icaoCodes
      })
    } else {
      console.warn('Cannot unsubscribe - ADS-B WebSocket not connected')
    }
  }

  // Function to get all tracked aircraft
  const getAllAircraft = (): Aircraft[] => {
    return aircraftData.value
  }

  // Function to get specific aircraft by ICAO code
  const getAircraftByICAO = (icao: string): Aircraft | undefined => {
    return aircraftData.value.find(a => a.icao_code === icao)
  }

  // Watch for changes in aircraft data and trigger callback
  watch(aircraftData, (newData) => {
    if (onUpdate && newData.length > 0) {
      onUpdate(newData)
    }
  })

  // Function to request current aircraft data snapshot
  const requestSnapshot = () => {
    if (isConnected.value) {
      send({
        type: 'request_snapshot'
      })
    } else {
      console.warn('Cannot request snapshot - ADS-B WebSocket not connected')
    }
  }

  // Function to start receiving all aircraft data
  const startTrackingAll = () => {
    if (isConnected.value) {
      send({
        type: 'start_tracking_all'
      })
    } else {
      console.warn('Cannot start tracking - ADS-B WebSocket not connected')
    }
  }

  // Function to stop receiving all aircraft data
  const stopTrackingAll = () => {
    if (isConnected.value) {
      send({
        type: 'stop_tracking_all'
      })
    } else {
      console.warn('Cannot stop tracking - ADS-B WebSocket not connected')
    }
  }

  return {
    // WebSocket connection
    ws,
    isConnected,
    connect,
    disconnect,
    reconnect,
    
    // Aircraft data
    aircraftData,
    lastUpdate,
    
    // Subscription methods
    subscribeToAircraft,
    unsubscribeFromAircraft,
    getAllAircraft,
    getAircraftByICAO,
    
    // Control methods
    requestSnapshot,
    startTrackingAll,
    stopTrackingAll
  }
}