# FlightFRD - 航班管理系统

一个现代化的航班管理系统，提供用户注册、邮箱验证、登录认证以及航班日历视图等功能，**并集成了 ATC（空中交通管制）实时直播功能**。

## 📋 项目特性

### 已实现功能
- ✅ **用户注册**：完整的注册表单，包含用户名、邮箱、密码等信息
- ✅ **邮箱验证**：注册后自动发送验证邮件，支持令牌验证和重发功能
- ✅ **用户登录**：JWT Token 认证，安全的会话管理
- ✅ **日历视图**：可视化展示航班信息，支持日期交互
- ✅ **响应式设计**：适配桌面和移动设备
- ✅ **ATC 直播**：实时音频流监听、语音转文字、消息分类、多频道显示
- ✅ **中文翻译**：ATC 通信实时翻译（可选）

### ATC 直播功能特性

#### 🎧 音频流直播
- 支持 LiveATC.net 和 SDR 硬件数据源
- WebSocket 和 HTTP 流媒体处理
- 多频道并发监听

#### 🤖 AI 语音识别
- **内置 OpenAI Whisper 模型**（自动下载）
- 实时语音转文字
- 自动提取航空呼号
- 消息智能分类（起飞/降落/滑行/紧急等）

#### 📺 分频道显示
- 按机场分组（KJFK、KLAX、EGLL 等）
- 按频道类型（Tower、Ground、Approach 等）
- 可订阅/取消订阅特定频道

#### 🌐 实时翻译
- 可选的实时中英文翻译
- 原文与译文对照显示

#### ⚡ 实时推送
- WebSocket 实时通信
- 消息优先级排序
- 紧急消息高亮闪烁

### 技术栈

#### 后端 (Backend)
- **框架**: Flask (Python)
- **数据库**: SQLAlchemy (支持 SQLite/PostgreSQL/MySQL)
- **认证**: JWT (JSON Web Tokens)
- **邮件服务**: Flask-Mail (SMTP)
- **密码加密**: Werkzeug/Bcrypt
- **API 规范**: RESTful API
- **实时通信**: Flask-SocketIO
- **语音识别**: OpenAI Whisper
- **音频处理**: websocket-client, ffmpeg-python

#### 前端 (Frontend)
- **框架**: Vue 3 + TypeScript
- **构建工具**: Vite
- **状态管理**: Pinia
- **路由**: Vue Router
- **UI 组件**: 自定义组件 + 响应式布局
- **HTTP 客户端**: Axios
- **WebSocket**: socket.io-client

## 📁 项目结构

```
/workspace
├── backend/                 # 后端代码
│   ├── app/                # 应用主目录
│   │   ├── api/           # API 路由
│   │   ├── models/        # 数据模型
│   │   ├── services/      # 业务逻辑
│   │   │   └── audio_stream_service.py  # ATC 音频流处理
│   │   ├── utils/         # 工具函数
│   │   └── config.py      # 配置文件
│   ├── requirements.txt   # Python 依赖
│   └── run.py            # 启动脚本
│
├── frontend/              # 前端代码
│   ├── src/              # 源代码
│   │   ├── views/        # 页面组件
│   │   │   └── ATCView.vue  # ATC 直播页面
│   │   ├── components/   # 可复用组件
│   │   ├── stores/       # Pinia 状态管理
│   │   ├── router/       # 路由配置
│   │   ├── api/          # API 调用
│   │   ├── composables/  # Vue 组合式函数
│   │   │   └── useATCSocket.ts  # ATC WebSocket 连接
│   │   └── types/        # TypeScript 类型定义
│   ├── package.json      # Node.js 依赖
│   └── vite.config.ts    # Vite 配置
│
├── .gitignore           # Git 忽略文件
├── README.md           # 项目说明
└── ATC_LIVE_COMPLETE_GUIDE.md  # ATC 直播详细指南
```

## 🚀 本地部署指南

### 前置要求

#### 后端
- Python 3.8+
- pip (Python 包管理器)
- **FFmpeg**（用于音频处理）：
  - Ubuntu/Debian: `sudo apt-get install ffmpeg`
  - macOS: `brew install ffmpeg`
  - Windows: 从 https://ffmpeg.org/download.html 下载

#### 前端
- Node.js 16+
- npm 或 yarn

### 1. 克隆项目

```bash
cd /workspace
```

### 2. 后端设置

#### 安装依赖
```bash
cd backend
pip install -r requirements.txt
```

> ⚠️ **ATC 功能依赖说明**:
> - `openai-whisper`: OpenAI 语音识别模型，首次运行时会自动下载模型文件（约 140MB）
> - `websocket-client`: 用于连接 LiveATC.net 等音频流
> - `ffmpeg-python`: 音频处理工具，需要系统已安装 FFmpeg
> - `sounddevice`: 音频设备访问（可选，用于 SDR 硬件）
> - `scipy`: 科学计算库，用于音频信号处理

