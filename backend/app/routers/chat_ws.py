from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.models.inference import LLMInference
from app.utils import get_logger

router = APIRouter()
logger = get_logger()
llm = LLMInference()

@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"收到消息: {data}")

            async for token in stream_reply(data):
                await websocket.send_text(token)

            await websocket.send_text("[END]")  # 表示结束
    except WebSocketDisconnect:
        logger.info("客户端断开连接")

async def stream_reply(prompt: str):
    for token in llm.stream_chat(prompt):
        yield token
