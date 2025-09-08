from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from app.models.database import SessionModel, MessageModel
from app.models.schemas import ChatMessage
from datetime import datetime
import uuid

class DatabaseService:
    """数据库服务类，提供会话和消息的CRUD操作"""
    
    def create_session(self, db: Session, title: str) -> SessionModel:
        """创建新会话"""
        session_id = str(uuid.uuid4())
        db_session = SessionModel(
            id=session_id,
            title=title
        )
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
        return db_session
    
    def get_sessions(self, db: Session, skip: int = 0, limit: int = 100, active_only: bool = True) -> List[SessionModel]:
        """获取会话列表"""
        query = db.query(SessionModel)
        if active_only:
            query = query.filter(SessionModel.is_active == True)
        return query.order_by(desc(SessionModel.updated_at)).offset(skip).limit(limit).all()
    
    def get_session(self, db: Session, session_id: str) -> Optional[SessionModel]:
        """获取会话详情"""
        return db.query(SessionModel).filter(SessionModel.id == session_id).first()
    
    def update_session(self, db: Session, session_id: str, title: str) -> Optional[SessionModel]:
        """更新会话"""
        db_session = self.get_session(db, session_id)
        if db_session:
            db_session.title = title
            db_session.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(db_session)
        return db_session
    
    def delete_session(self, db: Session, session_id: str) -> bool:
        """删除会话"""
        db_session = self.get_session(db, session_id)
        if db_session:
            db.delete(db_session)
            db.commit()
            return True
        return False
    
    def add_message(self, db: Session, session_id: str, role: str, content: str, tokens: int = 0, metadata: dict = None) -> Optional[MessageModel]:
        """添加消息"""
        # 验证会话是否存在
        session = self.get_session(db, session_id)
        if not session:
            return None
            
        message_id = str(uuid.uuid4())
        db_message = MessageModel(
            id=message_id,
            session_id=session_id,
            role=role,
            content=content,
            tokens=tokens,
            metadata_info=json.dumps(metadata) if metadata else None
        )
        db.add(db_message)
        # 更新会话的更新时间
        session.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_message)
        return db_message
    
    def get_messages(self, db: Session, session_id: str, skip: int = 0, limit: int = 100) -> List[MessageModel]:
        """获取会话消息"""
        return db.query(MessageModel).filter(MessageModel.session_id == session_id).order_by(MessageModel.created_at).offset(skip).limit(limit).all()
    
    def get_messages_as_chat_history(self, db: Session, session_id: str) -> List[ChatMessage]:
        """获取会话消息并转换为聊天历史格式"""
        messages = self.get_messages(db, session_id)
        chat_history = []
        for msg in messages:
            chat_history.append(ChatMessage(
                role=msg.role,
                content=msg.content
            ))
        return chat_history