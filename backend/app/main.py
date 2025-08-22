from fastapi import FastAPI
from app.config import settings
from app.routers import health ,chat ,chat_ws
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

# 跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(health.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(chat_ws.router, prefix="/api")
