import { ref, onMounted, onUnmounted, watch } from 'vue'
import { io, Socket } from 'socket.io-client'

interface ATCMessage {
  id: number
  frequency: string
  callsign: string | null
  message_type: string
  message_content: string
  translated_content?: string
  channel_name?: string
  airport_code: string | null
  received_at: string
  is_emergency: boolean
  priority_level: number
}

interface StreamInfo {
  stream_id: string
  frequency: string
  airport_code: string
  channel_name: string
  is_active: boolean
}

export function useATCSocket() {
  const socket = ref<Socket | null>(null)
  const messages = ref<ATCMessage[]>([])
  const isConnected = ref(false)
  const activeStreams = ref<StreamInfo[]>([])
  const subscribedChannels = ref<Set<string>>(new Set())
  
  // 按频道分组的消息
  const messagesByChannel = ref<Map<string, ATCMessage[]>>(new Map())
  
  // 连接 WebSocket
  const connect = () => {
    const apiBase = import.meta.env.VITE_API_BASE_URL || '/api/v1'
    const apiUrl = apiBase.startsWith('/') ? `${window.location.origin}${apiBase}` : apiBase
    let wsUrl = apiUrl.replace(/^http/, 'ws').replace(/\/api\/v1$/, '')
    if (wsUrl.endsWith('/')) {
      wsUrl = wsUrl.slice(0, -1)
    }

    socket.value = io(wsUrl, {
      path: '/socket.io',
      transports: ['websocket'],
      reconnection: true,
      reconnectionAttempts: 5,
      reconnectionDelay: 1000
    })
    
    // 连接到 ATC 命名空间
    const atcNamespace = socket.value.socket('/atc')
    
    // 连接成功
    atcNamespace.on('connect', () => {
      isConnected.value = true
      console.log('✅ Connected to ATC stream')
    })
    
    // 断开连接
    atcNamespace.on('disconnect', () => {
      isConnected.value = false
      console.log('❌ Disconnected from ATC stream')
    })
    
    // 接收新的 ATC 消息
    atcNamespace.on('new_atc_message', (message: ATCMessage) => {
      // 添加到总消息列表
      messages.value.unshift(message)
      
      // 保持最近 200 条消息
      if (messages.value.length > 200) {
        messages.value.pop()
      }
      
      // 按频道分组
      const channelKey = `${message.airport_code}_${message.channel_name || 'default'}`
      const channelMessages = messagesByChannel.value.get(channelKey) || []
      channelMessages.unshift(message)
      
      // 保持每个频道最近 100 条消息
      if (channelMessages.length > 100) {
        channelMessages.pop()
      }
      messagesByChannel.value.set(channelKey, channelMessages)
    })
    
    // 接收翻译后的消息
    atcNamespace.on('message_translated', (message: ATCMessage) => {
      const index = messages.value.findIndex(m => m.id === message.id)
      if (index !== -1) {
        messages.value[index] = { ...messages.value[index], ...message }
      }
      
      // 同时更新频道消息
      const channelKey = `${message.airport_code}_${message.channel_name || 'default'}`
      const channelMessages = messagesByChannel.value.get(channelKey) || []
      const channelIndex = channelMessages.findIndex(m => m.id === message.id)
      if (channelIndex !== -1) {
        channelMessages[channelIndex] = { ...channelMessages[channelIndex], ...message }
        messagesByChannel.value.set(channelKey, channelMessages)
      }
    })
    
    // 流启动事件
    atcNamespace.on('stream_started', (streamInfo: StreamInfo) => {
      console.log('📡 Stream started:', streamInfo)
      if (!activeStreams.value.find(s => s.stream_id === streamInfo.stream_id)) {
        activeStreams.value.push(streamInfo)
      }
    })
    
    // 流停止事件
    atcNamespace.on('stream_stopped', (data: { stream_id: string }) => {
      console.log('⏹️ Stream stopped:', data.stream_id)
      activeStreams.value = activeStreams.value.filter(s => s.stream_id !== data.stream_id)
    })
    
    // 流错误事件
    atcNamespace.on('stream_error', (data: { stream_id: string, error: string }) => {
      console.error('⚠️ Stream error:', data.stream_id, data.error)
    })
    
    // 消息验证事件
    atcNamespace.on('atc_message_verified', (message: ATCMessage) => {
      const index = messages.value.findIndex(m => m.id === message.id)
      if (index !== -1) {
        messages.value[index] = message
      }
    })
  }
  
  // 订阅特定频道
  const subscribeToChannel = (airportCode: string, channelName: string) => {
    if (!socket.value) return
    
    const room = `${airportCode}_${channelName}`
    socket.value.emit('subscribe_to_channel', { 
      airport_code: airportCode, 
      channel_name: channelName,
      room 
    })
    
    subscribedChannels.value.add(room)
    console.log(`📻 Subscribed to channel: ${room}`)
  }
  
  // 取消订阅频道
  const unsubscribeFromChannel = (airportCode: string, channelName: string) => {
    if (!socket.value) return
    
    const room = `${airportCode}_${channelName}`
    socket.value.emit('unsubscribe_from_channel', { room })
    
    subscribedChannels.value.delete(room)
    console.log(`🔇 Unsubscribed from channel: ${room}`)
  }
  
  // 订阅特定频率
  const subscribeToFrequency = (frequency: string) => {
    if (!socket.value) return
    
    socket.value.emit('subscribe_to_frequency', { frequency })
    console.log(`📻 Subscribed to frequency: ${frequency}`)
  }
  
  // 取消订阅频率
  const unsubscribeFromFrequency = (frequency: string) => {
    if (!socket.value) return
    
    socket.value.emit('unsubscribe_from_frequency', { frequency })
    console.log(`🔇 Unsubscribed from frequency: ${frequency}`)
  }
  
  // 获取指定频道的消息
  const getChannelMessages = (airportCode: string, channelName: string = 'default'): ATCMessage[] => {
    const channelKey = `${airportCode}_${channelName}`
    return messagesByChannel.value.get(channelKey) || []
  }
  
  // 清除消息
  const clearMessages = () => {
    messages.value = []
    messagesByChannel.value.clear()
  }
  
  // 监听频道订阅变化
  watch(subscribedChannels, (newChannels) => {
    console.log('Current subscriptions:', Array.from(newChannels))
  })
  
  // 组件挂载时连接
  onMounted(() => {
    connect()
  })
  
  // 组件卸载时断开
  onUnmounted(() => {
    if (socket.value) {
      socket.value.disconnect()
      console.log('Disconnected from ATC socket')
    }
  })
  
  return {
    socket,
    messages,
    isConnected,
    activeStreams,
    subscribedChannels,
    messagesByChannel,
    subscribeToChannel,
    unsubscribeFromChannel,
    subscribeToFrequency,
    unsubscribeFromFrequency,
    getChannelMessages,
    clearMessages
  }
}
