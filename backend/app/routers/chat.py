from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.models.inference import LLMInference
from app.models.schemas import ChatMessage

router = APIRouter()
llm = LLMInference()  # 初始化模型（可替换成单例模式）


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # 转换为消息格式
        messages = [ChatMessage(role="user", content=request.message)]
        
        # 生成回复
        reply = llm.chat(messages=messages)
        return ChatResponse(reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理聊天请求失败: {str(e)}")