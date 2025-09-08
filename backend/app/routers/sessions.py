from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.models.database import get_db, create_tables
from app.services.database_service import DatabaseService
from app.models.schemas import ChatMessage

router = APIRouter()
database_service = DatabaseService()

# 在应用启动时创建表
create_tables()

class SessionCreate(BaseModel):
    title: str

class SessionUpdate(BaseModel):
    title: str

class SessionResponse(BaseModel):
    id: str
    title: str
    created_at: str
    updated_at: str
    is_active: bool

class MessageCreate(BaseModel):
    role: str
    content: str
    tokens: int = 0
    metadata_info: dict = None

class MessageResponse(BaseModel):
    id: str
    session_id: str
    role: str
    content: str
    created_at: str
    tokens: int
    metadata_info: dict = None

@router.post("/sessions", response_model=SessionResponse)
def create_session(session_data: SessionCreate, db: Session = Depends(get_db)):
    """创建新会话"""
    try:
        db_session = database_service.create_session(db, session_data.title)
        return SessionResponse(
            id=db_session.id,
            title=db_session.title,
            created_at=db_session.created_at.isoformat(),
            updated_at=db_session.updated_at.isoformat(),
            is_active=db_session.is_active
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建会话失败: {str(e)}")

@router.get("/sessions", response_model=List[SessionResponse])
def get_sessions(skip: int = 0, limit: int = 100, active_only: bool = True, db: Session = Depends(get_db)):
    """获取会话列表"""
    try:
        sessions = database_service.get_sessions(db, skip, limit, active_only)
        return [
            SessionResponse(
                id=s.id,
                title=s.title,
                created_at=s.created_at.isoformat(),
                updated_at=s.updated_at.isoformat(),
                is_active=s.is_active
            )
            for s in sessions
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取会话列表失败: {str(e)}")

@router.get("/sessions/{session_id}", response_model=SessionResponse)
def get_session(session_id: str, db: Session = Depends(get_db)):
    """获取会话详情"""
    try:
        db_session = database_service.get_session(db, session_id)
        if not db_session:
            raise HTTPException(status_code=404, detail="会话不存在")
        return SessionResponse(
            id=db_session.id,
            title=db_session.title,
            created_at=db_session.created_at.isoformat(),
            updated_at=db_session.updated_at.isoformat(),
            is_active=db_session.is_active
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取会话详情失败: {str(e)}")

@router.put("/sessions/{session_id}", response_model=SessionResponse)
def update_session(session_id: str, session_data: SessionUpdate, db: Session = Depends(get_db)):
    """更新会话"""
    try:
        db_session = database_service.update_session(db, session_id, session_data.title)
        if not db_session:
            raise HTTPException(status_code=404, detail="会话不存在")
        return SessionResponse(
            id=db_session.id,
            title=db_session.title,
            created_at=db_session.created_at.isoformat(),
            updated_at=db_session.updated_at.isoformat(),
            is_active=db_session.is_active
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新会话失败: {str(e)}")

@router.delete("/sessions/{session_id}")
def delete_session(session_id: str, db: Session = Depends(get_db)):
    """删除会话"""
    try:
        success = database_service.delete_session(db, session_id)
        if not success:
            raise HTTPException(status_code=404, detail="会话不存在")
        return {"message": "会话删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除会话失败: {str(e)}")

@router.post("/sessions/{session_id}/messages", response_model=MessageResponse)
def add_message(session_id: str, message_data: MessageCreate, db: Session = Depends(get_db)):
    """添加消息到会话"""
    try:
        db_message = database_service.add_message(
            db, 
            session_id, 
            message_data.role, 
            message_data.content, 
            message_data.tokens,
            message_data.metadata_info
        )
        if not db_message:
            raise HTTPException(status_code=404, detail="会话不存在")
        return MessageResponse(
            id=db_message.id,
            session_id=db_message.session_id,
            role=db_message.role,
            content=db_message.content,
            created_at=db_message.created_at.isoformat(),
            tokens=db_message.tokens,
            metadata_info=db_message.metadata_info
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"添加消息失败: {str(e)}")

@router.get("/sessions/{session_id}/messages", response_model=List[MessageResponse])
def get_messages(session_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取会话消息"""
    try:
        # 验证会话是否存在
        db_session = database_service.get_session(db, session_id)
        if not db_session:
            raise HTTPException(status_code=404, detail="会话不存在")
            
        messages = database_service.get_messages(db, session_id, skip, limit)
        return [
            MessageResponse(
                id=m.id,
                session_id=m.session_id,
                role=m.role,
                content=m.content,
                created_at=m.created_at.isoformat(),
                tokens=m.tokens,
                metadata_info=m.metadata_info
            )
            for m in messages
        ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取消息失败: {str(e)}")

@router.get("/sessions/{session_id}/history", response_model=List[ChatMessage])
def get_chat_history(session_id: str, db: Session = Depends(get_db)):
    """获取会话聊天历史（用于模型推理）"""
    try:
        # 验证会话是否存在
        db_session = database_service.get_session(db, session_id)
        if not db_session:
            raise HTTPException(status_code=404, detail="会话不存在")
            
        return database_service.get_messages_as_chat_history(db, session_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取聊天历史失败: {str(e)}")