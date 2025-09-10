import uuid
import json
import time
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Query
from fastapi.websockets import WebSocket as WebSocketType
from sqlalchemy.orm import Session
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
from app.models.database import get_db, APIKeyModel
from app.services.database_service import DatabaseService
from app.utils import get_logger

router = APIRouter()
logger = get_logger()
chat_service = ChatService()
database_service = DatabaseService()


async def get_api_key_from_websocket(websocket: WebSocketType):
    """从WebSocket连接中获取并验证API Key"""
    # 获取Authorization头
    auth_header = websocket.headers.get("Authorization")
    
    if not auth_header:
        logger.warning("WebSocket连接缺少Authorization头")
        await websocket.close(code=4000, reason="缺少Authorization头")
        return None
    
    # 检查Bearer token格式
    if not auth_header.startswith("Bearer "):
        logger.warning("WebSocket连接无效的Authorization头格式")
        await websocket.close(code=4000, reason="无效的Authorization头格式")
        return None
    
    # 提取API Key
    api_key = auth_header.split(" ")[1]
    
    # 获取数据库连接
    db = next(get_db())
    
    try:
        # 在数据库中查找API Key
        db_api_key = db.query(APIKeyModel).filter(APIKeyModel.key == api_key).first()
        
        if not db_api_key:
            logger.warning("WebSocket连接无效的API Key")
            await websocket.close(code=4000, reason="无效的API Key")
            return None
        
        if not db_api_key.is_active:
            logger.warning("WebSocket连接API Key已被停用")
            await websocket.close(code=4000, reason="API Key已被停用")
            return None
        
        return db_api_key
    finally:
        db.close()


@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket, session_id: str = Query(None, description="会话ID，用于保存聊天历史")):
    """WebSocket聊天接口"""
    # 验证API Key
    api_key = await get_api_key_from_websocket(websocket)
    if not api_key:
        return
    
    await websocket.accept()
    
    # 如果没有提供会话ID，则生成一个新的
    if not session_id:
        session_id = str(uuid.uuid4())
    
    logger.info(f"新建WebSocket会话: {session_id}")
    
    # 获取数据库连接
    db = next(get_db())
    
    try:
        # 发送会话开始事件
        await websocket.send_text(
            json.dumps(SessionStartEvent(
                data={"session_id": session_id}
            ).model_dump())
        )
        
        # 如果提供了会话ID，获取会话历史
        if session_id:
            try:
                # 确保会话存在，如果不存在则创建
                db_session = database_service.get_session(db, session_id)
                if not db_session:
                    database_service.create_session(db, session_id, f"WebSocket会话 {session_id[:8]}")
            except Exception as e:
                logger.warning(f"创建会话失败: {str(e)}")
        
        while True:
            # 接收客户端消息
            data = await websocket.receive_text()
            message = ChatWebSocketMessage.model_validate_json(data)
            
            if message.type == "chat.message":
                logger.info(f"[{session_id}] 收到消息: {message.content}")
                
                try:
                    # 获取会话历史（如果有的话）
                    chat_history = []
                    if session_id:
                        try:
                            chat_history = database_service.get_messages_as_chat_history(db, session_id)
                        except Exception as e:
                            logger.warning(f"[{session_id}] 获取会话历史失败: {str(e)}")
                    
                    # 将新消息添加到历史中
                    messages = chat_history + [ChatMessage(role="user", content=message.content)]
                    
                    # 保存用户消息到数据库
                    if session_id:
                        try:
                            database_service.add_message(db, session_id, "user", message.content, len(message.content))
                        except Exception as e:
                            logger.warning(f"[{session_id}] 保存用户消息失败: {str(e)}")
                    
                    # 发送内容块开始事件
                    await websocket.send_text(
                        json.dumps(ContentBlockStartEvent(
                            data={"type": "text", "index": 0}
                        ).model_dump())
                    )
                    
                    # 流式生成回复
                    token_count = 0
                    assistant_response = ""
                    async for token in chat_service.generate_stream(messages):
                        if token:  # 只发送非空token
                            assistant_response += token
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
                    
                    # 保存AI回复到数据库
                    if session_id and assistant_response:
                        try:
                            database_service.add_message(db, session_id, "assistant", assistant_response, token_count)
                        except Exception as e:
                            logger.warning(f"[{session_id}] 保存AI回复失败: {str(e)}")
                    
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
    finally:
        db.close()