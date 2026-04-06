# ATC 直播实现指南

本指南将帮助您实现真实的 ATC（空中交通管制）直播功能。

## 📋 目录

1. [架构概述](#架构概述)
2. [数据源选项](#数据源选项)
3. [实现步骤](#实现步骤)
4. [代码示例](#代码示例)
5. [部署配置](#部署配置)

---

## 架构概述

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   音频源        │────▶│   处理服务       │────▶│   Web 前端      │
│                 │     │                  │     │                 │
│ • SDR 接收器    │     │ • 音频解码       │     │ • 实时消息显示  │
│ • LiveATC API   │     │ • 语音转文字     │     │ • 频率切换      │
│ • 其他数据源    │     │ • 消息解析       │     │ • WebSocket 推送│
└─────────────────┘     └──────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌──────────────────┐
                        │   数据库存储     │
                        │                  │
                        │ • ATCMessage 表  │
                        └──────────────────┘
```

---

## 数据源选项

### 选项 1: LiveATC.net (推荐用于测试)

LiveATC.net 提供全球各地的 ATC 音频流。

**优点**:
- 免费使用（非商业用途）
- 覆盖全球主要机场
- 稳定的音频流

**限制**:
- 需要遵守使用条款
- 不能重新分发音频流
- 仅限个人/教育用途

**API 示例**:
```python
import requests

def get_liveatc_streams(airport_code):
    """获取指定机场的音频流 URL"""
    url = f"https://www.liveatc.net/json/feedezmlist.php?icao={airport_code}"
    response = requests.get(url)
    return response.json()
```

### 选项 2: SDR (软件定义无线电)

使用 RTL-SDR 等设备直接接收无线电信号。

**所需硬件**:
- RTL-SDR USB 接收器 (~$25)
- VHF/UHF 天线（118-137 MHz 航空频段）
- 树莓派或计算机

**优点**:
- 完全控制
- 无 API 限制
- 可接收本地任何频率

**缺点**:
- 需要硬件投资
- 受地理位置限制
- 需要技术配置

### 选项 3: ADS-B Exchange + 音频同步

结合航班位置数据和音频流。

---

## 实现步骤

### 步骤 1: 安装依赖

```bash
# 后端依赖
cd backend
pip install \
    websocket-client \
    requests \
    sounddevice \
    soundfile \
    scipy \
    openai-whisper \
    ffmpeg-python \
    pyrtlsdr
```

### 步骤 2: 创建音频流服务

创建文件：`backend/app/services/audio_stream_service.py`

```python
import threading
import websocket
import json
import logging
from datetime import datetime
from extensions import db
from app.models import ATCMessage
from app.services.atc_service import ATCService

logger = logging.getLogger(__name__)

class AudioStreamService:
    """管理 ATC 音频流连接"""
    
    def __init__(self):
        self.active_streams = {}
        self.atc_service = ATCService()
    
    def start_stream(self, stream_id, stream_url, frequency, airport_code):
        """启动音频流监听"""
        if stream_id in self.active_streams:
            logger.warning(f"Stream {stream_id} already active")
            return
        
        thread = threading.Thread(
            target=self._listen_to_stream,
            args=(stream_id, stream_url, frequency, airport_code),
            daemon=True
        )
        thread.start()
        self.active_streams[stream_id] = thread
        logger.info(f"Started stream {stream_id} for frequency {frequency}")
    
    def stop_stream(self, stream_id):
        """停止音频流"""
        if stream_id in self.active_streams:
            # 实现停止逻辑
            del self.active_streams[stream_id]
    
    def _listen_to_stream(self, stream_id, stream_url, frequency, airport_code):
        """监听音频流并处理"""
        try:
            ws = websocket.create_connection(stream_url)
            
            while stream_id in self.active_streams:
                # 接收音频数据
                audio_data = ws.recv()
                
                # 处理音频（语音转文字）
                text = self._speech_to_text(audio_data)
                
                if text:
                    # 存储 ATC 消息
                    self.atc_service.store_atc_message(
                        frequency=frequency,
                        callsign=self._extract_callsign(text),
                        message_content=text,
                        message_type=self._classify_message(text),
                        airport_code=airport_code
                    )
                    
                    # 通过 WebSocket 推送给前端
                    from extensions import socketio
                    socketio.emit('new_atc_message', {
                        'frequency': frequency,
                        'callsign': self._extract_callsign(text),
                        'message_content': text,
                        'received_at': datetime.utcnow().isoformat()
                    }, namespace='/atc')
        
        except Exception as e:
            logger.error(f"Stream error: {str(e)}")
    
    def _speech_to_text(self, audio_data):
        """将音频转换为文字"""
        # 使用 Whisper 或其他 STT 服务
        import whisper
        model = whisper.load_model("base")
        result = model.transcribe(audio_data)
        return result["text"]
    
    def _extract_callsign(self, text):
        """从文本中提取呼号"""
        import re
        # 匹配航空呼号模式
        pattern = r'\b([A-Z]{2,3}\d+[A-Z]?)\b'
        match = re.search(pattern, text.upper())
        return match.group(1) if match else None
    
    def _classify_message(self, text):
        """分类消息类型"""
        text_lower = text.lower()
        if 'takeoff' in text_lower or 'cleared for takeoff' in text_lower:
            return 'takeoff'
        elif 'landing' in text_lower or 'cleared to land' in text_lower:
            return 'landing'
        elif 'taxi' in text_lower:
            return 'taxi'
        elif 'emergency' in text_lower or 'mayday' in text_lower:
            return 'emergency'
        elif 'contact' in text_lower:
            return 'contact'
        elif 'clearance' in text_lower or 'cleared' in text_lower:
            return 'clearance'
        else:
            return 'position'
```

### 步骤 3: 更新前端以使用 WebSocket

创建文件：`frontend/src/composables/useATCSocket.ts`

```typescript
import { ref, onMounted, onUnmounted } from 'vue'
import { io, Socket } from 'socket.io-client'

export function useATCSocket() {
  const socket = ref<Socket | null>(null)
  const messages = ref<any[]>([])
  const isConnected = ref(false)
  
  const connect = () => {
    socket.value = io(import.meta.env.VITE_API_BASE_URL.replace('/api/v1', ''), {
      path: '/socket.io/',
      transports: ['websocket']
    })
    
    const atcNamespace = socket.value.socket('/atc')
    
    atcNamespace.on('connect', () => {
      isConnected.value = true
      console.log('Connected to ATC stream')
    })
    
    atcNamespace.on('disconnect', () => {
      isConnected.value = false
      console.log('Disconnected from ATC stream')
    })
    
    atcNamespace.on('new_atc_message', (message: any) => {
      messages.value.unshift(message)
      // 保持最近 100 条消息
      if (messages.value.length > 100) {
        messages.value.pop()
      }
    })
    
    atcNamespace.on('atc_message_verified', (message: any) => {
      const index = messages.value.findIndex(m => m.id === message.id)
      if (index !== -1) {
        messages.value[index] = message
      }
    })
  }
  
  const subscribeToFrequency = (frequency: string) => {
    if (socket.value) {
      socket.value.emit('subscribe_to_frequency', { frequency })
    }
  }
  
  const unsubscribeFromFrequency = (frequency: string) => {
    if (socket.value) {
      socket.value.emit('unsubscribe_from_frequency', { frequency })
    }
  }
  
  onMounted(() => {
    connect()
  })
  
  onUnmounted(() => {
    if (socket.value) {
      socket.value.disconnect()
    }
  })
  
  return {
    socket,
    messages,
    isConnected,
    subscribeToFrequency,
    unsubscribeFromFrequency
  }
}
```

### 步骤 4: 更新 ATCView.vue

```vue
<template>
  <div class="atc-page">
    <div class="atc-header">
      <h1>ATC Communications Live</h1>
      <div class="status-indicator" :class="{ online: isConnected }">
        {{ isConnected ? '🔴 LIVE' : '⚪ OFFLINE' }}
      </div>
      <div class="controls">
        <select v-model="selectedFrequency" class="form-select">
          <option value="">All Frequencies</option>
          <option v-for="freq in frequencies" :key="freq" :value="freq">{{ freq }}</option>
        </select>
        <button @click="toggleSubscription" class="btn">
          {{ isSubscribed ? 'Unsubscribe' : 'Subscribe' }}
        </button>
      </div>
    </div>

    <div class="messages-container">
      <div 
        v-for="message in filteredMessages" 
        :key="message.id || message.timestamp" 
        class="message-card"
        :class="[message.message_type, { 'is-new': message.isNew }]"
      >
        <div class="message-header">
          <span class="frequency-badge">{{ formatFrequency(message.frequency) }}</span>
          <span class="callsign">{{ message.callsign || 'N/A' }}</span>
          <span class="timestamp">{{ formatDate(message.received_at) }}</span>
        </div>
        <div class="message-content">
          {{ message.message_content }}
        </div>
        <div class="message-footer">
          <span class="message-type-badge" :class="message.message_type">
            {{ message.message_type }}
          </span>
        </div>
      </div>
      
      <div v-if="filteredMessages.length === 0" class="no-messages">
        <p>Waiting for ATC communications...</p>
        <p v-if="!isConnected" class="offline-warning">Not connected to stream</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { formatFrequency, formatDate } from '@/utils/formatters'
import { useATCSocket } from '@/composables/useATCSocket'

const frequencies = ['118.100', '118.700', '119.100', '120.900', '121.900']
const selectedFrequency = ref('')
const isSubscribed = ref(false)

const { messages, isConnected } = useATCSocket()

const filteredMessages = computed(() => {
  return messages.value.filter(message => {
    return !selectedFrequency.value || message.frequency === selectedFrequency.value
  })
})

const toggleSubscription = () => {
  if (isSubscribed.value && selectedFrequency.value) {
    // Unsubscribe logic
  } else if (selectedFrequency.value) {
    // Subscribe logic
  }
  isSubscribed.value = !isSubscribed.value
}

watch(selectedFrequency, (newFreq) => {
  if (newFreq && isSubscribed.value) {
    // Re-subscribe to new frequency
  }
})
</script>

<style scoped>
/* 添加之前的样式 */
.status-indicator {
  font-weight: bold;
  padding: 5px 10px;
  border-radius: 4px;
  background: #ecf0f1;
}

.status-indicator.online {
  background: #fadbd8;
  color: #c0392b;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.message-card.is-new {
  animation: highlight 2s ease-out;
}

@keyframes highlight {
  0% { background-color: #fff3cd; }
  100% { background-color: white; }
}

.offline-warning {
  color: #e74c3c;
  font-weight: bold;
}
</style>
```

---

## 部署配置

### 环境变量

在 `backend/.env` 中添加：

```bash
# ATC Stream Configuration
ATC_STREAM_PROVIDER=liveatc
ATC_WS_URL=wss://your-websocket-url.com
WHISPER_MODEL=base
ENABLE_AUDIO_RECORDING=false
AUDIO_STORAGE_PATH=/var/atc/recordings
```

### Docker 部署（可选）

```dockerfile
# Dockerfile.atc
FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    libportaudio2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "run.py"]
```

---

## 测试与验证

1. **启动后端服务**:
```bash
cd backend
python run.py
```

2. **启动前端服务**:
```bash
cd frontend
npm run dev
```

3. **访问 ATC 页面**:
打开浏览器访问 `http://localhost:5173/atc`

4. **测试 WebSocket 连接**:
在浏览器控制台检查连接状态

---

## 注意事项

⚠️ **法律合规**:
- 确保遵守当地无线电接收法律
- 遵守音频源的使用条款
- 不得用于非法目的

⚠️ **性能优化**:
- 使用 Redis 缓存频繁访问的数据
- 对历史消息进行分页加载
- 考虑使用 CDN 分发静态资源

⚠️ **隐私保护**:
- 不要录制和存储敏感通信
- 遵守数据保护法规

---

## 扩展功能建议

1. **多语言支持**: 集成翻译服务
2. **AI 分析**: 使用 ML 识别异常通信模式
3. **地图集成**: 在地图上显示航班位置和对应通信
4. **搜索功能**: 按呼号、日期、机场搜索历史记录
5. **移动端应用**: 开发 iOS/Android 应用

---

祝您成功实现 ATC 直播功能！✈️📻
