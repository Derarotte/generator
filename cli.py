import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any

# 将 backend 目录添加到路径
sys.path.append(str(Path(__file__).parent / "backend"))

from app.core.engine import GeneratorEngine
from app.api.modules import AVAILABLE_MODULES

async def main():
    print("🚀 中国学生作业代码生成器 - 终端测试工具")
    print("-" * 40)
    
    # 1. 选择模块
    print("\n可用模块:")
    for i, mod in enumerate(AVAILABLE_MODULES):
        print(f"{i + 1}. [{mod.id}] {mod.name} - {mod.description}")
    
    try:
        choice = int(input("\n请选择模块编号: ")) - 1
        if choice < 0 or choice >= len(AVAILABLE_MODULES):
            print("❌ 无效选择")
            return
    except ValueError:
        print("❌ 输入有误")
        return
        
    selected_module = AVAILABLE_MODULES[choice]
    print(f"✅ 已选择: {selected_module.name}")
    
    # 2. 配置参数
    config = {}
    print("\n请输入配置参数 (直接按回车使用默认值):")
    for field in selected_module.fields:
        default_val = field.default if field.default is not None else ""
        prompt = f"[{field.label}]"
        if default_val:
            prompt += f" (默认: {default_val})"
        val = input(f"{prompt}: ").strip()
        
        if not val and field.default is not None:
            config[field.name] = field.default
        else:
            # 简单类型转换
            if field.type == "checkbox":
                config[field.name] = val.split(",") if val else field.default
            else:
                config[field.name] = val

    # 3. 执行生成
    print("\n⚙️ 正在生成项目...")
    engine = GeneratorEngine()
    project_id = f"test_{selected_module.id}"
    
    result = await engine.generate(
        module_id=selected_module.id,
        config=config,
        project_id=project_id
    )
    
    if result["success"]:
        output_path = Path(__file__).parent / "output" / project_id
        print(f"\n🎉 生成成功！")
        print(f"📂 项目路径: {output_path.absolute()}")
        print(f"📦 ZIP包路径: {output_path.with_suffix('.zip').absolute()}")
        print(f"📄 文件总数: {result.get('files_count', 0)}")
    else:
        print(f"\n❌ 生成失败: {result.get('error')}")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
