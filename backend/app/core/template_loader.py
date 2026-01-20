"""
模板加载器 - 从YAML配置加载模块定义
"""
from pathlib import Path
from typing import Dict, Any, List, Optional
import yaml
from pydantic import BaseModel, Field
from app.utils.logger import logger


class FieldDefinition(BaseModel):
    """字段定义"""
    name: str
    label: str
    type: str = "text"
    required: bool = True
    default: Any = None
    options: Optional[List[Dict[str, str]]] = None
    placeholder: Optional[str] = None
    description: Optional[str] = None


class FileMapping(BaseModel):
    """文件映射"""
    source: str  # 源模板路径
    target: str  # 目标路径（支持变量）


class ModuleDefinition(BaseModel):
    """模块定义"""
    id: str
    name: str
    description: str
    version: str = "1.0.0"
    author: str = "System"
    icon: str = "📦"
    category: str = "其他"
    tech_stack: List[str] = []
    fields: List[FieldDefinition] = []
    files: List[FileMapping] = []  # 文件映射列表
    module_path: Optional[Path] = None
    
    class Config:
        arbitrary_types_allowed = True


class TemplateLoader:
    """模板加载器"""
    
    def __init__(self, templates_dir: Path):
        self.templates_dir = templates_dir
        self._modules: Dict[str, ModuleDefinition] = {}
        self._load_all_modules()
    
    def _load_all_modules(self):
        """加载所有模块"""
        if not self.templates_dir.exists():
            logger.warning(f"模板目录不存在: {self.templates_dir}")
            return
        
        for module_dir in self.templates_dir.iterdir():
            if not module_dir.is_dir():
                continue
            if module_dir.name.startswith("_"):  # 跳过 _common 等特殊目录
                continue
            
            module_yaml = module_dir / "module.yaml"
            if not module_yaml.exists():
                logger.warning(f"模块缺少配置: {module_dir.name}")
                continue
            
            try:
                module = self._load_module(module_yaml, module_dir)
                self._modules[module.id] = module
                logger.info(f"✓ 加载模块: {module.id} ({module.name}) - {len(module.files)} 个模板")
            except Exception as e:
                logger.error(f"✗ 加载失败 {module_dir.name}: {e}")
    
    def _load_module(self, yaml_path: Path, module_dir: Path) -> ModuleDefinition:
        """从YAML加载模块"""
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        
        # 转换 fields
        if "fields" in data:
            data["fields"] = [FieldDefinition(**f) for f in data["fields"]]
        
        # 转换 files
        if "files" in data:
            data["files"] = [FileMapping(**f) for f in data["files"]]
        
        data["module_path"] = module_dir
        return ModuleDefinition(**data)
    
    def get_all_modules(self) -> List[ModuleDefinition]:
        return list(self._modules.values())
    
    def get_module(self, module_id: str) -> Optional[ModuleDefinition]:
        return self._modules.get(module_id)
    
    def get_categories(self) -> List[str]:
        return list(set(m.category for m in self._modules.values()))
    
    def reload(self):
        self._modules.clear()
        self._load_all_modules()
