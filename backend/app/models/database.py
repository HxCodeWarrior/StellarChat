from sqlalchemy import create_engine, Column, String, Text, DateTime, Boolean, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from typing import Optional
from datetime import datetime
import json
from app.config import settings

Base = declarative_base()

class SessionModel(Base):
    """会话模型"""
    __tablename__ = 'sessions'
    
    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # 关联消息
    messages = relationship("MessageModel", back_populates="session", cascade="all, delete-orphan")


class MessageModel(Base):
    """消息模型"""
    __tablename__ = 'messages'
    
    id = Column(String, primary_key=True, index=True)
    session_id = Column(String, ForeignKey('sessions.id'), nullable=False)
    role = Column(String, nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False, index=True)
    tokens = Column(Integer, default=0)
    metadata_info = Column(Text)  # JSON格式存储额外信息
    
    # 关联回话
    session = relationship("SessionModel", back_populates="messages")


# 数据库引擎和会话工厂
# 从配置中读取数据库URL
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """创建所有表"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()