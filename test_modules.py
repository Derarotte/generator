"""快速测试所有模块"""
import requests

modules = [
    "student_management",
    "library_management", 
    "hotel_management",
    "ecommerce",
    "algorithm_experiment",
    "data_visualization",
    "blog_system"
]

print("=" * 50)
print("测试所有生成器模块")
print("=" * 50)

for mod in modules:
    try:
        r = requests.post(
            "http://localhost:8000/api/internal/quick-gen",
            json={"module_id": mod}
        )
        data = r.json()
        if data.get("success"):
            print(f"✅ {mod}: 成功 - {data.get('files_count')} 个文件")
        else:
            print(f"❌ {mod}: 失败 - {data}")
    except Exception as e:
        print(f"❌ {mod}: 错误 - {e}")

print("=" * 50)
print("测试完成!")
