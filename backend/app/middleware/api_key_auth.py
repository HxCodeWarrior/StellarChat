from fastapi import HTTPException, Request, Depends
from sqlalchemy.orm import Session
from app.models.database import get_db, APIKeyModel
from app.utils import get_logger

logger = get_logger()

async def verify_api_key(request: Request, db: Session = Depends(get_db)):
    """验证API Key的中间件"""
    # 获取Authorization头
    auth_header = request.headers.get("Authorization")
    
    if not auth_header:
        logger.warning("缺少Authorization头")
        raise HTTPException(status_code=401, detail="缺少Authorization头")
    
    # 检查Bearer token格式
    if not auth_header.startswith("Bearer "):
        logger.warning("无效的Authorization头格式")
        raise HTTPException(status_code=401, detail="无效的Authorization头格式")
    
    # 提取API Key
    api_key = auth_header.split(" ")[1]
    
    # 在数据库中查找API Key
    db_api_key = db.query(APIKeyModel).filter(APIKeyModel.key == api_key).first()
    
    if not db_api_key:
        logger.warning("无效的API Key")
        raise HTTPException(status_code=401, detail="无效的API Key")
    
    if not db_api_key.is_active:
        logger.warning("API Key已被停用")
        raise HTTPException(status_code=401, detail="API Key已被停用")
    
    # 将API Key信息添加到请求状态中
    request.state.api_key = db_api_key