"""
代码生成引擎 - 核心生成逻辑
"""
from pathlib import Path
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader
import shutil
import os

from app.core.modules.student_management import StudentManagementGenerator
from app.core.modules.library_management import LibraryManagementGenerator
from app.core.modules.hotel_management import HotelManagementGenerator
from app.core.modules.ecommerce import EcommerceGenerator
from app.core.modules.blog_system import BlogSystemGenerator
from app.core.modules.data_visualization import DataVisualizationGenerator
from app.core.modules.algorithm_experiment import AlgorithmExperimentGenerator


class GeneratorEngine:
    """代码生成引擎"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent.parent
        self.templates_dir = self.base_dir / "templates"
        self.output_dir = self.base_dir.parent / "output"
        
        # 确保输出目录存在
        self.output_dir.mkdir(exist_ok=True)
        
        # 模块生成器映射
        self.generators = {
            "student_management": StudentManagementGenerator(),
            "library_management": LibraryManagementGenerator(),
            "hotel_management": HotelManagementGenerator(),
            "ecommerce": EcommerceGenerator(),
            "blog_system": BlogSystemGenerator(),
            "data_visualization": DataVisualizationGenerator(),
            "algorithm_experiment": AlgorithmExperimentGenerator(),
        }
    
    async def generate(self, module_id: str, config: Dict[str, Any], project_id: str) -> Dict[str, Any]:
        """
        生成项目
        
        Args:
            module_id: 模块ID
            config: 用户配置
            project_id: 项目唯一ID
            
        Returns:
            生成结果
        """
        try:
            # 获取对应的生成器
            generator = self.generators.get(module_id)
            if not generator:
                return {"success": False, "error": f"未知的模块: {module_id}"}
            
            # 创建项目输出目录
            project_dir = self.output_dir / project_id
            project_dir.mkdir(exist_ok=True)
            
            # 调用具体生成器
            result = await generator.generate(
                config=config,
                output_dir=project_dir,
                templates_dir=self.templates_dir
            )
            
            if result["success"]:
                # 打包为ZIP
                zip_path = self.output_dir / f"{project_id}"
                shutil.make_archive(str(zip_path), 'zip', project_dir)
                
                # 统计文件数量
                files_count = sum(1 for _ in project_dir.rglob("*") if _.is_file())
                result["files_count"] = files_count
            
            return result
            
        except Exception as e:
            return {"success": False, "error": str(e)}
