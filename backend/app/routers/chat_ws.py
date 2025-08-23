import uuid
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.models.inference import LLMInference
from app.utils import get_logger

router = APIRouter()
logger = get_logger()
llm = LLMInference()

@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    session_id = str(uuid.uuid4())
    logger.info(f"新建会话: {session_id}")

    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"[{session_id}] 收到消息: {data}")

            async for chunk in llm.stream_chat(data):
                await websocket.send_json(chunk)

            await websocket.send_json({"event": "end"})
    except WebSocketDisconnect:
        logger.info(f"会话断开: {session_id}")
    except Exception as e:
        logger.error(f"会话错误: {str(e)}")
        await websocket.send_json({"error": str(e)})
