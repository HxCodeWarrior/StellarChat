from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.models.database import get_db, APIKeyModel
from app.models.schemas import APIKeyCreate, APIKeyResponse, APIKeyCreateResponse, APIKeyListResponse
from app.utils import get_logger
import uuid

router = APIRouter()
logger = get_logger()

@router.post("/api-keys", response_model=APIKeyCreateResponse)
async def create_api_key(api_key_data: APIKeyCreate, db: Session = Depends(get_db)):
    """创建新的API Key"""
    try:
        # 生成新的API Key
        key = APIKeyModel.generate_key()
        
        # 创建API Key记录
        db_api_key = APIKeyModel(
            id=str(uuid.uuid4()),
            name=api_key_data.name,
            key=key
        )
        
        # 保存到数据库
        db.add(db_api_key)
        db.commit()
        db.refresh(db_api_key)
        
        # 返回API Key信息（包含key本身，仅在创建时返回）
        return APIKeyCreateResponse(
            id=db_api_key.id,
            name=db_api_key.name,
            created_at=db_api_key.created_at,
            is_active=db_api_key.is_active,
            key=key
        )
    except Exception as e:
        logger.error(f"创建API Key失败: {str(e)}")
        raise HTTPException(status_code=500, detail="创建API Key失败")

@router.get("/api-keys", response_model=APIKeyListResponse)
async def list_api_keys(db: Session = Depends(get_db)):
    """获取API Key列表"""
    try:
        api_keys = db.query(APIKeyModel).all()
        return APIKeyListResponse(
            data=[
                APIKeyResponse(
                    id=key.id,
                    name=key.name,
                    created_at=key.created_at,
                    is_active=key.is_active
                )
                for key in api_keys
            ]
        )
    except Exception as e:
        logger.error(f"获取API Key列表失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取API Key列表失败")

@router.delete("/api-keys/{key_id}")
async def delete_api_key(key_id: str, db: Session = Depends(get_db)):
    """删除API Key"""
    try:
        api_key = db.query(APIKeyModel).filter(APIKeyModel.id == key_id).first()
        if not api_key:
            raise HTTPException(status_code=404, detail="API Key不存在")
        
        db.delete(api_key)
        db.commit()
        return {"message": "API Key删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除API Key失败: {str(e)}")
        raise HTTPException(status_code=500, detail="删除API Key失败")

@router.post("/api-keys/{key_id}/deactivate")
async def deactivate_api_key(key_id: str, db: Session = Depends(get_db)):
    """停用API Key"""
    try:
        api_key = db.query(APIKeyModel).filter(APIKeyModel.id == key_id).first()
        if not api_key:
            raise HTTPException(status_code=404, detail="API Key不存在")
        
        api_key.is_active = False
        db.commit()
        return {"message": "API Key已停用"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"停用API Key失败: {str(e)}")
        raise HTTPException(status_code=500, detail="停用API Key失败")

@router.post("/api-keys/{key_id}/activate")
async def activate_api_key(key_id: str, db: Session = Depends(get_db)):
    """启用API Key"""
    try:
        api_key = db.query(APIKeyModel).filter(APIKeyModel.id == key_id).first()
        if not api_key:
            raise HTTPException(status_code=404, detail="API Key不存在")
        
        api_key.is_active = True
        db.commit()
        return {"message": "API Key已启用"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"启用API Key失败: {str(e)}")
        raise HTTPException(status_code=500, detail="启用API Key失败")