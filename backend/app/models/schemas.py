from typing import List, Optional, Union, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class ChatMessageContentItem(BaseModel):
    type: str
    text: Optional[str] = None


class ChatMessage(BaseModel):
    role: str
    content: Union[str, List[ChatMessageContentItem]]


class ChatCompletionRequest(BaseModel):
    model: str = Field(default="stellar-byte-llm", description="模型名称")
    messages: List[ChatMessage] = Field(description="聊天消息历史")
    temperature: Optional[float] = Field(default=0.7, ge=0, le=2, description="采样温度")
    top_p: Optional[float] = Field(default=1.0, ge=0, le=1, description="核采样")
    max_tokens: Optional[int] = Field(default=None, gt=0, description="最大生成token数")
    stream: Optional[bool] = Field(default=False, description="是否启用流式输出")
    stop: Optional[Union[str, List[str]]] = Field(default=None, description="停止词")
    user: Optional[str] = Field(default=None, description="用户标识符")


class ChatCompletionChoice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: Optional[str]


class ChatCompletionUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[ChatCompletionChoice]
    usage: ChatCompletionUsage


class ChatCompletionChunkDelta(BaseModel):
    role: Optional[str] = None
    content: Optional[str] = None


class ChatCompletionChunkChoice(BaseModel):
    index: int
    delta: ChatCompletionChunkDelta
    finish_reason: Optional[str] = None


class ChatCompletionChunk(BaseModel):
    id: str
    object: str = "chat.completion.chunk"
    created: int
    model: str
    choices: List[ChatCompletionChunkChoice]


class ModelInfo(BaseModel):
    id: str
    object: str = "model"
    created: int
    owned_by: str


class ModelListResponse(BaseModel):
    object: str = "list"
    data: List[ModelInfo]


class ChatWebSocketMessage(BaseModel):
    type: str
    content: str


class SessionStartEvent(BaseModel):
    event: str = "session_start"
    data: Dict[str, str]


class ContentBlockStartEvent(BaseModel):
    event: str = "content_block_start"
    data: Dict[str, Union[str, int]]


class ContentBlockDeltaEvent(BaseModel):
    event: str = "content_block_delta"
    data: Dict[str, Union[int, Dict[str, str]]]


class ContentBlockStopEvent(BaseModel):
    event: str = "content_block_stop"
    data: Dict[str, int]


class MessageDeltaEvent(BaseModel):
    event: str = "message_delta"
    data: Dict[str, Union[Dict[str, str], Dict[str, int]]]


class MessageStopEvent(BaseModel):
    event: str = "message_stop"
    data: Dict[str, Any]


class ErrorEvent(BaseModel):
    event: str = "error"
    data: Dict[str, str]


# API Key管理相关的数据模型
class APIKeyCreate(BaseModel):
    name: str = Field(..., description="API Key名称")


class APIKeyResponse(BaseModel):
    id: str
    name: str
    created_at: datetime
    is_active: bool


class APIKeyListResponse(BaseModel):
    data: List[APIKeyResponse]