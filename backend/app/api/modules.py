"""
模块管理 API - 从模板加载器获取模块列表
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel

from app.core.engine import GeneratorEngine

router = APIRouter()
engine = GeneratorEngine()


class ModuleResponse(BaseModel):
    id: str
    name: str
    description: str
    version: str
    icon: str
    category: str
    tech_stack: List[str]
    fields: List[Dict[str, Any]]


@router.get("/", response_model=List[ModuleResponse])
async def get_all_modules():
    """获取所有可用模块"""
    modules = engine.get_modules()
    return [
        ModuleResponse(
            id=m.id,
            name=m.name,
            description=m.description,
            version=m.version,
            icon=m.icon,
            category=m.category,
            tech_stack=m.tech_stack,
            fields=[f.model_dump() for f in m.fields]
        )
        for m in modules
    ]


@router.get("/categories")
async def get_categories():
    """获取所有分类"""
    modules = engine.get_modules()
    categories = list(set(m.category for m in modules))
    return {"categories": categories}


@router.get("/{module_id}")
async def get_module(module_id: str):
    """获取单个模块详情"""
    module = engine.get_module(module_id)
    if not module:
        raise HTTPException(status_code=404, detail=f"模块不存在: {module_id}")
    
    return {
        "id": module.id,
        "name": module.name,
        "description": module.description,
        "version": module.version,
        "icon": module.icon,
        "category": module.category,
        "tech_stack": module.tech_stack,
        "fields": [f.model_dump() for f in module.fields],
        "files_count": len(module.files)
    }
