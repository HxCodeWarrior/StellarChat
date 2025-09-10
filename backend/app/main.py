import os
import sys
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, Histogram, make_asgi_app
from app.config import settings
from app.routers import health, models, chat_completions, chat_ws
from app.routers import sessions, api_keys
from app.utils import get_logger
import time

# 配置日志
logger = get_logger()

# 使用 lifespan 替代 on_event
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 应用启动事件
    logger.info(f"应用启动: {settings.PROJECT_NAME} v{settings.VERSION}")
    logger.info(f"模型路径: {settings.MODEL_PATH}")
    logger.info(f"监听地址: {settings.HOST}:{settings.PORT}")
    yield
    # 应用关闭事件
    logger.info("应用关闭")

# 监控指标
# 使用 prometheus_client 的 REGISTRY 来避免重复注册
from prometheus_client import REGISTRY

# 检查指标是否已注册，避免重复注册
try:
    REQUEST_COUNT = REGISTRY._names_to_collectors["api_requests_total"]
except KeyError:
    REQUEST_COUNT = Counter("api_requests_total", "Total API requests", ["method", "endpoint", "status"])

try:
    REQUEST_LATENCY = REGISTRY._names_to_collectors["api_request_latency_seconds"]
except KeyError:
    REQUEST_LATENCY = Histogram("api_request_latency_seconds", "Request latency", ["endpoint"])

# 创建FastAPI应用
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="StellarByte LLM Chat Backend API",
    docs_url=f"{settings.API_PREFIX}/docs",
    redoc_url=f"{settings.API_PREFIX}/redoc",
    lifespan=lifespan
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# 请求时间记录中间件
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    # 记录监控指标
    REQUEST_LATENCY.labels(endpoint=request.url.path).observe(process_time)
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    logger.info(f"{request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.4f}s")
    return response

# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"全局异常处理: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "type": "server_error",
                "message": "服务器内部错误",
                "param": None,
                "code": "server_error"
            }
        }
    )

# 404异常处理
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=404,
        content={
            "error": {
                "type": "not_found_error",
                "message": "请求的资源不存在",
                "param": None,
                "code": "not_found"
            }
        }
    )

# Prometheus metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# 注册路由
app.include_router(health.router, prefix=settings.API_PREFIX)
app.include_router(models.router, prefix=settings.API_PREFIX)
app.include_router(chat_completions.router, prefix=settings.API_PREFIX)
app.include_router(chat_ws.router, prefix=settings.API_PREFIX)
app.include_router(sessions.router, prefix=settings.API_PREFIX)
app.include_router(api_keys.router, prefix=settings.API_PREFIX)

# 添加根路径处理
@app.get("/")
async def root():
    return {"message": "StellarByte LLM Chat Backend is running here"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
        log_level=settings.LOG_LEVEL.lower()
    )