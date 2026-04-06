# ATC 直播实现完整指南

## 📋 功能概述

本系统实现了完整的 ATC（空中交通管制）直播功能，包括：

1. **音频流直播** - 实时接收和处理 ATC 音频
2. **语音转文字** - 使用 Whisper AI 进行实时转录
3. **消息分类** - 自动识别消息类型（起飞、降落、滑行等）
4. **多频道支持** - 按机场和频道（Tower、Ground、Approach 等）分组
5. **实时推送** - WebSocket 实时推送到前端
6. **中文翻译** - 可选的实时翻译功能

---

## 🏗️ 架构设计

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   音频源        │────▶│   后端处理服务   │────▶│   前端显示      │
│                 │     │                  │     │                 │
│ • LiveATC.net   │     │ • 音频流管理     │     │ • 频道选择      │
│ • SDR 硬件      │     │ • 语音识别       │     │ • 实时消息      │
│ • 其他 API      │     │ • 消息分类       │     │ • 翻译切换      │
└─────────────────┘     │ • WebSocket 推送  │     │ • 状态指示      │
                        └──────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌──────────────────┐
                        │   PostgreSQL     │
                        │                  │
                        │ • atc_messages表 │
                        └──────────────────┘
```

---

## 📁 文件结构

### 后端文件

```
backend/
├── app/
│   ├── services/
│   │   ├── atc_service.py              # ATC 基础服务
│   │   └── audio_stream_service.py     # 音频流处理服务（新增）
│   ├── api/v1/
│   │   └── atc.py                      # ATC API 和 WebSocket 事件
│   └── models/
│       └── atc_message.py              # ATC 消息数据模型
```

### 前端文件

```
frontend/
└── src/
    ├── composables/
    │   └── useATCSocket.ts             # WebSocket 连接管理（新增）
    └── views/
        └── ATCView.vue                 # ATC 直播页面（已更新）
```

---

## 🚀 快速开始

### 1. 安装依赖

```bash
# 后端依赖
cd backend
pip install \
    websocket-client \
    requests \
    openai-whisper \
    ffmpeg-python \
    flask-socketio \
    python-socketio[asyncio]

# 前端依赖
cd frontend
npm install socket.io-client
```

### 2. 配置环境变量

创建 `backend/.env` 文件：

```bash
# ATC 流配置
ATC_STREAM_PROVIDER=liveatc
WHISPER_MODEL=base
ENABLE_AUDIO_RECORDING=false
AUDIO_STORAGE_PATH=/var/atc/recordings

# WebSocket 配置
SOCKETIO_ASYNC_MODE=threading
SOCKETIO_CORS_ORIGINS=http://localhost:5173
```

### 3. 启动服务

```bash
# 启动后端（终端 1）
cd backend
python run.py

# 启动前端（终端 2）
cd frontend
npm run dev
```

### 4. 访问应用

打开浏览器访问：`http://localhost:5173/atc`

---

## 🔧 核心功能说明

### 音频流服务 (audio_stream_service.py)

**主要功能：**

1. **流管理**
   - `start_stream()` - 启动音频流监听
   - `stop_stream()` - 停止音频流
   - `get_active_streams()` - 获取活动流列表

2. **音频处理**
   - `_handle_websocket_stream()` - 处理 WebSocket 音频流
   - `_handle_http_stream()` - 处理 HTTP 音频流（Icecast/Shoutcast）
   - `_process_audio_buffer()` - 处理音频缓冲区

3. **语音识别与分类**
   - `_extract_callsign()` - 提取航空呼号
   - `_classify_message()` - 分类消息类型
   - `_is_emergency()` - 检测紧急通信
   - `_calculate_priority()` - 计算优先级

4. **实时推送**
   - 通过 Socket.IO 推送新消息到前端
   - 支持频道级别的订阅/取消订阅

### WebSocket 连接 (useATCSocket.ts)

**提供的功能：**

```typescript
const {
  socket,              // Socket.IO 连接实例
  messages,            // 所有消息列表
  isConnected,         // 连接状态
  activeStreams,       // 活动音频流
  subscribedChannels,  // 已订阅的频道
  messagesByChannel,   // 按频道分组的消息
  
  // 方法
  subscribeToChannel,      // 订阅频道
  unsubscribeFromChannel,  // 取消订阅频道
  subscribeToFrequency,    // 订阅频率
  unsubscribeFromFrequency,// 取消订阅频率
  getChannelMessages,      // 获取频道消息
  clearMessages           // 清除消息
} = useATCSocket()
```

### 前端界面 (ATCView.vue)

**界面特性：**

