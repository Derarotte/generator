"""
生成引擎 v2.0 - 模板驱动架构
"""
from pathlib import Path
from typing import Dict, Any, Optional
import shutil
import time
import uuid

from app.core.template_loader import TemplateLoader
from app.core.renderer import TemplateRenderer
from app.utils.logger import logger, log_generation_start, log_generation_success, log_generation_error
from app.config import get_settings


class GenerationResult:
    """生成结果"""
    def __init__(
        self,
        success: bool,
        project_id: str,
        message: str = "",
        files_count: int = 0,
        output_path: Optional[Path] = None,
        zip_path: Optional[Path] = None,
        duration: float = 0.0,
        error: Optional[str] = None
    ):
        self.success = success
        self.project_id = project_id
        self.message = message
        self.files_count = files_count
        self.output_path = output_path
        self.zip_path = zip_path
        self.duration = duration
        self.error = error
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "project_id": self.project_id,
            "message": self.message,
            "files_count": self.files_count,
            "output_path": str(self.output_path) if self.output_path else None,
            "download_url": f"/api/generator/download/{self.project_id}" if self.success else None,
            "duration": round(self.duration, 2),
            "error": self.error
        }


class GeneratorEngine:
    """
    生成引擎 v2.0
    
    核心能力:
    1. 从YAML配置加载模块定义
    2. 使用Jinja2渲染模板
    3. 自动打包为ZIP
    4. 完整的日志追踪
    """
    
    def __init__(self):
        self.settings = get_settings()
        
        # 确保目录存在
        self.settings.TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
        self.settings.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        # 初始化组件
        self.template_loader = TemplateLoader(self.settings.TEMPLATES_DIR)
        self.renderer = TemplateRenderer(self.settings.TEMPLATES_DIR)
        
        logger.info(f"生成引擎初始化完成，加载了 {len(self.template_loader.get_all_modules())} 个模块")
    
    async def generate(
        self,
        module_id: str,
        config: Dict[str, Any],
        project_id: Optional[str] = None
    ) -> GenerationResult:
        """
        生成项目
        
        Args:
            module_id: 模块ID
            config: 用户配置
            project_id: 项目ID（可选，自动生成）
            
        Returns:
            GenerationResult
        """
        start_time = time.time()
        project_id = project_id or str(uuid.uuid4())[:8]
        
        log_generation_start(module_id, config, project_id)
        
        try:
            # 1. 获取模块定义
            module = self.template_loader.get_module(module_id)
            if not module:
                return GenerationResult(
                    success=False,
                    project_id=project_id,
                    error=f"模块不存在: {module_id}"
                )
            
            # 2. 验证和补全配置
            context = self._build_context(module, config)
            
            # 3. 创建输出目录
            output_dir = self.settings.OUTPUT_DIR / project_id
            if output_dir.exists():
                shutil.rmtree(output_dir)
            output_dir.mkdir(parents=True)
            
            # 4. 渲染模板
            generated_files = []
            
            # 遍历模块目录下的所有模板子目录
            for template_subdir in ["backend", "frontend", "database", "docs"]:
                source_dir = module.module_path / template_subdir
                if source_dir.exists():
                    files = self.renderer.render_directory(
                        source_dir=source_dir,
                        target_dir=output_dir / template_subdir,
                        context=context,
                        module_path=module.module_path
                    )
                    generated_files.extend(files)
            
            # 5. 生成README
            readme_template = module.module_path / "README.md.j2"
            if readme_template.exists():
                readme_content = self.renderer.render_file(
                    readme_template, context, module.module_path
                )
                (output_dir / "README.md").write_text(readme_content, encoding="utf-8")
                generated_files.append(output_dir / "README.md")
            
            # 6. 打包ZIP
            zip_path = self.settings.OUTPUT_DIR / f"{project_id}.zip"
            shutil.make_archive(str(zip_path.with_suffix("")), "zip", output_dir)
            
            duration = time.time() - start_time
            log_generation_success(module_id, project_id, len(generated_files), duration)
            
            return GenerationResult(
                success=True,
                project_id=project_id,
                message=f"成功生成 {module.name}",
                files_count=len(generated_files),
                output_path=output_dir,
                zip_path=zip_path,
                duration=duration
            )
            
        except Exception as e:
            duration = time.time() - start_time
            error_msg = str(e)
            log_generation_error(module_id, project_id, error_msg)
            
            return GenerationResult(
                success=False,
                project_id=project_id,
                message="生成失败",
                duration=duration,
                error=error_msg
            )
    
    def _build_context(self, module, config: Dict[str, Any]) -> Dict[str, Any]:
        """构建渲染上下文"""
        context = {}
        
        # 1. 填充默认值
        for field in module.fields:
            if field.default is not None:
                context[field.name] = field.default
        
        # 2. 覆盖用户配置
        context.update(config)
        
        # 3. 添加计算属性
        if "package_name" in context:
            context["package_path"] = context["package_name"].replace(".", "/")
        
        # 4. 添加元信息
        context["_module"] = {
            "id": module.id,
            "name": module.name,
            "version": module.version
        }
        
        from datetime import datetime
        context["_generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return context
    
    def get_modules(self):
        """获取所有可用模块"""
        return self.template_loader.get_all_modules()
    
    def get_module(self, module_id: str):
        """获取指定模块"""
        return self.template_loader.get_module(module_id)
    
    def reload_templates(self):
        """重新加载模板"""
        self.template_loader.reload()
