from fastapi import APIRouter
from app.models.schemas import ModelListResponse, ModelInfo
import time

router = APIRouter()


@router.get("/models", response_model=ModelListResponse)
async def list_models():
    """获取可用模型列表"""
    models = [
        ModelInfo(
            id="stellar-byte-llm",
            created=int(time.time()),
            owned_by="stellar-byte"
        )
    ]
    return ModelListResponse(data=models)