import asyncio
import uuid
import json
import time
from fastapi import APIRouter, HTTPException
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
from app.utils import get_logger

router = APIRouter()
logger = get_logger()
chat_service = ChatService()





@router.post("/chat/completions", response_model=ChatCompletionResponse)
async def create_chat_completion(request: ChatCompletionRequest):
    """创建聊天完成"""
    try:
        # 检查模型是否存在
        if request.model != "stellar-byte-llm":
            raise HTTPException(status_code=400, detail="模型不存在")
        
        # 如果启用流式输出，返回流式响应
        if request.stream:
            return StreamingResponse(
                chat_service.generate_streaming_response(request),
                media_type="text/event-stream"
            )
        
        # 非流式输出
        return await chat_service.generate_completion(request)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"聊天完成处理失败: {str(e)}")
        raise HTTPException(status_code=500, detail="聊天完成处理失败")