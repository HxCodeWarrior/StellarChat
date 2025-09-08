import logging
import time
import uuid
from functools import wraps
from app.config import settings


def get_logger():
    """获取logger实例"""
    return logging.getLogger("llm-backend")


def timing_decorator(func):
    """性能计时装饰器"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            return result
        finally:
            end_time = time.time()
            logger = get_logger()
            logger.info(f"{func.__name__} 执行时间: {end_time - start_time:.4f}秒")
    return wrapper


def generate_id(prefix: str = "") -> str:
    """生成唯一ID"""
    return f"{prefix}{uuid.uuid4().hex}"


def format_timestamp() -> int:
    """生成时间戳"""
    return int(time.time())