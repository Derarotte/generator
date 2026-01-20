"""
内部测试 API - 用于终端调试和自动化测试
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import time

from app.core.engine import GeneratorEngine
from app.api.modules import AVAILABLE_MODULES

router = APIRouter()
engine = GeneratorEngine()

class QuickTestRequest(BaseModel):
    module_id: str = "student_management"
    config: Dict[str, Any] = {}

@router.get("/status")
async def get_system_status():
    """获取系统内部状态，用于心跳检查"""
    return {
        "status": "online",
        "timestamp": time.time(),
        "available_modules": [m.id for m in AVAILABLE_MODULES],
        "output_dir_exists": engine.output_dir.exists()
    }

@router.post("/quick-gen")
async def quick_generate_test(request: QuickTestRequest):
    """快速生成测试，返回文件的预览结构而非ZIP"""
    project_id = f"debug_{int(time.time())}"
    
    # 如果没传配置，使用各个模块的默认值
    if not request.config:
        module = next((m for m in AVAILABLE_MODULES if m.id == request.module_id), None)
        if module:
            request.config = {f.name: f.default for f in module.fields if f.default is not None}

    result = await engine.generate(
        module_id=request.module_id,
        config=request.config,
        project_id=project_id
    )
    
    if result["success"]:
        return {
            "success": True,
            "project_id": project_id,
            "files_count": result.get("files_count"),
            "test_path": str(engine.output_dir / project_id)
        }
    else:
        raise HTTPException(status_code=500, detail=result.get("error"))