1. **机场选择** - 支持全球主要机场
2. **频道选择** - Tower、Ground、Approach 等
3. **实时状态** - 显示连接状态和活动流
4. **消息显示**
   - 按类型着色（起飞=绿色，降落=红色，紧急=闪烁）
   - 支持单频道/多频道视图
   - 可选中文翻译
5. **消息分类标签**
   - 放行许可、联系指令、滑行、起飞、降落、位置报告、紧急

---

## 📊 消息类型说明

| 类型 | 说明 | 示例 |
|------|------|------|
| clearance | 放行许可 | "Cleared to JFK via flight plan" |
| contact | 联系指令 | "Contact Departure on 125.7" |
| taxi | 滑行指令 | "Taxi to runway 24L via Alpha" |
| takeoff | 起飞许可 | "Cleared for takeoff runway 24L" |
| landing | 降落许可 | "Cleared to land runway 24R" |
| position | 位置报告 | "Passing 10,000 feet" |
| emergency | 紧急通信 | "Mayday Mayday Mayday" |
| other | 其他 | 无法分类的消息 |

---

## 🎯 使用示例

### 订阅特定机场频道

```typescript
// 订阅 JFK Tower
subscribeToChannel('KJFK', 'Tower')

// 订阅 JFK Ground
subscribeToChannel('KJFK', 'Ground')

// 取消订阅
unsubscribeFromChannel('KJFK', 'Tower')
```

### 获取频道消息

```typescript
// 获取 JFK Tower 的所有消息
const towerMessages = getChannelMessages('KJFK', 'Tower')

// 获取所有消息
const allMessages = messages.value
```

---

## 🔍 测试数据源

### LiveATC.net（推荐用于测试）

```python
# 获取机场音频流 URL
import requests

def get_liveatc_streams(airport_code):
    url = f"https://www.liveatc.net/json/feedezmlist.php?icao={airport_code}"
    response = requests.get(url)
    return response.json()

# 示例：获取 JFK 机场的流
streams = get_liveatc_streams('KJFK')
print(streams)
```

### 常见机场频率参考

**KJFK (纽约肯尼迪)**
- Tower: 119.100 MHz
- Ground: 121.900 MHz
- Approach: 125.700 MHz
- Departure: 135.900 MHz
- Clearance: 135.050 MHz
- ATIS: 128.725 MHz

**KLAX (洛杉矶)**
- Tower: 133.900 MHz
- Ground: 121.750 MHz
- Approach: 124.900 MHz

---

## ⚠️ 注意事项

### 法律合规
- ✅ 遵守当地无线电接收法律
- ✅ 遵守音频源的使用条款（如 LiveATC.net）
- ❌ 不得用于非法目的
- ❌ 不得重新分发受版权保护的音频流

### 性能优化
- 使用 Redis 缓存频繁访问的数据
- 对历史消息进行分页加载
- 限制每个频道的消息数量（默认 100 条）
- 考虑使用 CDN 分发静态资源

### 隐私保护
- 不录制和存储敏感通信
- 遵守数据保护法规（GDPR 等）
- 提供消息删除功能

---

## 🛠️ 故障排除

### 常见问题

**1. WebSocket 连接失败**
```bash
# 检查后端是否启动
curl http://localhost:5000/api/v1/atc/messages

# 检查 CORS 配置
# 确保 SOCKETIO_CORS_ORIGINS 包含前端地址
```

**2. 语音识别不工作**
```bash
# 检查 Whisper 是否安装
python -c "import whisper; print(whisper.__version__)"

# 检查 FFmpeg 是否安装
ffmpeg -version
```

**3. 没有收到消息**
- 确认已选择机场和频道
- 检查 WebSocket 连接状态（浏览器控制台）
- 确认音频流 URL 有效

---

## 📈 扩展功能建议

1. **多语言支持** - 集成 DeepL/Google Translate API
2. **AI 分析** - 使用 ML 识别异常通信模式
3. **地图集成** - 在地图上显示航班位置和对应通信
4. **搜索功能** - 按呼号、日期、机场搜索历史记录
5. **移动端应用** - 开发 iOS/Android 应用
6. **音频回放** - 保存并回放原始音频
7. **统计面板** - 显示流量统计、 busiest times 等

---

## 📚 相关资源

- [LiveATC.net](https://www.liveatc.net/) - 全球 ATC 音频流
- [OpenAI Whisper](https://github.com/openai/whisper) - 语音识别模型
- [Socket.IO](https://socket.io/) - WebSocket 库
- [RTL-SDR](https://www.rtl-sdr.com/) - 软件定义无线电

---

祝您成功实现 ATC 直播功能！✈️📻

如有问题，请查看日志文件或提交 issue。
