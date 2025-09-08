import asyncio
import uuid
import json
import time
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from app.models.schemas import (
    ChatCompletionRequest, 
    ChatCompletionResponse, 
    ChatCompletionChoice, 
    ChatCompletionUsage,
    ChatMessage,
    ChatCompletionChunk,
    ChatCompletionChunkChoice,
    ChatCompletionChunkDelta
)
from app.services.chat_service import ChatService
from app.models.database import get_db
from app.services.database_service import DatabaseService
from app.utils import get_logger

router = APIRouter()
logger = get_logger()
chat_service = ChatService()
database_service = DatabaseService()





@router.post("/chat/completions", response_model=ChatCompletionResponse)
async def create_chat_completion(
    request: ChatCompletionRequest,
    session_id: str = Query(None, description="会话ID，用于保存聊天历史")
):
    """创建聊天完成"""
    try:
        # 检查模型是否存在
        if request.model != "stellar-byte-llm":
            raise HTTPException(status_code=400, detail="模型不存在")
        
        # 如果提供了会话ID，获取会话历史并合并到请求中
        db = next(get_db())
        try:
            if session_id:
                # 获取会话历史
                session_history = database_service.get_messages_as_chat_history(db, session_id)
                # 合并历史和当前请求消息
                full_messages = session_history + request.messages
                # 更新请求消息
                request.messages = full_messages
            
            # 如果启用流式输出，返回流式响应
            if request.stream:
                return StreamingResponse(
                    chat_service.generate_streaming_response(request),
                    media_type="text/event-stream"
                )
            
            # 非流式输出
            return await chat_service.generate_completion(request, session_id, db)
        finally:
            db.close()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"聊天完成处理失败: {str(e)}")
        raise HTTPException(status_code=500, detail="聊天完成处理失败")