"""
中国学生作业代码生成器 - FastAPI 后端主入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.api import generator, modules, templates, internal

app = FastAPI(
    title="中国学生作业代码生成器",
    description="模块化学生作业代码生成系统，支持多种作业类型一键生成",
    version="1.0.0"
)

# 配置CORS，允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册API路由
app.include_router(generator.router, prefix="/api/generator", tags=["生成器"])
app.include_router(modules.router, prefix="/api/modules", tags=["模块管理"])
app.include_router(templates.router, prefix="/api/templates", tags=["模板管理"])
app.include_router(internal.router, prefix="/api/internal", tags=["内部测试"])

# 静态文件服务（生成的输出）
output_path = Path(__file__).parent.parent.parent / "output"
output_path.mkdir(exist_ok=True)
app.mount("/output", StaticFiles(directory=str(output_path)), name="output")


@app.get("/")
async def root():
    """API根路径"""
    return {
        "message": "中国学生作业代码生成器 API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}
