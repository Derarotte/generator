"""
模板管理API - 管理代码模板
"""
from fastapi import APIRouter
from typing import List
from pydantic import BaseModel

router = APIRouter()


class TemplateInfo(BaseModel):
    """模板信息"""
    id: str
    name: str
    description: str
    category: str
    file_count: int


@router.get("/", response_model=List[TemplateInfo])
async def get_all_templates():
    """获取所有可用模板"""
    # TODO: 从模板目录读取
    return [
        TemplateInfo(
            id="springboot_vue",
            name="Spring Boot + Vue 全栈模板",
            description="前后端分离的企业级应用模板",
            category="Web应用",
            file_count=50
        ),
        TemplateInfo(
            id="flask_vue",
            name="Flask + Vue 全栈模板",
            description="轻量级Python全栈模板",
            category="Web应用",
            file_count=30
        ),
        TemplateInfo(
            id="cpp_console",
            name="C++控制台应用模板",
            description="标准C++控制台程序模板",
            category="控制台应用",
            file_count=10
        ),
    ]
