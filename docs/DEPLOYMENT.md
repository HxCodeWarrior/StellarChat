# 操作部署文档

## 1. 环境要求

- Python 3.8+
- pip 20.0+
- SQLite (默认数据库)
- 至少4GB内存 (推荐8GB)
- 至少2GB磁盘空间

## 2. 本地部署

### 2.1 克隆代码库

```bash
git clone <repository-url>
cd StellarChat/backend
```

### 2.2 安装依赖

```bash
pip install -r requirements.txt
```

### 2.3 数据库初始化

```bash
python init_db.py
```

这将创建SQLite数据库文件 `chat_history.db` 并初始化所需的表结构。

### 2.4 模型准备

1. 下载模型文件到 `models/test/SmolLM-135M-Instruct` 目录
2. 或通过环境变量 `MODEL_PATH` 指定模型路径

### 2.5 启动服务

#### 开发环境

Linux/Mac:
```bash
./run.sh
```

Windows:
```cmd
run.bat
```

#### 生产环境

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080 --workers 4
```

服务启动后，默认访问地址:
- API基础路径: http://localhost:8080/api
- Swagger文档: http://localhost:8080/api/docs
- ReDoc文档: http://localhost:8080/api/redoc

## 3. Docker部署

### 3.1 构建Docker镜像

```bash
docker build -t stellar-chat-backend .
```

### 3.2 运行容器

```bash
docker run -d -p 8080:8000 --name stellar-chat-backend stellar-chat-backend
```

### 3.3 挂载卷 (可选)

```bash
docker run -d -p 8080:8000 \
  -v ./models:/app/models \
  -v ./logs:/app/logs \
  -v ./chat_history.db:/app/chat_history.db \
  --name stellar-chat-backend \
  stellar-chat-backend
```

## 4. 环境变量配置

| 变量名 | 默认值 | 描述 |
|--------|--------|------|
| `HOST` | "0.0.0.0" | 服务监听地址 |
| `PORT` | 8080 | 服务监听端口 |
| `MODEL_PATH` | "./models/test/SmolLM-135M-Instruct" | 模型文件路径 |
| `DATABASE_URL` | "sqlite:///./chat_history.db" | 数据库连接URL |
| `LOG_LEVEL` | "INFO" | 日志级别 |
| `LOG_FILE` | "logs/app.log" | 日志文件路径 |

## 5. 监控和日志

### 5.1 Prometheus监控

Prometheus监控指标可通过 `/metrics` 端点访问:
```
http://localhost:8080/metrics
```

### 5.2 日志查看

日志文件默认保存在 `logs/app.log`，可通过以下方式查看:

```bash
# 实时查看日志
tail -f logs/app.log

# 查看最近100行日志
tail -n 100 logs/app.log
```

## 6. 测试

### 6.1 运行单元测试

```bash
cd tests
pip install -r requirements.txt
python -m pytest
```

### 6.2 API测试

使用curl测试API:

```bash
# 健康检查
curl http://localhost:8080/api/health

# 获取模型列表
curl http://localhost:8080/api/models
```

## 7. 故障排除

### 7.1 常见问题

1. **端口被占用**
   - 修改 `PORT` 环境变量或命令行参数
   - 使用 `lsof -i :8080` (Linux/Mac) 或 `netstat -ano | findstr :8080` (Windows) 查找占用进程

2. **模型加载失败**
   - 检查模型路径是否正确
   - 确认模型文件完整性
   - 查看日志文件获取详细错误信息

3. **数据库连接失败**
   - 检查 `DATABASE_URL` 环境变量
   - 确认数据库服务是否正常运行
   - 验证数据库文件权限

### 7.2 日志分析

通过日志可以诊断大部分问题:
- ERROR级别日志表示严重错误
- WARNING级别日志表示潜在问题
- INFO级别日志记录正常操作流程

## 8. 性能优化建议

1. **模型优化**
   - 使用量化模型减少内存占用
   - 考虑使用更小的模型以提高响应速度

2. **数据库优化**
   - 定期清理过期会话数据
   - 为常用查询字段添加索引

3. **服务配置**
   - 根据硬件资源调整worker数量
   - 合理设置日志级别以减少I/O开销