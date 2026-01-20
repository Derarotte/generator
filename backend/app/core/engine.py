"""
生成引擎 v2.0 - 使用文件映射方式
"""
from pathlib import Path
from typing import Dict, Any, Optional, List
import shutil
import time
import uuid
import re

from jinja2 import Environment, FileSystemLoader
from app.core.template_loader import TemplateLoader, ModuleDefinition
from app.utils.logger import logger
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
        duration: float = 0.0,
        error: Optional[str] = None
    ):
        self.success = success
        self.project_id = project_id
        self.message = message
        self.files_count = files_count
        self.output_path = output_path
        self.duration = duration
        self.error = error
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "project_id": self.project_id,
            "message": self.message,
            "files_count": self.files_count,
            "download_url": f"/api/generator/download/{self.project_id}" if self.success else None,
            "duration": round(self.duration, 2),
            "error": self.error
        }


class GeneratorEngine:
    """生成引擎"""
    
    def __init__(self):
        self.settings = get_settings()
        self.settings.TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
        self.settings.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        self.template_loader = TemplateLoader(self.settings.TEMPLATES_DIR)
        self._jinja_envs: Dict[str, Environment] = {}
        
        logger.info(f"生成引擎初始化完成，共 {len(self.template_loader.get_all_modules())} 个模块")
    
    def _get_jinja_env(self, module_path: Path) -> Environment:
        """获取Jinja2环境"""
        key = str(module_path)
        if key not in self._jinja_envs:
            env = Environment(
                loader=FileSystemLoader(str(module_path)),
                trim_blocks=True,
                lstrip_blocks=True,
                keep_trailing_newline=True
            )
            # 自定义过滤器
            env.filters["lower"] = str.lower
            env.filters["upper"] = str.upper
            self._jinja_envs[key] = env
        return self._jinja_envs[key]
    
    def _render_path(self, path_template: str, context: Dict[str, Any]) -> str:
        """渲染路径中的变量"""
        # 处理 {{ variable }} 形式
        def replace(match):
            expr = match.group(1).strip()
            # 简单变量
            if expr in context:
                return str(context[expr])
            # 带过滤器 如 package_name | replace(".", "/")
            if "|" in expr:
                var, *filters = [p.strip() for p in expr.split("|")]
                value = context.get(var, "")
                for f in filters:
                    if "replace" in f:
                        # 提取 replace(".", "/")
                        m = re.search(r'replace\(["\'](.+?)["\']\s*,\s*["\'](.+?)["\']\)', f)
                        if m:
                            value = value.replace(m.group(1), m.group(2))
                return str(value)
            return match.group(0)
        
        return re.sub(r'\{\{\s*(.+?)\s*\}\}', replace, path_template)
    
    async def generate(
        self,
        module_id: str,
        config: Dict[str, Any],
        project_id: Optional[str] = None
    ) -> GenerationResult:
        """生成项目"""
        start_time = time.time()
        project_id = project_id or str(uuid.uuid4())[:8]
        
        logger.info(f"开始生成: module={module_id}, project_id={project_id}")
        
        try:
            # 1. 获取模块
            module = self.template_loader.get_module(module_id)
            if not module:
                return GenerationResult(
                    success=False,
                    project_id=project_id,
                    error=f"模块不存在: {module_id}"
                )
            
            # 2. 构建上下文
            context = self._build_context(module, config)
            
            # 3. 创建输出目录
            output_dir = self.settings.OUTPUT_DIR / project_id
            if output_dir.exists():
                shutil.rmtree(output_dir)
            output_dir.mkdir(parents=True)
            
            # 4. 获取Jinja环境
            env = self._get_jinja_env(module.module_path)
            
            # 5. 渲染所有文件
            generated_files = []
            
            for file_mapping in module.files:
                source_path = file_mapping.source
                target_path = self._render_path(file_mapping.target, context)
                
                source_file = module.module_path / source_path
                target_file = output_dir / target_path
                
                if not source_file.exists():
                    logger.warning(f"模板不存在: {source_path}")
                    continue
                
                # 确保目标目录存在
                target_file.parent.mkdir(parents=True, exist_ok=True)
                
                # 渲染模板
                try:
                    template = env.get_template(source_path)
                    content = template.render(**context)
                    target_file.write_text(content, encoding="utf-8")
                    generated_files.append(target_file)
                    logger.debug(f"  ✓ {source_path} -> {target_path}")
                except Exception as e:
                    logger.error(f"  ✗ 渲染失败 {source_path}: {e}")
            
            # 6. 打包ZIP
            zip_path = self.settings.OUTPUT_DIR / f"{project_id}.zip"
            shutil.make_archive(str(zip_path.with_suffix("")), "zip", output_dir)
            
            duration = time.time() - start_time
            logger.info(f"生成完成: {len(generated_files)} 个文件, 耗时 {duration:.2f}s")
            
            return GenerationResult(
                success=True,
                project_id=project_id,
                message=f"成功生成 {module.name}",
                files_count=len(generated_files),
                output_path=output_dir,
                duration=duration
            )
            
        except Exception as e:
            logger.error(f"生成失败: {e}")
            return GenerationResult(
                success=False,
                project_id=project_id,
                error=str(e),
                duration=time.time() - start_time
            )
    
    def _build_context(self, module: ModuleDefinition, config: Dict[str, Any]) -> Dict[str, Any]:
        """构建渲染上下文"""
        context = {}
        
        # 默认值
        for field in module.fields:
            if field.default is not None:
                context[field.name] = field.default
        
        # 用户配置
        context.update(config)
        
        # 计算属性
        if "package_name" in context:
            context["package_path"] = context["package_name"].replace(".", "/")
        
        # 元信息
        from datetime import datetime
        context["_generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        context["_module_name"] = module.name
        
        return context
    
    def get_modules(self) -> List[ModuleDefinition]:
        return self.template_loader.get_all_modules()
    
    def get_module(self, module_id: str) -> Optional[ModuleDefinition]:
        return self.template_loader.get_module(module_id)
