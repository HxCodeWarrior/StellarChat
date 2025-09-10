from fastapi import APIRouter
from app.models.schemas import ModelListResponse, ModelInfo
import time

router = APIRouter()

# 定义支持的模型列表
SUPPORTED_MODELS = [
    {
        "id": "stellar-byte-llm",
        "owned_by": "stellar-byte"
    },
    {
        "id": "deepseek-ai/DeepSeek-R1",
        "owned_by": "deepseek-ai"
    },
    {
        "id": "deepseek-ai/DeepSeek-V3",
        "owned_by": "deepseek-ai"
    },
    {
        "id": "deepseek-ai/DeepSeek-V2.5",
        "owned_by": "deepseek-ai"
    },
    {
        "id": "Qwen/Qwen2.5-72B-Instruct-128K",
        "owned_by": "Qwen"
    },
    {
        "id": "Qwen/QwQ-32B-Preview",
        "owned_by": "Qwen"
    },
    {
        "id": "THUDM/glm-4-9b-chat",
        "owned_by": "THUDM"
    },
    {
        "id": "Pro/THUDM/glm-4-9b-chat",
        "owned_by": "THUDM"
    }
]


@router.get("/models", response_model=ModelListResponse)
async def list_models():
    """获取可用模型列表"""
    models = [
        ModelInfo(
            id=model["id"],
            created=int(time.time()),
            owned_by=model["owned_by"]
        )
        for model in SUPPORTED_MODELS
    ]
    return ModelListResponse(data=models)