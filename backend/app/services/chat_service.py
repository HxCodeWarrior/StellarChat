from fastapi import HTTPException
import asyncio
import json
import time
from app.models.inference import LLMInference
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
from app.services.database_service import DatabaseService
from app.utils import get_logger, generate_id, format_timestamp

logger = get_logger()
llm = LLMInference()
database_service = DatabaseService()


class ChatService:
    """聊天服务类"""
    
    async def generate_completion(self, request: ChatCompletionRequest, session_id: str = None, db = None) -> ChatCompletionResponse:
        """生成聊天完成响应"""
        try:
            # 记录开始时间
            start_time = time.time()
            
            # 生成回复
            response_text = llm.chat(
                messages=request.messages,
                max_new_tokens=request.max_tokens or 150,
                temperature=request.temperature,
                top_p=request.top_p
            )
            
            # 计算耗时
            elapsed_time = time.time() - start_time
            
            # 计算token数量（简化计算）
            prompt_tokens = sum(len(msg.content) if isinstance(msg.content, str) else sum(len(item.text) for item in msg.content if item.type == "text" and item.text) for msg in request.messages)
            completion_tokens = len(response_text)
            total_tokens = prompt_tokens + completion_tokens
            
            # 如果提供了会话ID且有数据库连接，将消息保存到数据库
            if session_id and db:
                # 保存用户消息
                for msg in request.messages:
                    database_service.add_message(
                        db, 
                        session_id, 
                        msg.role, 
                        msg.content, 
                        len(msg.content) if isinstance(msg.content, str) else 0
                    )
                
                # 保存AI回复
                database_service.add_message(
                    db, 
                    session_id, 
                    "assistant", 
                    response_text, 
                    completion_tokens
                )
            
            # 构造响应
            response = ChatCompletionResponse(
                id=generate_id("chatcmpl-"),
                created=format_timestamp(),
                model=request.model,
                choices=[
                    ChatCompletionChoice(
                        index=0,
                        message=ChatMessage(role="assistant", content=response_text),
                        finish_reason="stop"
                    )
                ],
                usage=ChatCompletionUsage(
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    total_tokens=total_tokens
                )
            )
            
            logger.info(f"聊天完成生成成功 - 耗时: {elapsed_time:.4f}s, tokens: {total_tokens}")
            return response
            
        except Exception as e:
            logger.error(f"生成聊天完成响应失败: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail="生成聊天完成响应失败")

    async def generate_streaming_response(self, request: ChatCompletionRequest):
        """生成流式响应"""
        try:
            # 生成唯一ID
            completion_id = generate_id("chatcmpl-")
            created = format_timestamp()
            
            # 发送初始块
            first_chunk = ChatCompletionChunk(
                id=completion_id,
                created=created,
                model=request.model,
                choices=[
                    ChatCompletionChunkChoice(
                        index=0,
                        delta=ChatCompletionChunkDelta(role="assistant", content=""),
                        finish_reason=None
                    )
                ]
            )
            yield f"data: {json.dumps(first_chunk.model_dump())}\n\n"
            
            # 流式生成回复
            token_count = 0
            async for token in llm.stream_chat(
                messages=request.messages,
                max_new_tokens=request.max_tokens or 150,
                temperature=request.temperature,
                top_p=request.top_p
            ):
                if token:  # 只发送非空token
                    chunk = ChatCompletionChunk(
                        id=completion_id,
                        created=created,
                        model=request.model,
                        choices=[
                            ChatCompletionChunkChoice(
                                index=0,
                                delta=ChatCompletionChunkDelta(content=token),
                                finish_reason=None
                            )
                        ]
                    )
                    yield f"data: {json.dumps(chunk.model_dump())}\n\n"
                    token_count += 1
            
            # 发送结束块
            final_chunk = ChatCompletionChunk(
                id=completion_id,
                created=created,
                model=request.model,
                choices=[
                    ChatCompletionChunkChoice(
                        index=0,
                        delta=ChatCompletionChunkDelta(),
                        finish_reason="stop"
                    )
                ]
            )
            yield f"data: {json.dumps(final_chunk.model_dump())}\n\n"
            
            # 发送结束标记
            yield "data: [DONE]\n\n"
            
            logger.info(f"流式响应生成完成 - tokens: {token_count}")
            
        except Exception as e:
            logger.error(f"生成流式响应失败: {str(e)}", exc_info=True)
            error_chunk = {
                "error": {
                    "type": "server_error",
                    "message": "生成流式响应失败",
                    "param": None,
                    "code": "server_error"
                }
            }
            yield f"data: {json.dumps(error_chunk)}\n\n"
            yield "data: [DONE]\n\n"

    async def generate_stream(self, messages):
        """生成流式回复（用于WebSocket）"""
        try:
            # 流式生成回复
            async for token in llm.stream_chat(messages=messages):
                yield token
                
        except Exception as e:
            logger.error(f"生成流式回复失败: {str(e)}", exc_info=True)
            raise