import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { ATCMessage } from '@/types/atc'

export const useATCStore = defineStore('atc', () => {
  // State
  const messages = ref<ATCMessage[]>([])
  const activeFrequency = ref<string | null>(null)
  const connected = ref<boolean>(false)
  const loading = ref<boolean>(false)
  const error = ref<string | null>(null)

  // Getters
  const getMessagesByFrequency = computed(() => {
    return (frequency: string) => messages.value.filter(msg => msg.frequency === frequency)
  })

  const getRecentMessages = computed(() => {
    return (limit: number = 50) => {
      return [...messages.value]
        .sort((a, b) => new Date(b.received_at).getTime() - new Date(a.received_at).getTime())
        .slice(0, limit)
    }
  })

  const getMessagesByAirport = computed(() => {
    return (airportCode: string) => messages.value.filter(msg => msg.airport_code === airportCode)
  })

  // Actions
  const setLoading = (status: boolean) => {
    loading.value = status
  }

  const setError = (message: string | null) => {
    error.value = message
  }

  const setMessages = (msgs: ATCMessage[]) => {
    messages.value = msgs
  }

  const addMessage = (msg: ATCMessage) => {
    messages.value.push(msg)
  }

  const setActiveFrequency = (frequency: string | null) => {
    activeFrequency.value = frequency
  }

  const setConnected = (status: boolean) => {
    connected.value = status
  }

  const clearMessages = () => {
    messages.value = []
  }

  const clearError = () => {
    error.value = null
  }

  // Filter messages by multiple criteria
  const filterMessages = (
    frequency?: string,
    airportCode?: string,
    messageType?: string,
    limit?: number
  ) => {
    let filtered = [...messages.value]

    if (frequency) {
      filtered = filtered.filter(msg => msg.frequency === frequency)
    }

    if (airportCode) {
      filtered = filtered.filter(msg => msg.airport_code === airportCode)
    }

    if (messageType) {
      filtered = filtered.filter(msg => msg.message_type === messageType)
    }

    if (limit) {
      filtered = filtered.slice(0, limit)
    }

    return filtered
  }

  return {
    // State
    messages,
    activeFrequency,
    connected,
    loading,
    error,

    // Getters
    getMessagesByFrequency,
    getRecentMessages,
    getMessagesByAirport,

    // Actions
    setLoading,
    setError,
    setMessages,
    addMessage,
    setActiveFrequency,
    setConnected,
    clearMessages,
    clearError,
    filterMessages
  }
})