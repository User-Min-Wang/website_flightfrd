# FlightFRD - 航班管理系统

一个现代化的航班管理系统，提供用户注册、邮箱验证、登录认证以及航班日历视图等功能。

## 📋 项目特性

### 已实现功能
- ✅ **用户注册**：完整的注册表单，包含用户名、邮箱、密码等信息
- ✅ **邮箱验证**：注册后自动发送验证邮件，支持令牌验证和重发功能
- ✅ **用户登录**：JWT Token 认证，安全的会话管理
- ✅ **日历视图**：可视化展示航班信息，支持日期交互
- ✅ **响应式设计**：适配桌面和移动设备

### 技术栈

#### 后端 (Backend)
- **框架**: Flask (Python)
- **数据库**: SQLAlchemy (支持 SQLite/PostgreSQL/MySQL)
- **认证**: JWT (JSON Web Tokens)
- **邮件服务**: Flask-Mail (SMTP)
- **密码加密**: Werkzeug/Bcrypt
- **API 规范**: RESTful API

#### 前端 (Frontend)
- **框架**: Vue 3 + TypeScript
- **构建工具**: Vite
- **状态管理**: Pinia
- **路由**: Vue Router
- **UI 组件**: 自定义组件 + 响应式布局
- **HTTP 客户端**: Axios

## 📁 项目结构

```
/workspace
├── backend/                 # 后端代码
│   ├── app/                # 应用主目录
│   │   ├── api/           # API 路由
│   │   ├── models/        # 数据模型
│   │   ├── services/      # 业务逻辑
│   │   ├── utils/         # 工具函数
│   │   └── config.py      # 配置文件
│   ├── requirements.txt   # Python 依赖
│   └── run.py            # 启动脚本
│
├── frontend/              # 前端代码
│   ├── src/              # 源代码
│   │   ├── views/        # 页面组件
│   │   ├── components/   # 可复用组件
│   │   ├── stores/       # Pinia 状态管理
│   │   ├── router/       # 路由配置
│   │   ├── api/          # API 调用
│   │   └── types/        # TypeScript 类型定义
│   ├── package.json      # Node.js 依赖
│   └── vite.config.ts    # Vite 配置
│
├── .gitignore           # Git 忽略文件
└── README.md           # 项目说明
```

## 🚀 本地部署指南

### 前置要求

#### 后端
- Python 3.8+
- pip (Python 包管理器)

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

## 📄 许可证

本项目采用 MIT 许可证

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 联系方式

如有问题，请通过 GitHub Issues 联系。

---

**祝您使用愉快！** ✈️
