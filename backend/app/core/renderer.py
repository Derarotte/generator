"""
Jinja2模板渲染器 - 核心渲染引擎
"""
from pathlib import Path
from typing import Dict, Any, List
from jinja2 import Environment, FileSystemLoader, select_autoescape, TemplateNotFound
import re
from app.utils.logger import logger


class TemplateRenderer:
    """
    模板渲染器
    
    职责:
    1. 初始化Jinja2环境
    2. 提供自定义过滤器和函数
    3. 渲染模板文件
    4. 处理模板继承和包含
    """
    
    def __init__(self, templates_base_dir: Path):
        self.templates_base_dir = templates_base_dir
        self._env: Dict[str, Environment] = {}
    
    def _get_env(self, module_path: Path) -> Environment:
        """
        获取模块的Jinja2环境
        每个模块有独立的环境，支持模板继承
        """
        module_key = str(module_path)
        
        if module_key not in self._env:
            env = Environment(
                loader=FileSystemLoader([
                    str(module_path),
                    str(self.templates_base_dir / "_common"),  # 公共模板
                ]),
                autoescape=select_autoescape(["html", "xml"]),
                trim_blocks=True,
                lstrip_blocks=True,
                keep_trailing_newline=True,
            )
            
            # 注册自定义过滤器
            env.filters["camel_case"] = self._to_camel_case
            env.filters["pascal_case"] = self._to_pascal_case
            env.filters["snake_case"] = self._to_snake_case
            env.filters["kebab_case"] = self._to_kebab_case
            env.filters["package_path"] = lambda s: s.replace(".", "/")
            
            # 注册全局函数
            env.globals["now"] = self._get_current_datetime
            
            self._env[module_key] = env
        
        return self._env[module_key]
    
    def render_file(self, template_path: Path, context: Dict[str, Any], module_path: Path) -> str:
        """
        渲染单个模板文件
        
        Args:
            template_path: 相对于模块目录的模板路径
            context: 渲染上下文
            module_path: 模块根目录
            
        Returns:
            渲染后的内容
        """
        env = self._get_env(module_path)
        
        try:
            # 获取相对路径
            relative_path = template_path.relative_to(module_path)
            template = env.get_template(str(relative_path))
            return template.render(**context)
        except TemplateNotFound as e:
            logger.error(f"模板不存在: {e}")
            raise
        except Exception as e:
            logger.error(f"渲染模板失败 {template_path}: {e}")
            raise
    
    def render_directory(
        self,
        source_dir: Path,
        target_dir: Path,
        context: Dict[str, Any],
        module_path: Path
    ) -> List[Path]:
        """
        渲染整个目录的模板
        
        规则:
        - .j2 后缀的文件会被渲染，输出时去掉.j2
        - 非.j2文件直接复制
        - 目录名和文件名中的变量也会被替换
        
        Returns:
            生成的文件列表
        """
        generated_files = []
        
        for item in source_dir.rglob("*"):
            if item.is_dir():
                continue
            
            # 计算相对路径
            rel_path = item.relative_to(source_dir)
            
            # 处理路径中的变量（如 {{package_path}}）
            output_rel_path = self._process_path_variables(str(rel_path), context)
            
            # 去掉.j2后缀
            if output_rel_path.endswith(".j2"):
                output_rel_path = output_rel_path[:-3]
            
            output_path = target_dir / output_rel_path
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            if item.suffix == ".j2" or item.name.endswith(".j2"):
                # 渲染模板
                try:
                    content = self.render_file(item, context, module_path)
                    output_path.write_text(content, encoding="utf-8")
                    generated_files.append(output_path)
                    logger.debug(f"渲染: {rel_path} -> {output_rel_path}")
                except Exception as e:
                    logger.error(f"渲染失败 {item}: {e}")
            else:
                # 直接复制
                import shutil
                shutil.copy2(item, output_path)
                generated_files.append(output_path)
                logger.debug(f"复制: {rel_path}")
        
        return generated_files
    
    def _process_path_variables(self, path: str, context: Dict[str, Any]) -> str:
        """处理路径中的变量，如 {{package_path}}"""
        pattern = r"\{\{(\w+)\}\}"
        
        def replace(match):
            var_name = match.group(1)
            return str(context.get(var_name, match.group(0)))
        
        return re.sub(pattern, replace, path)
    
    # ==================== 自定义过滤器 ====================
    
    @staticmethod
    def _to_camel_case(s: str) -> str:
        """转驼峰命名: student_info -> studentInfo"""
        components = s.split("_")
        return components[0] + "".join(x.title() for x in components[1:])
    
    @staticmethod
    def _to_pascal_case(s: str) -> str:
        """转帕斯卡命名: student_info -> StudentInfo"""
        return "".join(x.title() for x in s.split("_"))
    
    @staticmethod
    def _to_snake_case(s: str) -> str:
        """转蛇形命名: StudentInfo -> student_info"""
        s = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", s)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s).lower()
    
    @staticmethod
    def _to_kebab_case(s: str) -> str:
        """转烤串命名: StudentInfo -> student-info"""
        return TemplateRenderer._to_snake_case(s).replace("_", "-")
    
    @staticmethod
    def _get_current_datetime() -> str:
        """获取当前时间"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
