"""
生成器 API - 项目生成和下载
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Any
from pathlib import Path

from app.core.engine import GeneratorEngine
from app.config import get_settings

router = APIRouter()
engine = GeneratorEngine()
settings = get_settings()


class GenerateRequest(BaseModel):
    module_id: str
    config: Dict[str, Any] = {}


@router.post("/generate")
async def generate_project(request: GenerateRequest):
    """生成项目"""
    result = await engine.generate(
        module_id=request.module_id,
        config=request.config
    )
    return result.to_dict()


@router.get("/download/{project_id}")
async def download_project(project_id: str):
    """下载生成的项目ZIP"""
    zip_path = settings.OUTPUT_DIR / f"{project_id}.zip"
    
    if not zip_path.exists():
        raise HTTPException(status_code=404, detail="项目不存在或已过期")
    
    return FileResponse(
        path=str(zip_path),
        filename=f"{project_id}.zip",
        media_type="application/zip"
    )


@router.get("/preview/{project_id}")
async def preview_project(project_id: str):
    """预览项目文件结构"""
    project_dir = settings.OUTPUT_DIR / project_id
    
    if not project_dir.exists():
        raise HTTPException(status_code=404, detail="项目不存在")
    
    files = []
    for item in project_dir.rglob("*"):
        rel_path = item.relative_to(project_dir)
        files.append({
            "path": str(rel_path),
            "name": item.name,
            "type": "directory" if item.is_dir() else "file",
            "size": item.stat().st_size if item.is_file() else None
        })
    
    return {
        "project_id": project_id,
        "files": sorted(files, key=lambda x: (x["type"] == "file", x["path"]))
    }
