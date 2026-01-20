"""
中国学生作业代码生成器 - FastAPI 后端主入口
v2.0 - 生产级架构重构
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from app.api import generator, modules, templates, internal
from app.config import get_settings, init_directories
from app.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    logger.info("=" * 50)
    logger.info("中国学生作业代码生成器 v2.0 启动中...")
    init_directories()
    logger.info("目录初始化完成")
    logger.info("=" * 50)
    
    yield
    
    # 关闭时
    logger.info("应用关闭")


settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description="模块化学生作业代码生成系统，支持多种作业类型一键生成",
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# 配置CORS
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

# 静态文件服务
settings.OUTPUT_DIR.mkdir(exist_ok=True)
app.mount("/output", StaticFiles(directory=str(settings.OUTPUT_DIR)), name="output")


@app.get("/")
async def root():
    """API根路径"""
    return {
        "message": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION
    }
