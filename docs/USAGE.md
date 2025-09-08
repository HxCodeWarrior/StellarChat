# StellarChat 使用文档

## 1. 项目简介

StellarChat 是一个基于 StellarByte LLM 模型的现代化 Web 聊天应用。它提供了实时交互、流式响应和主题切换等功能，为用户带来快速响应的智能对话体验。

## 2. 环境准备

### 2.1 系统要求

- **操作系统**: Windows 10/11, macOS 10.15+, Linux (Ubuntu 20.04+/CentOS 8+)
- **内存**: 至少 8GB RAM (推荐 16GB+)
- **存储**: 至少 10GB 可用磁盘空间
- **Python**: 3.8 或更高版本
- **Node.js**: 16 或更高版本
- **Docker**: 20.10 或更高版本 (可选，用于容器化部署)

### 2.2 依赖组件

- **后端**: FastAPI, Transformers, PyTorch, Prometheus Client
- **前端**: React 18, TypeScript, Vite, Tailwind CSS
- **模型**: StellarByte LLM 模型文件 (需单独获取)

## 3. 快速开始

### 3.1 获取代码

```bash
git clone https://github.com/your-username/StellarChat.git
cd StellarChat
```

### 3.2 配置模型

1. 获取 StellarByte LLM 模型文件
2. 将模型文件放置在 `backend/models/test/SmolLM-135M-Instruct/` 目录下
3. 或者通过环境变量 `MODEL_PATH` 指定模型路径

### 3.3 启动服务

#### 方式一：直接运行 (开发模式)

1. 启动后端服务：
```bash
# 进入后端目录
cd backend

# 安装依赖
pip install -r requirements.txt

# 启动服务
python app/main.py
```

2. 启动前端服务：
```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

3. 访问应用：打开浏览器访问 `http://localhost:5173`

#### 方式二：Docker 运行 (推荐)

```bash
# 构建并启动所有服务
docker-compose up --build

# 后台运行
docker-compose up --build -d
```

访问应用：打开浏览器访问 `http://localhost:5173`

## 4. 开发指南

### 4.1 后端开发

#### 项目结构
```
backend/
├── app/                 # 应用代码
│   ├── main.py          # 应用入口
│   ├── routers/         # 路由模块
│   ├── models/          # 模型处理
│   ├── services/        # 业务逻辑
│   ├── config.py        # 配置文件
│   └── utils.py         # 工具函数
├── requirements.txt     # 依赖列表
├── Dockerfile           # Docker 镜像配置
└── run.sh               # 启动脚本
```

#### 添加新接口

1. 在 `app/routers/` 目录下创建新的路由文件
2. 在 `app/main.py` 中注册路由
3. 实现业务逻辑

#### 配置说明

环境变量配置：
- `MODEL_PATH`: 模型文件路径 (默认: ./models/test/SmolLM-135M-Instruct)
- `HOST`: 服务监听地址 (默认: 0.0.0.0)
- `PORT`: 服务监听端口 (默认: 8080)

### 4.2 前端开发

#### 项目结构
```
frontend/
├── src/                 # 源代码
│   ├── components/      # 组件
│   ├── hooks/           # 自定义 Hooks
│   ├── routes/          # 路由配置
│   ├── services/        # API 服务
│   ├── store/           # 状态管理
│   ├── styles/          # 样式文件
│   ├── types/           # 类型定义
│   ├── utils/           # 工具函数
│   ├── views/           # 页面视图
│   ├── App.tsx          # 根组件
│   └── main.tsx         # 入口文件
├── public/              # 静态资源
├── package.json         # 依赖和脚本
└── vite.config.ts       # 构建配置
```

#### 开发命令

```bash
# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 代码检查
npm run lint

# 预览生产构建
npm run preview
```

#### 添加新组件

1. 在 `src/components/` 对应目录下创建组件文件
2. 在页面或父组件中引入并使用

### 4.3 模型配置

#### 模型加载

模型在应用启动时自动加载，支持以下特性：
- 自动设备检测 (CPU/GPU)
- 自动精度选择 (FP32/FP16)
- 单例模式避免重复加载

#### 模型替换

