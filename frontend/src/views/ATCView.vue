<template>
  <div class="atc-page">
    <div class="atc-header">
      <h1>🎧 ATC 直播 - 空中交通管制通信</h1>
      <div class="status-indicator" :class="{ online: isConnected }">
        {{ isConnected ? '🔴 直播中' : '⚪ 未连接' }}
      </div>
    </div>

    <!-- 频道选择和控制 -->
    <div class="controls-section">
      <div class="control-group">
        <label>选择机场</label>
        <select v-model="selectedAirport" class="form-select">
          <option value="">-- 选择机场 --</option>
          <option v-for="airport in airports" :key="airport.code" :value="airport.code">
            {{ airport.code }} - {{ airport.name }}
          </option>
        </select>
      </div>

      <div class="control-group" v-if="selectedAirport">
        <label>选择频道</label>
        <div class="channel-buttons">
          <button 
            v-for="channel in availableChannels" 
            :key="channel.name"
            @click="toggleChannel(channel.name)"
            class="channel-btn"
            :class="{ 
              active: isChannelSubscribed(channel.name),
              emergency: channel.type === 'emergency'
            }"
          >
            {{ channel.name }}
            <span class="freq">{{ channel.frequency }} MHz</span>
          </button>
        </div>
      </div>

      <div class="control-group">
        <label>显示选项</label>
        <div class="toggle-options">
          <label class="toggle-label">
            <input type="checkbox" v-model="showTranslation" />
            显示中文翻译
          </label>
          <label class="toggle-label">
            <input type="checkbox" v-model="showAllChannels" />
            显示所有频道
          </label>
        </div>
      </div>
    </div>

    <!-- 活动流状态 -->
    <div v-if="activeStreams.length > 0" class="active-streams">
      <h3>📡 活动音频流</h3>
      <div class="stream-list">
        <div 
          v-for="stream in activeStreams" 
          :key="stream.stream_id"
          class="stream-item"
        >
          <span class="stream-status">🔴</span>
          <span class="stream-info">
            {{ stream.airport_code }} - {{ stream.channel_name }} 
            ({{ stream.frequency }} MHz)
          </span>
        </div>
      </div>
    </div>

    <!-- 消息显示区域 -->
    <div class="messages-container">
      <!-- 按频道分组显示 -->
      <div v-if="showAllChannels && selectedAirport" class="channels-grid">
        <div 
          v-for="channel in availableChannels" 
          :key="channel.name"
          class="channel-messages"
        >
          <div class="channel-header" :class="{ active: isChannelSubscribed(channel.name) }">
            <h4>{{ channel.name }}</h4>
            <span class="channel-frequency">{{ channel.frequency }} MHz</span>
          </div>
          <div class="message-list">
            <div 
              v-for="message in getChannelMessages(selectedAirport, channel.name)" 
              :key="message.id" 
              class="message-card"
              :class="[message.message_type, { 'is-emergency': message.is_emergency }]"
            >
              <div class="message-header">
                <span class="callsign">{{ message.callsign || 'N/A' }}</span>
                <span class="timestamp">{{ formatTime(message.received_at) }}</span>
              </div>
              <div class="message-content">
                {{ message.message_content }}
              </div>
              <div v-if="showTranslation && message.translated_content" class="translated-content">
                {{ message.translated_content }}
              </div>
              <div class="message-footer">
                <span class="message-type-badge" :class="message.message_type">
                  {{ getMessageTypeLabel(message.message_type) }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 单频道或混合显示 -->
      <div v-else class="single-view">
        <div 
          v-for="message in displayedMessages" 
          :key="message.id" 
          class="message-card"
          :class="[message.message_type, { 'is-emergency': message.is_emergency, 'is-new': message.isNew }]"
        >
          <div class="message-header">
            <span class="frequency-badge">{{ formatFrequency(message.frequency) }}</span>
            <span v-if="message.channel_name" class="channel-badge">{{ message.channel_name }}</span>
            <span class="callsign">{{ message.callsign || 'N/A' }}</span>
            <span class="timestamp">{{ formatTime(message.received_at) }}</span>
          </div>
          <div class="message-content">
            {{ message.message_content }}
          </div>
          <div v-if="showTranslation && message.translated_content" class="translated-content">
            {{ message.translated_content }}
          </div>
          <div class="message-footer">
            <span class="message-type-badge" :class="message.message_type">
              {{ getMessageTypeLabel(message.message_type) }}
            </span>
            <span v-if="message.is_emergency" class="emergency-badge">🚨 紧急</span>
          </div>
        </div>
        
        <div v-if="displayedMessages.length === 0" class="no-messages">
          <p>⏳ 等待 ATC 通信...</p>
          <p v-if="!isConnected" class="offline-warning">未连接到音频流</p>
          <p v-else-if="!selectedAirport" class="hint">请选择机场和频道开始接收消息</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { formatFrequency } from '@/utils/formatters'
import { useATCSocket } from '@/composables/useATCSocket'

// 机场和频道配置
const airports = [
  { code: 'KJFK', name: 'John F. Kennedy Intl (New York)' },
  { code: 'KLAX', name: 'Los Angeles Intl' },
  { code: 'EGLL', name: 'London Heathrow' },
  { code: 'RJTT', name: 'Tokyo Haneda' },
  { code: 'ZBAA', name: 'Beijing Capital' },
  { code: 'VHHH', name: 'Hong Kong Intl' }
]

const channelsByAirport: Record<string, Array<{name: string, frequency: string, type: string}>> = {
  'KJFK': [
    { name: 'Tower', frequency: '119.100', type: 'tower' },
    { name: 'Ground', frequency: '121.900', type: 'ground' },
    { name: 'Approach', frequency: '125.700', type: 'approach' },
    { name: 'Departure', frequency: '135.900', type: 'departure' },
    { name: 'Clearance', frequency: '135.050', type: 'clearance' },
    { name: 'ATIS', frequency: '128.725', type: 'atis' }
  ],
  'KLAX': [
    { name: 'Tower', frequency: '133.900', type: 'tower' },
    { name: 'Ground', frequency: '121.750', type: 'ground' },
    { name: 'Approach', frequency: '124.900', type: 'approach' },
    { name: 'Departure', frequency: '125.200', type: 'departure' }
  ],
  'EGLL': [
    { name: 'Tower', frequency: '118.500', type: 'tower' },
    { name: 'Ground', frequency: '121.900', type: 'ground' },
    { name: 'Approach', frequency: '119.725', type: 'approach' }
  ],
  'RJTT': [
    { name: 'Tower', frequency: '118.100', type: 'tower' },
    { name: 'Ground', frequency: '121.700', type: 'ground' },
    { name: 'Approach', frequency: '119.100', type: 'approach' }
  ],
  'ZBAA': [
    { name: 'Tower', frequency: '118.500', type: 'tower' },
    { name: 'Ground', frequency: '121.600', type: 'ground' },
    { name: 'Approach', frequency: '119.250', type: 'approach' }
  ],
  'VHHH': [
    { name: 'Tower', frequency: '118.200', type: 'tower' },
    { name: 'Ground', frequency: '121.800', type: 'ground' },
    { name: 'Approach', frequency: '124.000', type: 'approach' }
  ]
}

// 状态变量
const selectedAirport = ref('')
const subscribedChannels = ref<Set<string>>(new Set())
const showTranslation = ref(false)
const showAllChannels = ref(false)

// 使用 ATC Socket
const { 
  messages, 
  isConnected, 
  activeStreams,
  subscribeToChannel, 
  unsubscribeFromChannel,
  getChannelMessages 
} = useATCSocket()

// 计算可用频道
const availableChannels = computed(() => {
  if (!selectedAirport.value) return []
  return channelsByAirport[selectedAirport.value] || []
})

// 计算显示的消息
const displayedMessages = computed(() => {
  if (!selectedAirport.value) {
    return messages.value
  }
  
  // 如果订阅了特定频道，只显示这些频道的消息
  if (subscribedChannels.value.size > 0) {
    return messages.value.filter(msg => {
      const channelKey = `${msg.airport_code}_${msg.channel_name}`
      return msg.airport_code === selectedAirport.value && 
             subscribedChannels.value.has(channelKey)
    })
  }
  
  // 否则显示该机场的所有消息
  return messages.value.filter(msg => msg.airport_code === selectedAirport.value)
})

// 切换频道订阅
const toggleChannel = (channelName: string) => {
  if (!selectedAirport.value) return
  
  const channelKey = `${selectedAirport.value}_${channelName}`
  
  if (subscribedChannels.value.has(channelKey)) {
    unsubscribeFromChannel(selectedAirport.value, channelName)
    subscribedChannels.value.delete(channelKey)
  } else {
    subscribeToChannel(selectedAirport.value, channelName)
    subscribedChannels.value.add(channelKey)
  }
}

// 检查频道是否已订阅
const isChannelSubscribed = (channelName: string) => {
  if (!selectedAirport.value) return false
  const channelKey = `${selectedAirport.value}_${channelName}`
  return subscribedChannels.value.has(channelKey)
}

// 格式化时间
const formatTime = (isoString: string) => {
  const date = new Date(isoString)
  return date.toLocaleTimeString('zh-CN', { 
    hour: '2-digit', 
    minute: '2-digit', 
    second: '2-digit' 
  })
}

// 获取消息类型标签（中文）
const getMessageTypeLabel = (type: string): string => {
  const labels: Record<string, string> = {
    'clearance': '放行许可',
    'contact': '联系指令',
    'taxi': '滑行',
    'takeoff': '起飞',
    'landing': '降落',
    'position': '位置报告',
    'emergency': '紧急',
    'other': '其他'
  }
  return labels[type] || type
}

// 初始化时订阅默认频道
onMounted(() => {
  console.log('ATC View mounted')
})
</script>

<style scoped>
.atc-page {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.atc-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #ecf0f1;
}

.atc-header h1 {
  color: #2c3e50;
  margin: 0;
  font-size: 1.8rem;
}

.status-indicator {
  font-weight: bold;
  padding: 8px 16px;
  border-radius: 6px;
  background: #ecf0f1;
  font-size: 0.9rem;
}

.status-indicator.online {
  background: #fadbd8;
  color: #c0392b;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

/* 控制区域 */
.controls-section {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.control-group {
  margin-bottom: 15px;
}

.control-group:last-child {
  margin-bottom: 0;
}

.control-group label {
  display: block;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 8px;
  font-size: 0.9rem;
}

.form-select {
  width: 100%;
  max-width: 400px;
  padding: 10px 14px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.95rem;
  background: white;
  cursor: pointer;
}

.channel-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.channel-btn {
  padding: 10px 16px;
  border: 2px solid #ddd;
  border-radius: 6px;
  background: white;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.9rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 120px;
}

.channel-btn:hover {
  border-color: #3498db;
  background: #ebf5fb;
}

.channel-btn.active {
  border-color: #2ecc71;
  background: #d5f5e3;
  color: #27ae60;
  font-weight: 600;
}

.channel-btn.emergency {
  border-color: #e74c3c;
}

.channel-btn .freq {
  font-size: 0.75rem;
  color: #7f8c8d;
  margin-top: 4px;
}

.toggle-options {
  display: flex;
  gap: 20px;
}

.toggle-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 0.9rem;
  color: #2c3e50;
}

.toggle-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

/* 活动流状态 */
.active-streams {
  background: #fff3cd;
  padding: 15px 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  border-left: 4px solid #f39c12;
}

.active-streams h3 {
  margin: 0 0 10px 0;
  font-size: 1rem;
  color: #856404;
}

.stream-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.stream-item {
  display: flex;
  align-items: center;
  gap: 8px;
  background: white;
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 0.85rem;
}

.stream-status {
  animation: blink 1.5s infinite;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

.stream-info {
  color: #2c3e50;
}

/* 消息容器 */
.messages-container {
  display: grid;
  gap: 15px;
}

.channels-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.channel-messages {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.channel-header {
  padding: 12px 16px;
  background: #ecf0f1;
  border-bottom: 2px solid #bdc3c7;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.channel-header.active {
  background: #d5f5e3;
  border-bottom-color: #2ecc71;
}

.channel-header h4 {
  margin: 0;
  font-size: 1rem;
  color: #2c3e50;
}

.channel-frequency {
  font-size: 0.8rem;
  color: #7f8c8d;
  font-weight: 600;
}

.message-list {
  max-height: 400px;
  overflow-y: auto;
  padding: 10px;
}

.single-view {
  display: grid;
  gap: 15px;
}

.message-card {
  background: white;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-left: 4px solid #bdc3c7;
  transition: all 0.3s;
}

.message-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.message-card.is-new {
  animation: highlight 2s ease-out;
}

.message-card.is-emergency {
  border-left-color: #c0392b;
  animation: emergency-pulse 2s infinite;
}

@keyframes emergency-pulse {
  0%, 100% { background-color: white; }
  50% { background-color: #fadbd8; }
}

@keyframes highlight {
  0% { background-color: #fff3cd; }
  100% { background-color: white; }
}

.message-card.clearance { border-left-color: #27ae60; }
.message-card.contact { border-left-color: #2980b9; }
.message-card.taxi { border-left-color: #8e44ad; }
.message-card.takeoff { border-left-color: #2ecc71; }
.message-card.landing { border-left-color: #e74c3c; }
.message-card.position { border-left-color: #f39c12; }
.message-card.emergency { border-left-color: #c0392b; }

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  font-size: 0.85rem;
  flex-wrap: wrap;
  gap: 8px;
}

.frequency-badge {
  font-weight: bold;
  color: #2980b9;
  background: #d4e6f1;
  padding: 2px 8px;
  border-radius: 4px;
}

.channel-badge {
  font-weight: 600;
  color: #8e44ad;
  background: #ebdef0;
  padding: 2px 8px;
  border-radius: 4px;
}

.callsign {
  font-weight: 600;
  color: #2c3e50;
}

.timestamp {
  color: #7f8c8d;
  font-family: monospace;
}

.message-content {
  color: #34495e;
  margin-bottom: 10px;
  line-height: 1.6;
  font-size: 0.95rem;
}

.translated-content {
  color: #27ae60;
  margin-bottom: 10px;
  line-height: 1.6;
  font-size: 0.9rem;
  padding: 8px;
  background: #f0f9f0;
  border-radius: 4px;
  border-left: 3px solid #27ae60;
}

.message-footer {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 8px;
}

.message-type-badge {
  font-size: 0.7rem;
  font-weight: bold;
  text-transform: uppercase;
  padding: 4px 10px;
  border-radius: 4px;
  background: #ecf0f1;
}

.message-type-badge.clearance { background: #d5f5e3; color: #27ae60; }
.message-type-badge.contact { background: #d4e6f1; color: #2980b9; }
.message-type-badge.taxi { background: #ebdef0; color: #8e44ad; }
.message-type-badge.takeoff { background: #d5f5e3; color: #2ecc71; }
.message-type-badge.landing { background: #fadbd8; color: #e74c3c; }
.message-type-badge.position { background: #fdebd0; color: #f39c12; }
.message-type-badge.emergency { background: #fadbd8; color: #c0392b; }

.emergency-badge {
  font-size: 0.75rem;
  font-weight: bold;
  color: #c0392b;
  background: #fadbd8;
  padding: 4px 10px;
  border-radius: 4px;
  animation: blink 1s infinite;
}

.no-messages {
  text-align: center;
  padding: 60px 20px;
  color: #7f8c8d;
  background: #f8f9fa;
  border-radius: 8px;
}

.no-messages p {
  margin: 10px 0;
}

.offline-warning {
  color: #e74c3c !important;
  font-weight: 600;
}

.hint {
  font-size: 0.9rem;
  color: #95a5a6 !important;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .atc-header {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
  
  .channels-grid {
    grid-template-columns: 1fr;
  }
  
  .channel-buttons {
    flex-direction: column;
  }
  
  .channel-btn {
    width: 100%;
  }
  
  .toggle-options {
    flex-direction: column;
    gap: 10px;
  }
}
</style>
