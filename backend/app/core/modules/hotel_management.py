"""酒店管理系统生成器"""
from pathlib import Path
from typing import Dict, Any
from app.core.modules.base import BaseGenerator

class HotelManagementGenerator(BaseGenerator):
    def __init__(self): super().__init__(); self.name = "酒店管理系统"
    async def generate(self, config: Dict[str, Any], output_dir: Path, templates_dir: Path) -> Dict[str, Any]:
        self.write_file(output_dir / "README.md", f"# {config.get('project_name_cn', '酒店管理系统')}\n\n开发中...")
        return {"success": True}