1. 准备新的模型文件
2. 修改 `MODEL_PATH` 环境变量指向新模型路径
3. 重启服务

## 5. API 使用

### 5.1 HTTP API

后端提供 RESTful API 接口，支持以下功能：
- 健康检查: `GET /api/health`
- 模型列表: `GET /api/models`
- 聊天完成: `POST /api/chat/completions` (支持流式和非流式)
- 监控指标: `GET /metrics`

详细接口文档请参考 `docs/API.md` 文件。

### 5.2 WebSocket API

后端提供 WebSocket 接口用于实时聊天：
- 连接地址: `WebSocket /api/ws/chat`
- 支持标准化事件流格式

## 6. 部署指南

### 6.1 生产环境部署

#### Docker 部署 (推荐)

1. 构建镜像：
```bash
# 构建后端镜像
docker build -t stellar-chat-backend backend/

# 构建前端镜像
docker build -t stellar-chat-frontend frontend/
```

2. 运行容器：
```bash
# 运行后端
docker run -d -p 8080:8080 --name backend stellar-chat-backend

# 运行前端
docker run -d -p 80:80 --name frontend stellar-chat-frontend
```

#### 直接部署

1. 后端部署：
```bash
# 安装依赖
pip install -r backend/requirements.txt

# 启动服务
MODEL_PATH=/path/to/model HOST=0.0.0.0 PORT=8080 python backend/app/main.py
```

2. 前端部署：
```bash
# 构建生产版本
cd frontend
npm run build

# 将 dist/ 目录内容部署到 Web 服务器
```

### 6.2 环境变量配置

生产环境建议通过环境变量配置：

```bash
# 后端环境变量
MODEL_PATH=/path/to/your/model
HOST=0.0.0.0
PORT=8080

# 前端环境变量 (构建时)
VITE_API_URL=https://your-api-domain.com
```

### 6.3 监控与日志

#### 监控指标

访问 `/metrics` 端点获取 Prometheus 监控指标：
- 请求总数
- 请求延迟分布

#### 日志查看

```bash
# Docker 环境查看日志
docker logs backend
docker logs frontend

# 直接运行查看日志
# 日志输出到标准输出，可根据系统配置进行收集
```

## 7. 故障排除

### 7.1 常见问题

#### 1. 模型加载失败
- 检查模型文件是否存在且完整
- 确认 `MODEL_PATH` 环境变量配置正确
- 检查系统内存是否充足

#### 2. 前端无法连接后端
- 检查后端服务是否正常运行
- 确认 CORS 配置是否正确
- 检查网络连接和防火墙设置

#### 3. 响应速度慢
- 检查硬件资源使用情况
- 确认是否使用 GPU 加速
- 调整模型参数 (如 max_new_tokens)

### 7.2 日志分析

查看日志定位问题：
```bash
# 查看后端日志
tail -f backend/logs/app.log

# 查看 Docker 容器日志
docker logs -f backend
```

## 8. 性能优化建议

### 8.1 模型优化
- 使用模型量化减少内存占用
- 启用 GPU 加速提升推理速度
- 调整生成参数平衡质量和速度

### 8.2 系统优化
- 使用反向代理 (如 Nginx) 提升并发处理能力
- 配置缓存减少重复计算
- 启用 Gzip 压缩减少网络传输

## 9. 安全建议

### 9.1 访问控制
- 配置防火墙限制访问来源
- 使用 HTTPS 加密传输
- 实施 API 限流防止滥用

### 9.2 数据安全
- 避免在日志中记录敏感信息
- 定期更新依赖组件修复安全漏洞
- 实施输入验证防止注入攻击

## 10. 版本升级

### 10.1 升级步骤
1. 备份当前配置和数据
2. 拉取最新代码
3. 更新依赖
4. 重启服务

### 10.2 兼容性说明
- 注意查看版本更新日志
- 重大版本升级可能需要迁移数据
- 建议在测试环境验证后再升级生产环境

## 11. 联系支持

如遇到问题或有任何建议，请通过以下方式联系我们：
- 提交 GitHub Issues
- 发送邮件至 support@stellarbyte.com