#### 配置环境变量
创建 `.env` 文件在 `backend/` 目录下：

```bash
# 后端/.env
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your-secret-key-here-change-in-production

# 数据库配置
DATABASE_URL=sqlite:///flightfrd.db

# JWT 配置
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ACCESS_TOKEN_EXPIRES=3600

# 邮件服务配置 (用于邮箱验证)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com

# 前端地址 (用于 CORS)
FRONTEND_URL=http://localhost:5173

# ATC 直播配置（可选）
ATC_ENABLED=true
WHISPER_MODEL=base  # 可选：tiny, base, small, medium, large
TRANSLATION_ENABLED=false
```

> ⚠️ **注意**: 
> - `SECRET_KEY` 和 `JWT_SECRET_KEY` 请使用强随机字符串
> - Gmail 用户需要使用"应用专用密码"，而非登录密码
> - 其他邮件服务商请调整相应配置

#### 初始化数据库
```bash
cd backend
python run.py  # 首次运行会自动创建数据库
```

#### 启动后端服务
```bash
cd backend
python run.py
```

后端将在 `http://localhost:5000` 运行

### 3. 前端设置

#### 安装依赖
```bash
cd frontend
npm install
# 或
yarn install
```

#### 配置环境变量
创建 `.env` 文件在 `frontend/` 目录下：

```bash
# 前端/.env
VITE_API_BASE_URL=http://localhost:5000/api/v1
VITE_APP_NAME=FlightFRD
```

#### 启动前端开发服务器
```bash
cd frontend
npm run dev
# 或
yarn dev
```

前端将在 `http://localhost:5173` 运行

### 4. 访问应用

打开浏览器访问：`http://localhost:5173`

### 5. 使用 ATC 直播功能

#### 访问 ATC 直播页面
访问 `http://localhost:5173/atc` 进入 ATC 直播界面

#### 配置音频源
在 `.env` 文件中配置或使用预设的 LiveATC.net 流：

```bash
# 预设机场频率（已在代码中配置）
- KJFK (纽约肯尼迪): Tower 118.7, Ground 121.9, Approach 125.25
- KLAX (洛杉矶): Tower 120.35, Ground 121.75, Approach 124.9
- EGLL (伦敦希思罗): Tower 118.5, Ground 121.7, Approach 119.2
- RJTT (东京羽田): Tower 118.1, Ground 121.6, Approach 119.1
- ZBAA (北京首都): Tower 118.5, Ground 121.9, Approach 119.7
- VHHH (香港): Tower 118.4, Ground 121.8, Approach 119.3
```

#### 使用 SDR 硬件（可选）
如需使用 RTL-SDR 硬件接收真实无线电：
```bash
# 安装 RTL-SDR 驱动
pip install pyrtlsdr

# Ubuntu/Debian
sudo apt-get install rtl-sdr librtlsdr-dev

# macOS
brew install rtlsdr

# 连接 RTL-SDR 设备后，在应用中配置频率
```

## 📝 API 端点

### 认证相关
| 方法 | 端点 | 描述 |
|------|------|------|
| POST | `/api/v1/auth/register` | 用户注册 |
| GET | `/api/v1/auth/verify-email/<token>` | 验证邮箱 |
| POST | `/api/v1/auth/resend-verification` | 重发验证邮件 |
| POST | `/api/v1/auth/login` | 用户登录 |
| POST | `/api/v1/auth/logout` | 用户登出 |
| GET | `/api/v1/auth/me` | 获取当前用户信息 |

### 航班相关
| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/v1/flights` | 获取航班列表 |
| GET | `/api/v1/flights/<id>` | 获取航班详情 |
| POST | `/api/v1/flights` | 创建航班 (需认证) |
| PUT | `/api/v1/flights/<id>` | 更新航班 (需认证) |
| DELETE | `/api/v1/flights/<id>` | 删除航班 (需认证) |

## 🔐 安全特性

- 密码使用 bcrypt 加密存储
- JWT Token 认证机制
- 邮箱验证防止虚假注册
- CORS 跨域保护
- 输入验证和 sanitization
- SQL 注入防护 (通过 SQLAlchemy ORM)

## 🛠️ 开发指南

### 后端开发

```bash
# 进入虚拟环境
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 运行开发服务器
python run.py
```

### 前端开发

```bash
# 安装依赖
cd frontend
npm install

# 启动开发服务器 (热重载)
npm run dev

# 构建生产版本
npm run build

