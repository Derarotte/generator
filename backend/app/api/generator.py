"""
代码生成API - 根据模块和配置生成完整项目
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Any
from pathlib import Path
import shutil
import uuid
import asyncio

from app.core.engine import GeneratorEngine

router = APIRouter()


class GenerateRequest(BaseModel):
    """生成请求"""
    module_id: str
    config: Dict[str, Any]


class GenerateResponse(BaseModel):
    """生成响应"""
    success: bool
    message: str
    project_id: str | None = None
    download_url: str | None = None
    files_count: int = 0


# 生成引擎实例
engine = GeneratorEngine()


@router.post("/generate", response_model=GenerateResponse)
async def generate_project(request: GenerateRequest):
    """生成项目"""
    try:
        # 生成唯一项目ID
        project_id = str(uuid.uuid4())[:8]
        
        # 调用生成引擎
        result = await engine.generate(
            module_id=request.module_id,
            config=request.config,
            project_id=project_id
        )
        
        if result["success"]:
            return GenerateResponse(
                success=True,
                message=f"项目生成成功！",
                project_id=project_id,
                download_url=f"/api/generator/download/{project_id}",
                files_count=result.get("files_count", 0)
            )
        else:
            return GenerateResponse(
                success=False,
                message=result.get("error", "生成失败"),
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/{project_id}")
async def download_project(project_id: str):
    """下载生成的项目（ZIP格式）"""
    output_dir = Path(__file__).parent.parent.parent.parent / "output"
    zip_path = output_dir / f"{project_id}.zip"
    
    if not zip_path.exists():
        raise HTTPException(status_code=404, detail="项目不存在或已过期")
    
    return FileResponse(
        path=str(zip_path),
        filename=f"homework_project_{project_id}.zip",
        media_type="application/zip"
    )


@router.get("/preview/{project_id}")
async def preview_project(project_id: str):
    """预览生成的项目文件结构"""
    output_dir = Path(__file__).parent.parent.parent.parent / "output" / project_id
    
    if not output_dir.exists():
        raise HTTPException(status_code=404, detail="项目不存在")
    
    def get_tree(path: Path, prefix: str = "") -> list:
        """获取目录树结构"""
        items = []
        entries = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name))
        
        for i, entry in enumerate(entries):
            is_last = i == len(entries) - 1
            current_prefix = "└── " if is_last else "├── "
            
            if entry.is_dir():
                items.append({
                    "type": "directory",
                    "name": entry.name,
                    "path": str(entry.relative_to(output_dir)),
                })
                # 递归获取子目录
                child_items = get_tree(entry)
                items.extend(child_items)
            else:
                items.append({
                    "type": "file",
                    "name": entry.name,
                    "path": str(entry.relative_to(output_dir)),
                    "size": entry.stat().st_size,
                })
        
        return items
    
    tree = get_tree(output_dir)
    return {"project_id": project_id, "files": tree}


@router.delete("/clean/{project_id}")
async def clean_project(project_id: str):
    """清理生成的项目"""
    output_dir = Path(__file__).parent.parent.parent.parent / "output"
    project_dir = output_dir / project_id
    zip_path = output_dir / f"{project_id}.zip"
    
    if project_dir.exists():
        shutil.rmtree(project_dir)
    if zip_path.exists():
        zip_path.unlink()
    
    return {"success": True, "message": "项目已清理"}
