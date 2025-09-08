import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime


class Settings:
    # 项目配置
    PROJECT_NAME: str = "StellarByte LLM Chat Backend"
    VERSION: str = "1.0.0"
    
    # 模型配置
    MODEL_PATH: str = os.getenv("MODEL_PATH", "./models/test/SmolLM-135M-Instruct")
    
    # 服务器配置
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8080))
    
    # 日志配置
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/app.log")
    LOG_MAX_BYTES: int = int(os.getenv("LOG_MAX_BYTES", 10485760))  # 10MB
    LOG_BACKUP_COUNT: int = int(os.getenv("LOG_BACKUP_COUNT", 5))
    
    # API配置
    API_PREFIX: str = "/api"


# 创建全局配置实例
settings = Settings()


def setup_logging():
    """设置日志配置"""
    # 创建日志目录
    log_dir = os.path.dirname(settings.LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 配置日志格式
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # 创建logger
    logger = logging.getLogger("llm-backend")
    logger.setLevel(settings.LOG_LEVEL)
    
    # 创建文件处理器
    file_handler = RotatingFileHandler(
        settings.LOG_FILE,
        maxBytes=settings.LOG_MAX_BYTES,
        backupCount=settings.LOG_BACKUP_COUNT,
        encoding="utf-8"
    )
    file_handler.setLevel(settings.LOG_LEVEL)
    file_formatter = logging.Formatter(log_format)
    file_handler.setFormatter(file_formatter)
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(settings.LOG_LEVEL)
    console_formatter = logging.Formatter(log_format)
    console_handler.setFormatter(console_formatter)
    console_handler.stream.reconfigure(encoding="utf-8")
    
    # 添加处理器到logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


# 初始化日志
setup_logging()