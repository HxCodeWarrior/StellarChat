# 后端应用架构文档

## 1. 概述

StellarByte LLM Chat Backend 是一个基于 FastAPI 的后端服务，提供聊天完成、会话管理和模型管理等功能。该应用使用 SQLite 作为数据库存储聊天历史，并集成了大型语言模型进行对话生成。

## 2. 技术栈

- **框架**: FastAPI
- **数据库**: SQLite (通过 SQLAlchemy ORM)
- **模型推理**: Transformers (Hugging Face)
- **监控**: Prometheus
- **日志**: Python logging with RotatingFileHandler
- **测试**: pytest

## 3. 项目结构

```
backend/
├── app/                    # 主应用目录
│   ├── __init__.py         # 包初始化文件
│   ├── config.py           # 配置管理
│   ├── main.py             # 应用入口点
│   ├── utils.py            # 工具函数
│   ├── models/             # 数据模型和Schema定义
│   │   ├── __init__.py
│   │   ├── database.py     # 数据库模型
│   │   ├── schemas.py      # Pydantic模型
│   │   ├── inference.py    # 模型推理相关
│   │   └── tokenizer.py    # 分词器相关
│   ├── routers/            # API路由
│   │   ├── __init__.py
│   │   ├── health.py       # 健康检查
│   │   ├── models.py       # 模型管理
│   │   ├── chat_completions.py  # 聊天完成API
│   │   ├── chat_ws.py      # WebSocket聊天
│   │   └── sessions.py     # 会话管理
│   └── services/           # 业务逻辑层
│       ├── __init__.py
│       ├── chat_service.py     # 聊天服务
│       └── database_service.py # 数据库服务
├── logs/                   # 日志目录
├── models/                 # 模型文件目录
│   └── test/               # 测试模型
├── tests/                  # 测试文件
├── chat_history.db         # SQLite数据库文件
├── init_db.py              # 数据库初始化脚本
├── requirements.txt        # Python依赖
└── run.sh                  # 启动脚本
```

## 4. 核心组件

### 4.1 应用入口 (main.py)

- 创建 FastAPI 应用实例
- 配置 CORS 中间件
- 注册路由
- 设置全局异常处理
- 配置 Prometheus 监控指标
- 实现请求日志记录中间件

### 4.2 配置管理 (config.py)

- 管理应用配置参数
- 设置日志配置
- 定义数据库连接URL
- 配置模型路径和服务器参数

### 4.3 数据库模型 (models/database.py)

- 定义 SessionModel 和 MessageModel
- 创建数据库引擎和会话工厂
- 提供数据库会话管理器

### 4.4 Schema定义 (models/schemas.py)

- 定义请求和响应的数据模型
- 包括聊天消息、完成请求、模型信息等Pydantic模型

### 4.5 路由 (routers/)

- **health.py**: 健康检查端点
- **models.py**: 模型列表端点
- **chat_completions.py**: 聊天完成API (REST)
- **chat_ws.py**: WebSocket聊天接口
- **sessions.py**: 会话管理API

### 4.6 服务层 (services/)

- **chat_service.py**: 处理聊天生成逻辑
- **database_service.py**: 封装数据库操作

## 5. 数据流

1. 用户通过 REST API 或 WebSocket 连接到应用
2. 请求被路由到相应的处理函数
3. 服务层处理业务逻辑
4. 数据库服务处理数据持久化
5. 聊天服务与模型交互生成回复
6. 响应返回给用户

## 6. 监控和日志

- 使用 Prometheus 收集API请求指标
- 通过 Python logging 模块记录应用日志
- 日志同时输出到文件和控制台
- 支持日志轮转以防止文件过大