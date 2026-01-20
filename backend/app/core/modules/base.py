"""
生成器基类
"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader
import os


class BaseGenerator(ABC):
    """生成器基类"""
    
    def __init__(self):
        self.name = "基础生成器"
        self.description = ""
    
    @abstractmethod
    async def generate(self, config: Dict[str, Any], output_dir: Path, templates_dir: Path) -> Dict[str, Any]:
        """
        生成项目
        
        Args:
            config: 用户配置
            output_dir: 输出目录
            templates_dir: 模板目录
            
        Returns:
            生成结果 {"success": bool, "error": str | None}
        """
        pass
    
    def create_jinja_env(self, templates_dir: Path) -> Environment:
        """创建Jinja2环境"""
        return Environment(
            loader=FileSystemLoader(str(templates_dir)),
            trim_blocks=True,
            lstrip_blocks=True,
        )
    
    def write_file(self, path: Path, content: str):
        """写入文件，自动创建父目录"""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
    
    def copy_static(self, src: Path, dest: Path):
        """复制静态文件"""
        import shutil
        if src.is_dir():
            shutil.copytree(src, dest, dirs_exist_ok=True)
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
