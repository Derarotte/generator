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
    type: str = "text"  # text, number, select, checkbox, textarea
    required: bool = True
    default: Any = None
    options: Optional[List[Dict[str, str]]] = None
    placeholder: Optional[str] = None
    description: Optional[str] = None


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
    
    # 模板结构
    template_structure: Dict[str, Any] = Field(default_factory=dict)
    
    # 模块路径
    module_path: Optional[Path] = None


class TemplateLoader:
    """
    模板加载器
    
    职责:
    1. 扫描templates目录，发现所有模块
    2. 解析module.yaml获取模块定义
    3. 提供模块查询接口
    """
    
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
            
            module_yaml = module_dir / "module.yaml"
            if not module_yaml.exists():
                logger.warning(f"模块缺少配置文件: {module_dir.name}")
                continue
            
            try:
                module = self._load_module(module_yaml)
                module.module_path = module_dir
                self._modules[module.id] = module
                logger.info(f"加载模块成功: {module.id} ({module.name})")
            except Exception as e:
                logger.error(f"加载模块失败 {module_dir.name}: {e}")
    
    def _load_module(self, yaml_path: Path) -> ModuleDefinition:
        """从YAML文件加载模块定义"""
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        
        # 转换fields
        if "fields" in data:
            data["fields"] = [FieldDefinition(**f) for f in data["fields"]]
        
        return ModuleDefinition(**data)
    
    def get_all_modules(self) -> List[ModuleDefinition]:
        """获取所有模块"""
        return list(self._modules.values())
    
    def get_module(self, module_id: str) -> Optional[ModuleDefinition]:
        """根据ID获取模块"""
        return self._modules.get(module_id)
    
    def get_modules_by_category(self, category: str) -> List[ModuleDefinition]:
        """根据分类获取模块"""
        return [m for m in self._modules.values() if m.category == category]
    
    def get_categories(self) -> List[str]:
        """获取所有分类"""
        return list(set(m.category for m in self._modules.values()))
    
    def reload(self):
        """重新加载所有模块"""
        self._modules.clear()
        self._load_all_modules()
        logger.info(f"重新加载完成，共 {len(self._modules)} 个模块")
