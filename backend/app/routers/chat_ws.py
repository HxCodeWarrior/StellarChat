import uuid
import json
import time
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from app.models.schemas import (
    ChatWebSocketMessage,
    SessionStartEvent,
    ContentBlockStartEvent,
    ContentBlockDeltaEvent,
    ContentBlockStopEvent,
    MessageDeltaEvent,
    MessageStopEvent,
    ErrorEvent,
    ChatMessage
)
from app.services.chat_service import ChatService
from app.utils import get_logger

router = APIRouter()
logger = get_logger()
chat_service = ChatService()


@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """WebSocket聊天接口"""
    await websocket.accept()
    session_id = str(uuid.uuid4())
    logger.info(f"新建WebSocket会话: {session_id}")
    
    try:
        # 发送会话开始事件
        await websocket.send_text(
            json.dumps(SessionStartEvent(
                data={"session_id": session_id}
            ).model_dump())
        )
        
        while True:
            # 接收客户端消息
            data = await websocket.receive_text()
            message = ChatWebSocketMessage.model_validate_json(data)
            
            if message.type == "chat.message":
                logger.info(f"[{session_id}] 收到消息: {message.content}")
                
                try:
                    # 发送内容块开始事件
                    await websocket.send_text(
                        json.dumps(ContentBlockStartEvent(
                            data={"type": "text", "index": 0}
                        ).model_dump())
                    )
                    
                    # 转换为消息格式
                    messages = [ChatMessage(role="user", content=message.content)]
                    
                    # 流式生成回复
                    token_count = 0
                    async for token in chat_service.generate_stream(messages):
                        if token:  # 只发送非空token
                            # 发送内容块增量事件
                            await websocket.send_text(
                                json.dumps(ContentBlockDeltaEvent(
                                    data={
                                        "index": 0,
                                        "delta": {
                                            "type": "text_delta",
                                            "text": token
                                        }
                                    }
                                ).model_dump())
                            )
                            token_count += 1
                    
                    # 发送内容块结束事件
                    await websocket.send_text(
                        json.dumps(ContentBlockStopEvent(
                            data={"index": 0}
                        ).model_dump())
                    )
                    
                    # 发送消息增量事件（包含使用量统计）
                    await websocket.send_text(
                        json.dumps(MessageDeltaEvent(
                            data={
                                "delta": {"finish_reason": "stop"},
                                "usage": {"output_tokens": token_count}
                            }
                        ).model_dump())
                    )
                    
                    # 发送消息结束事件
                    await websocket.send_text(
                        json.dumps(MessageStopEvent(
                            data={}
                        ).model_dump())
                    )
                    
                except Exception as e:
                    logger.error(f"[{session_id}] 处理消息时出错: {str(e)}")
                    # 发送错误事件
                    await websocket.send_text(
                        json.dumps(ErrorEvent(
                            data={"type": "server_error", "message": "处理消息时出错"}
                        ).model_dump())
                    )
                    
    except WebSocketDisconnect:
        logger.info(f"WebSocket会话断开: {session_id}")
    except Exception as e:
        logger.error(f"WebSocket会话错误: {str(e)}")
        # 尝试发送错误事件
        try:
            await websocket.send_text(
                json.dumps(ErrorEvent(
                    data={"type": "server_error", "message": "服务器内部错误"}
                ).model_dump())
            )
        except:
            pass