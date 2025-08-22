from fastapi import APIRouter
from pydantic import BaseModel
from app.models.inference import LLMInference

router = APIRouter()
llm = LLMInference()  # 初始化模型（可替换成单例模式）

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    reply = llm.chat(request.message)
    return ChatResponse(reply=reply)
