"""
日志系统 - 生产级日志配置
"""
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from datetime import datetime


def setup_logger(name: str = "generator", log_level: str = "INFO") -> logging.Logger:
    """
    配置日志器
    
    特性:
    - 同时输出到控制台和文件
    - 文件自动轮转 (最大10MB, 保留5个)
    - 结构化日志格式
    """
    logger = logging.getLogger(name)
    
    # 避免重复添加handler
    if logger.handlers:
        return logger
    
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # 日志格式
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器
    log_dir = Path(__file__).parent.parent.parent / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    file_handler = RotatingFileHandler(
        log_dir / f"{name}.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger


# 默认日志器
logger = setup_logger()


def log_generation_start(module_id: str, project_id: str, config: dict):
    """记录生成开始"""
    logger.info(f"开始生成 | module={module_id} | project_id={project_id} | config={config}")


def log_generation_success(module_id: str, project_id: str, files_count: int, duration: float):
    """记录生成成功"""
    logger.info(f"生成成功 | module={module_id} | project_id={project_id} | files={files_count} | duration={duration:.2f}s")


def log_generation_error(module_id: str, project_id: str, error: str):
    """记录生成失败"""
    logger.error(f"生成失败 | module={module_id} | project_id={project_id} | error={error}")
