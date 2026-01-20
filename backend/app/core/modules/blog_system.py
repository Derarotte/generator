"""博客系统生成器"""
from pathlib import Path
from typing import Dict, Any
from app.core.modules.base import BaseGenerator

class BlogSystemGenerator(BaseGenerator):
    def __init__(self): super().__init__(); self.name = "博客系统"
    async def generate(self, config: Dict[str, Any], output_dir: Path, templates_dir: Path) -> Dict[str, Any]:
        self.write_file(output_dir / "README.md", f"# {config.get('project_name_cn', '个人博客系统')}\n\n开发中...")
        return {"success": True}
