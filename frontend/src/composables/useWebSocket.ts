import { ref, onMounted, onUnmounted } from 'vue'

interface WebSocketOptions {
  onOpen?: (event: Event) => void
  onClose?: (event: CloseEvent) => void
  onError?: (event: Event) => void
  onMessage?: (data: any) => void
}

export const useWebSocket = (url: string, options: WebSocketOptions = {}) => {
  const ws = ref<WebSocket | null>(null)
  const isConnected = ref(false)
  const messageQueue = ref<any[]>([])

  // Connect to WebSocket
  const connect = () => {
    if (ws.value && ws.value.readyState === WebSocket.OPEN) {
      console.warn('WebSocket is already connected')
      return
    }

    ws.value = new WebSocket(url)

    ws.value.onopen = (event) => {
      isConnected.value = true
      console.log('WebSocket connected')
      
      // Process queued messages
      while (messageQueue.value.length > 0) {
        const message = messageQueue.value.shift()
        send(message)
      }
      
      if (options.onOpen) options.onOpen(event)
    }

    ws.value.onclose = (event) => {
      isConnected.value = false
      console.log('WebSocket disconnected')
      if (options.onClose) options.onClose(event)
    }

    ws.value.onerror = (event) => {
      console.error('WebSocket error:', event)
      if (options.onError) options.onError(event)
    }

    ws.value.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        if (options.onMessage) options.onMessage(data)
      } catch (e) {
        console.error('Error parsing WebSocket message:', e)
        // If JSON parsing fails, pass the raw data
        if (options.onMessage) options.onMessage(event.data)
      }
    }
  }

  // Disconnect from WebSocket
  const disconnect = () => {
    if (ws.value) {
      ws.value.close()
      ws.value = null
      isConnected.value = false
    }
  }

  // Send message via WebSocket
  const send = (data: any) => {
    if (!ws.value || ws.value.readyState !== WebSocket.OPEN) {
      // Queue the message if not connected
      messageQueue.value.push(data)
      console.log('WebSocket not connected, queuing message')
      return
    }

    try {
      const message = typeof data === 'string' ? data : JSON.stringify(data)
      ws.value.send(message)
    } catch (e) {
      console.error('Error sending WebSocket message:', e)
    }
  }

  // Reconnect WebSocket
  const reconnect = () => {
    disconnect()
    setTimeout(connect, 1000) // Retry after 1 second
  }

  // Lifecycle hooks
  onMounted(() => {
    connect()
  })

  onUnmounted(() => {
    disconnect()
  })

  return {
    ws,
    isConnected,
    connect,
    disconnect,
    send,
    reconnect
  }
}