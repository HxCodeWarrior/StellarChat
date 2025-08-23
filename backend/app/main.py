from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.config import settings
from app.routers import health ,chat ,chat_ws
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, Histogram
from prometheus_client import make_asgi_app

# 监控指标
REQUEST_COUNT = Counter("requests_total", "Total API requests", ["method", "endpoint"])
REQUEST_LATENCY = Histogram("request_latency_seconds", "Request latency", ["endpoint"])


app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

# 跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "message": "服务器内部错误"}
    )

# Prometheus metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# 注册路由
app.include_router(health.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(chat_ws.router, prefix="/api")