# 代码检查
npm run lint
```

## 📦 生产部署

### 后端部署建议
- 使用 Gunicorn 或 uWSGI 作为 WSGI 服务器
- 使用 Nginx 作为反向代理
- 使用 PostgreSQL 或 MySQL 替代 SQLite
- 配置 HTTPS
- 设置适当的缓存策略

### 前端部署建议
- 运行 `npm run build` 生成静态文件
- 使用 Nginx 或其他 Web 服务器托管 `dist/` 目录
- 配置 CDN 加速静态资源
- 启用 gzip 压缩

## 🐛 常见问题

### 邮箱验证不工作？
1. 检查 `.env` 中的邮件服务器配置
2. 确认邮箱账号开启了 SMTP 权限
3. 查看后端日志获取详细错误信息
4. 垃圾邮件箱中查找验证邮件

### 端口被占用？
- 后端默认使用 5000 端口，可通过 `FLASK_RUN_PORT` 修改
- 前端默认使用 5173 端口，可在 `vite.config.ts` 中修改

### 数据库迁移问题？
- 删除 `instance/` 目录和 `.db` 文件重新初始化
- 或使用 Flask-Migrate 进行数据库迁移管理

### ATC 语音识别不工作？
1. **检查 Whisper 模型是否下载**：
   - 首次运行时会自动下载模型（约 140MB）
   - 手动下载：`python -c "import whisper; whisper.load_model('base')"`
   - 模型存储位置：`~/.cache/whisper/`

2. **检查 FFmpeg 是否安装**：
   ```bash
   ffmpeg -version  # 检查是否安装
   sudo apt-get install ffmpeg  # Ubuntu/Debian 安装
   brew install ffmpeg  # macOS 安装
   ```

3. **查看后端日志**：
   - 确认没有 "Whisper not installed" 警告
   - 检查音频流连接状态

4. **调整模型大小**（如果性能不足）：
   ```bash
   # 在 .env 中修改
   WHISPER_MODEL=tiny  # 更快但精度较低
   # 可选：tiny (39M), base (74M), small (244M), medium (769M), large (1550M)
   ```

### LiveATC.net 流无法连接？
- LiveATC.net 限制非商业用途，建议仅用于测试
- 考虑使用 SDR 硬件接收本地机场信号
- 或购买商业航空数据服务

## 🤖 AI 模型说明

### OpenAI Whisper 模型

本项目使用 OpenAI Whisper 进行语音识别，模型会自动下载。

#### 模型下载地址
- **官方源**（自动下载）：https://openaipublic.azureedge.net/main/whisper/models/
- **手动下载**（如果自动下载失败）：

| 模型 | 大小 | 下载链接 | 适用场景 |
|------|------|---------|---------|
| tiny | 39 MB | [下载](https://openaipublic.azureedge.net/main/whisper/models/65147644a518d12f04e32d6f3b26facc3f8dd46e5390956a9424a650c0ce22b9/tiny.pt) | 低配置设备 |
| base | 74 MB | [下载](https://openaipublic.azureedge.net/main/whisper/models/ed3a0b6b1c0edf879ad9b11b1af5a0e6ab5db9205f891f668f8b0e6c6326e34e/base.pt) | 推荐默认 |
| small | 244 MB | [下载](https://openaipublic.azureedge.net/main/whisper/models/f953ad0fd29cacd07d5a9eda56200b7e07378584f1306f58bfe242f80c3eb83c/small.pt) | 高精度需求 |
| medium | 769 MB | [下载](https://openaipublic.azureedge.net/main/whisper/models/345ae4da62f9b3d59415adc60127b97c714f32e89e936602e85993674d08dcb1/medium.pt) | 专业用途 |
| large | 1550 MB | [下载](https://openaipublic.azureedge.net/main/whisper/models/e5b1a55b89c1367dacf97e3e19bfd82964718a94f0dd8aa6486ba16b656cb2cd/large-v3.pt) | 最高精度 |

#### 手动安装模型
```bash
# 1. 下载模型文件
wget https://openaipublic.azureedge.net/main/whisper/models/ed3a0b6b1c0edf879ad9b11b1af5a0e6ab5db9205f891f668f8b0e6c6326e34e/base.pt -O ~/.cache/whisper/base.pt

# 2. 或在代码中指定路径
# 修改 backend/app/services/audio_stream_service.py
self.whisper_model = whisper.load_model("/path/to/base.pt")
```

#### 模型要求
- **CPU**: base 模型约 1-2 秒延迟
- **GPU**: 支持 CUDA，可大幅提升速度
- **内存**: base 模型至少需要 1GB RAM

## 📄 许可证

本项目采用 MIT 许可证

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📚 相关文档

- [ATC 直播完整实现指南](ATC_LIVE_COMPLETE_GUIDE.md) - 详细的 ATC 功能实现说明
- [部署教程](DEPLOYMENT_TUTORIAL.md) - 生产环境部署指南

## 📞 联系方式

如有问题，请通过 GitHub Issues 联系。

---

**祝您使用愉快！** ✈️
