"""
配置管理 - 生产级配置系统
"""
from pathlib import Path
from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    """应用配置"""
    
    # 应用信息
    APP_NAME: str = "中国学生作业代码生成器"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = True
    
    # 路径配置
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    TEMPLATES_DIR: Path = BASE_DIR / "templates"
    OUTPUT_DIR: Path = BASE_DIR / "output"
    DATA_DIR: Path = BASE_DIR / "data"
    
    # 数据库
    DATABASE_URL: str = "sqlite:///./data/history.db"
    
    # 生成配置
    MAX_CONCURRENT_GENERATIONS: int = 5
    OUTPUT_RETENTION_DAYS: int = 7
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()


# 确保必要目录存在
def init_directories():
    """初始化目录结构"""
    settings = get_settings()
    settings.TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
    settings.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
    (settings.BASE_DIR / "logs").mkdir(parents=True, exist_ok=True)
