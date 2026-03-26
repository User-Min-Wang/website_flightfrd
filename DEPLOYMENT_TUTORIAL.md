# FlightFRD 服务器配置教程

本教程将指导您如何配置 FlightFRD 航班管理系统的服务器环境，包括创建和激活 Python 虚拟环境。

## 📋 目录

1. [前置要求](#前置要求)
2. [克隆项目](#克隆项目)
3. [后端配置（含虚拟环境）](#后端配置含虚拟环境)
4. [前端配置](#前端配置)
5. [环境变量配置](#环境变量配置)
6. [启动服务](#启动服务)
7. [常见问题](#常见问题)

---

## 🔧 前置要求

### 后端要求
- **Python 3.8+** (推荐 Python 3.9 或 3.10)
- **pip** (Python 包管理器)

检查 Python 版本：
```bash
python --version
# 或
python3 --version
```

检查 pip 版本：
```bash
pip --version
# 或
pip3 --version
```

### 前端要求
- **Node.js 16+**
- **npm** 或 **yarn**

检查 Node.js 版本：
```bash
node --version
```

检查 npm 版本：
```bash
npm --version
```

---

## 📥 克隆项目

如果您还没有项目代码，请先克隆：

```bash
cd /workspace
# 项目已经在 /workspace 目录中
```

---

## 🐍 后端配置（含虚拟环境）

### 步骤 1: 进入后端目录

```bash
cd /workspace/backend
```

### 步骤 2: 创建 Python 虚拟环境 ⭐

**为什么需要虚拟环境？**
- 隔离项目依赖，避免与系统 Python 包冲突
- 便于管理不同项目的依赖版本
- 方便部署和迁移

**创建虚拟环境：**

```bash
# 方法 1: 使用 python -m venv (推荐)
python -m venv venv

# 如果上述命令不成功，尝试：
python3 -m venv venv
```

执行后会在 `backend/` 目录下生成一个 `venv/` 文件夹。

### 步骤 3: 激活虚拟环境

**Linux / macOS:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
# CMD
venv\Scripts\activate

# PowerShell
venv\Scripts\Activate.ps1
```

**激活成功的标志：**
命令行前面会出现 `(venv)` 前缀，例如：
```bash
(venv) user@hostname:/workspace/backend$
```

### 步骤 4: 升级 pip (推荐)

```bash
pip install --upgrade pip
```

### 步骤 5: 安装项目依赖

确保虚拟环境已激活后，执行：

```bash
pip install -r requirements.txt
```

这将安装以下主要依赖：
- Flask (Web 框架)
- Flask-SQLAlchemy (数据库 ORM)
- PyJWT (认证)
- Flask-Mail (邮件服务)
- bcrypt (密码加密)
- 等等...

**安装可能需要几分钟，请耐心等待。**

### 步骤 6: 验证安装

```bash
# 检查 Flask 是否安装成功
flask --version

# 检查已安装的包
pip list
```

### 步骤 7: 配置环境变量

在 `backend/` 目录下创建 `.env` 文件：

```bash
# 创建 .env 文件
touch .env
# 或使用编辑器
nano .env
```

**.env 文件内容示例：**

```bash
# Flask 配置
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

> ⚠️ **重要提示：**
> - `SECRET_KEY` 和 `JWT_SECRET_KEY` 请使用强随机字符串
> - Gmail 用户需要使用"应用专用密码"，而非登录密码
> - 生产环境请务必修改默认值！

### 步骤 8: 初始化数据库

确保虚拟环境已激活，然后运行：

```bash
python run.py
```

首次运行会自动创建数据库文件。

### 步骤 9: 启动后端服务

```bash
# 开发模式
python run.py

# 或使用 Flask 命令
flask run --host=0.0.0.0 --port=5000
```

后端服务将在 `http://localhost:5000` 运行。

---

## 🌐 前端配置

### 步骤 1: 进入前端目录

```bash
cd /workspace/frontend
```

### 步骤 2: 安装依赖

```bash
npm install
# 或
yarn install
```

### 步骤 3: 配置环境变量

在 `frontend/` 目录下创建 `.env` 文件：

```bash
# 创建 .env 文件
touch .env
# 或使用编辑器
nano .env
```

**.env 文件内容：**

```bash
VITE_API_BASE_URL=http://localhost:5000/api/v1
VITE_APP_NAME=FlightFRD
```

### 步骤 4: 启动前端开发服务器

```bash
npm run dev
# 或
yarn dev
```

前端服务将在 `http://localhost:5173` 运行。

---

## 🔐 环境变量配置详解

### 后端环境变量 (.env)

| 变量名 | 说明 | 示例值 |
|--------|------|--------|
| `FLASK_APP` | Flask 应用名称 | `app` |
| `FLASK_ENV` | 运行环境 | `development` / `production` |
| `SECRET_KEY` | Flask 密钥 | 随机字符串 |
| `DATABASE_URL` | 数据库连接 URL | `sqlite:///flightfrd.db` |
| `JWT_SECRET_KEY` | JWT 签名密钥 | 随机字符串 |
| `JWT_ACCESS_TOKEN_EXPIRES` | Token 过期时间 (秒) | `3600` |
| `MAIL_SERVER` | SMTP 服务器 | `smtp.gmail.com` |
| `MAIL_PORT` | SMTP 端口 | `587` |
| `MAIL_USERNAME` | 邮箱账号 | `your-email@gmail.com` |
| `MAIL_PASSWORD` | 邮箱密码/应用密码 | `your-password` |
| `FRONTEND_URL` | 前端地址 | `http://localhost:5173` |

### 前端环境变量 (.env)

| 变量名 | 说明 | 示例值 |
|--------|------|--------|
| `VITE_API_BASE_URL` | 后端 API 地址 | `http://localhost:5000/api/v1` |
| `VITE_APP_NAME` | 应用名称 | `FlightFRD` |

---

## 🚀 启动服务

### 完整启动流程

**终端 1 - 启动后端：**
```bash
cd /workspace/backend

# 激活虚拟环境
source venv/bin/activate

# 启动服务
python run.py
```

**终端 2 - 启动前端：**
```bash
cd /workspace/frontend

# 启动服务
npm run dev
```

### 访问应用

打开浏览器访问：`http://localhost:5173`

---

## 🛠️ 虚拟环境常用命令

### 激活虚拟环境
```bash
# Linux / macOS
source venv/bin/activate

# Windows (CMD)
venv\Scripts\activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

### 退出虚拟环境
```bash
deactivate
```

### 查看虚拟环境中的包
```bash
pip list
```

### 导出依赖
```bash
pip freeze > requirements.txt
```

### 重新安装依赖
```bash
# 确保虚拟环境已激活
pip install -r requirements.txt --force-reinstall
```

---

## 🐛 常见问题

### 1. 虚拟环境创建失败

**问题：** `python: No module named venv`

**解决方案：**
```bash
# Ubuntu/Debian
sudo apt-get install python3-venv

# CentOS/RHEL
sudo yum install python3-venv

# macOS (使用 brew)
brew install python3
```

### 2. 虚拟环境激活失败

**问题：** `source: command not found` (Windows)

**解决方案：**
Windows 用户使用：
```bash
# CMD
venv\Scripts\activate

# PowerShell
venv\Scripts\Activate.ps1
```

如果 PowerShell 提示权限问题：
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. 端口被占用

**问题：** `Address already in use`

**解决方案：**
```bash
# 查找占用端口的进程
lsof -i :5000  # 后端端口
lsof -i :5173  # 前端端口

# 杀死进程
kill -9 <PID>
```

或者修改端口：
```bash
# 后端修改端口
export FLASK_RUN_PORT=5001
flask run --port=5001

# 前端修改端口，编辑 vite.config.ts
```

### 4. 邮箱验证不工作

**检查清单：**
1. ✅ 确认 `.env` 中邮件配置正确
2. ✅ Gmail 用户启用"应用专用密码"
3. ✅ 检查防火墙是否阻止 SMTP 端口
4. ✅ 查看后端日志获取详细错误

### 5. 数据库连接失败

**解决方案：**
```bash
# 删除旧数据库文件
rm instance/flightfrd.db
# 或
rm *.db

# 重新运行应用初始化数据库
python run.py
```

### 6. 依赖安装失败

**问题：** 某些包安装时报错

**解决方案：**
```bash
# 升级构建工具
pip install --upgrade pip setuptools wheel

# 安装系统依赖 (Ubuntu/Debian)
sudo apt-get install python3-dev build-essential libssl-dev libffi-dev

# 重新安装
pip install -r requirements.txt
```

---

## 📦 生产部署建议

### 后端部署

1. **使用 Gunicorn 作为 WSGI 服务器：**
```bash
# 在虚拟环境中安装
pip install gunicorn

# 启动
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

2. **使用 Nginx 作为反向代理**

3. **使用 PostgreSQL/MySQL 替代 SQLite**

4. **配置 HTTPS**

5. **设置进程管理 (Supervisor/systemd)**

### 前端部署

1. **构建生产版本：**
```bash
npm run build
```

2. **使用 Nginx 托管 `dist/` 目录**

3. **配置 CDN 加速静态资源**

---

## 📞 获取帮助

如遇到问题：
1. 查看后端日志输出
2. 检查浏览器控制台错误
3. 确认环境变量配置正确
4. 确保虚拟环境已激活

---

**祝您部署顺利！** ✈️

如有问题，请通过 GitHub Issues 联系。
