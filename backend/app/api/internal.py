"""
内部测试 API
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any

from app.core.engine import GeneratorEngine

router = APIRouter()
engine = GeneratorEngine()


class QuickTestRequest(BaseModel):
    module_id: str = "student_management"
    config: Dict[str, Any] = {}


@router.get("/status")
async def get_status():
    """系统状态"""
    modules = engine.get_modules()
    return {
        "status": "online",
        "modules_count": len(modules),
        "modules": [{"id": m.id, "name": m.name} for m in modules]
    }


@router.post("/quick-gen")
async def quick_generate(request: QuickTestRequest):
    """快速测试生成"""
    result = await engine.generate(
        module_id=request.module_id,
        config=request.config
    )
    return result.to_dict()
