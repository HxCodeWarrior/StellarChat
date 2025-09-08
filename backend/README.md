# StellarChat 后端服务

## 目录结构

```
backend/
├── app/                    # 应用核心代码
│   ├── main.py            # FastAPI入口
│   ├── config.py          # 配置文件
│   ├── utils.py           # 工具函数
│   ├── models/            # 模型相关
│   │   ├── inference.py   # LLM推理逻辑
│   │   ├── tokenizer.py   # 分词器
│   │   └── database.py    # 数据库模型
│   ├── routers/           # API路由
│   │   ├── chat.py        # 聊天接口
│   │   ├── chat_ws.py     # WebSocket聊天接口
│   │   ├── chat_completions.py  # 兼容OpenAI的聊天完成接口
│   │   ├── health.py      # 健康检查接口
│   │   ├── models.py      # 模型接口
│   │   └── sessions.py    # 会话管理接口
│   └── services/          # 业务逻辑
│       ├── chat_service.py      # 聊天服务
│       └── database_service.py  # 数据库服务
├── models/                 # 模型文件
├── logs/                   # 日志文件
├── tests/                  # 测试文件
├── requirements.txt        # 依赖包
├── init_db.py             # 数据库初始化脚本
├── run.sh                 # Linux启动脚本
├── run.bat                # Windows启动脚本
└── Dockerfile             # Docker部署文件
```

## 环境要求

- Python 3.8+
- SQLite (默认) 或 PostgreSQL (可选)

## 安装依赖

```bash
pip install -r requirements.txt
```

## 数据库设置

### 初始化数据库

运行以下命令初始化数据库表结构：

```bash
python init_db.py
```

这将创建SQLite数据库文件 `chat_history.db` 并初始化所需的表结构。

### 数据库配置

数据库连接可以通过环境变量 `DATABASE_URL` 进行配置：

```bash
# SQLite (默认)
export DATABASE_URL=sqlite:///./chat_history.db

# PostgreSQL (可选)
export DATABASE_URL=postgresql://user:password@localhost/dbname
```

## 启动服务

### 开发环境

```bash
# Linux/Mac
./run.sh

# Windows
run.bat
```

### 生产环境

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080 --workers 4
```

## API文档

服务启动后，可以通过以下地址访问API文档：

- Swagger UI: http://localhost:8080/api/docs
- ReDoc: http://localhost:8080/api/redoc

## 监控

Prometheus监控指标可通过 `/metrics` 端点访问。

## 测试

运行测试：

```bash
cd tests
pip install -r requirements.txt
python -m unittest test_chat_completions.py
python -m unittest test_database_service.py
```