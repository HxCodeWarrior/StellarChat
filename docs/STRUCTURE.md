# StellarChat 项目结构介绍

## 项目概述

StellarChat 是一个基于 StellarByte LLM 模型的现代化 Web 聊天应用。它结合了 React 和 FastAPI，提供实时交互、流式响应和主题切换等功能，为用户带来快速响应的体验。

## 整体目录结构

```
StellarChat/
│
├── backend/                   # 后端服务（加载 LLM 权重，提供 API 接口）
│   ├── app/
│   │   ├── main.py            # FastAPI 入口文件
│   │   ├── routers/
│   │   │   ├── chat_ws.py     # WebSocket 聊天接口
│   │   │   ├── chat.py        # HTTP 聊天接口
│   │   │   ├── health.py      # 健康检查接口
│   │   ├── models/
│   │   │   ├── inference.py   # LLM 推理逻辑
│   │   │   ├── tokenizer.py   # 分词与预处理
│   │   ├── config.py          # 配置文件（模型路径、端口等）
│   │   └── utils.py           # 工具函数（日志等）
│   ├── requirements.txt       # 后端依赖
│   ├── Dockerfile             # 后端容器化部署文件
│   └── run.sh                 # 启动脚本
│
├── frontend/                  # 前端（精美聊天网页）
│   ├── public/
│   │   └── index.html         # 页面模板
│   ├── src/
│   │   ├── components/
│   │   │   ├── chat/          # 聊天相关组件
│   │   │   ├── common/        # 通用组件
│   │   │   ├── layout/        # 布局组件
│   │   │   └── settings/      # 设置相关组件
│   │   ├── hooks/             # 自定义 React Hooks
│   │   ├── routes/            # 路由配置
│   │   ├── services/          # API 服务层
│   │   ├── store/             # 状态管理
│   │   ├── styles/            # 样式文件
│   │   ├── types/             # TypeScript 类型定义
│   │   ├── utils/             # 工具函数
│   │   ├── views/             # 页面视图
│   │   ├── App.tsx            # React 根组件
│   │   └── main.tsx           # 前端入口
│   ├── package.json           # 前端依赖
│   ├── vite.config.ts         # Vite 配置
│   └── tsconfig.json          # TypeScript 配置
│
├── docs/                      # 项目文档
│   ├── project_structure.md   # 项目结构介绍（本文档）
│   ├── design.md              # 设计文档
│   ├── api.md                 # API 接口文档
│   └── usage.md               # 使用文档
│
├── docker-compose.yml         # 前后端一键部署配置
└── README.md                  # 项目总体说明
```

## 后端结构详解

### 核心模块

1. **main.py** - 应用入口
   - 初始化 FastAPI 应用
   - 配置 CORS 跨域支持
   - 集成 Prometheus 监控指标
   - 注册路由模块
   - 添加全局异常处理

2. **routers/** - 路由模块
   - `chat.py`: 提供 HTTP 聊天接口
   - `chat_ws.py`: 提供 WebSocket 实时聊天接口
   - `health.py`: 提供健康检查接口

3. **models/** - 模型处理
   - `inference.py`: LLM 模型加载和推理逻辑，支持流式输出
   - `tokenizer.py`: 文本分词和预处理

4. **config.py** - 配置管理
   - 项目基本信息配置
   - 模型路径、主机地址、端口等环境变量配置

5. **utils.py** - 工具函数
   - 日志配置和获取

## 前端结构详解

### 核心目录

1. **components/** - 组件库
   - 按功能划分的组件目录，便于维护和复用
   - `chat/`: 聊天相关组件（待开发）
   - `common/`: 通用组件（待开发）
   - `layout/`: 布局组件（待开发）
   - `settings/`: 设置相关组件（待开发）

2. **hooks/** - 自定义 Hooks
   - 封装可复用的业务逻辑（待开发）

3. **routes/** - 路由配置
   - 页面路由映射关系（待开发）

4. **services/** - API 服务层
   - 封装后端 API 调用（待开发）

5. **store/** - 状态管理
   - 全局状态管理（待开发）

6. **styles/** - 样式文件
   - 全局样式和主题配置（待开发）

7. **types/** - TypeScript 类型定义
   - 项目中使用的类型定义（待开发）

8. **utils/** - 工具函数
   - 通用工具函数，如国际化支持（待开发）

9. **views/** - 页面视图
   - 完整页面组件（待开发）

## 文档结构

项目文档位于 `docs/` 目录下，包含以下内容：
- 项目结构介绍（本文档）
- 设计文档
- API 接口文档
- 使用文档

## 部署配置

- **docker-compose.yml**: 用于一键部署前后端服务的 Docker Compose 配置文件
- **backend/Dockerfile**: 后端服务的 Docker 镜像构建文件
- **frontend/**: 前端项目配置文件（Vite、TypeScript 等）

这个结构设计遵循了现代 Web 应用开发的最佳实践，前后端分离清晰，模块化程度高，便于团队协作开发和后期维护。