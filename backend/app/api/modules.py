"""
模块管理API - 获取可用的作业类型模块
"""
from fastapi import APIRouter
from typing import List
from pydantic import BaseModel

router = APIRouter()


class ModuleField(BaseModel):
    """模块配置字段"""
    name: str
    label: str
    type: str  # text, number, select, checkbox, textarea
    required: bool = True
    default: str | int | bool | None = None
    options: List[dict] | None = None  # 用于select类型
    placeholder: str | None = None


class ModuleInfo(BaseModel):
    """作业模块信息"""
    id: str
    name: str
    description: str
    icon: str
    category: str
    tech_stack: List[str]
    fields: List[ModuleField]
    preview_image: str | None = None


# 定义所有可用的作业模块
AVAILABLE_MODULES: List[ModuleInfo] = [
    ModuleInfo(
        id="student_management",
        name="学生信息管理系统",
        description="完整的学生信息管理系统，包含学生、课程、成绩管理等功能",
        icon="🎓",
        category="管理系统",
        tech_stack=["Java", "Spring Boot", "MyBatis", "Vue 3", "MySQL"],
        fields=[
            ModuleField(name="project_name", label="项目名称", type="text", default="StudentManagementSystem", placeholder="英文项目名"),
            ModuleField(name="project_name_cn", label="项目中文名", type="text", default="学生信息管理系统"),
            ModuleField(name="package_name", label="包名", type="text", default="com.example.student"),
            ModuleField(name="author", label="作者", type="text", default="Student"),
            ModuleField(name="db_name", label="数据库名", type="text", default="student_db"),
            ModuleField(name="features", label="功能模块", type="checkbox", default=True, options=[
                {"value": "student", "label": "学生管理"},
                {"value": "course", "label": "课程管理"},
                {"value": "grade", "label": "成绩管理"},
                {"value": "class", "label": "班级管理"},
                {"value": "teacher", "label": "教师管理"},
            ]),
        ]
    ),
    ModuleInfo(
        id="library_management",
        name="图书管理系统",
        description="图书馆管理系统，支持图书借阅、归还、用户管理等",
        icon="📚",
        category="管理系统",
        tech_stack=["Java", "Spring Boot", "MyBatis", "Vue 3", "MySQL"],
        fields=[
            ModuleField(name="project_name", label="项目名称", type="text", default="LibraryManagementSystem"),
            ModuleField(name="project_name_cn", label="项目中文名", type="text", default="图书管理系统"),
            ModuleField(name="package_name", label="包名", type="text", default="com.example.library"),
            ModuleField(name="author", label="作者", type="text", default="Student"),
            ModuleField(name="db_name", label="数据库名", type="text", default="library_db"),
            ModuleField(name="features", label="功能模块", type="checkbox", default=True, options=[
                {"value": "book", "label": "图书管理"},
                {"value": "borrow", "label": "借阅管理"},
                {"value": "user", "label": "用户管理"},
                {"value": "category", "label": "分类管理"},
            ]),
        ]
    ),
    ModuleInfo(
        id="hotel_management",
        name="酒店管理系统",
        description="酒店房间预订与管理系统",
        icon="🏨",
        category="管理系统",
        tech_stack=["Java", "Spring Boot", "MyBatis", "Vue 3", "MySQL"],
        fields=[
            ModuleField(name="project_name", label="项目名称", type="text", default="HotelManagementSystem"),
            ModuleField(name="project_name_cn", label="项目中文名", type="text", default="酒店管理系统"),
            ModuleField(name="package_name", label="包名", type="text", default="com.example.hotel"),
            ModuleField(name="author", label="作者", type="text", default="Student"),
            ModuleField(name="db_name", label="数据库名", type="text", default="hotel_db"),
        ]
    ),
    ModuleInfo(
        id="ecommerce",
        name="电商购物平台",
        description="在线购物商城，包含商品展示、购物车、订单管理",
        icon="🛒",
        category="Web应用",
        tech_stack=["Java", "Spring Boot", "MyBatis", "Vue 3", "MySQL"],
        fields=[
            ModuleField(name="project_name", label="项目名称", type="text", default="EcommerceSystem"),
            ModuleField(name="project_name_cn", label="项目中文名", type="text", default="电商购物平台"),
            ModuleField(name="package_name", label="包名", type="text", default="com.example.shop"),
            ModuleField(name="author", label="作者", type="text", default="Student"),
            ModuleField(name="db_name", label="数据库名", type="text", default="shop_db"),
        ]
    ),
    ModuleInfo(
        id="blog_system",
        name="个人博客系统",
        description="个人博客网站，支持文章发布、评论、分类标签",
        icon="📝",
        category="Web应用",
        tech_stack=["Python", "Flask", "SQLAlchemy", "Vue 3", "SQLite"],
        fields=[
            ModuleField(name="project_name", label="项目名称", type="text", default="BlogSystem"),
            ModuleField(name="project_name_cn", label="项目中文名", type="text", default="个人博客系统"),
            ModuleField(name="author", label="作者", type="text", default="Student"),
        ]
    ),
    ModuleInfo(
        id="data_visualization",
        name="数据可视化大屏",
        description="数据采集与可视化展示系统，支持ECharts图表",
        icon="📊",
        category="数据分析",
        tech_stack=["Python", "FastAPI", "Pandas", "ECharts", "Vue 3"],
        fields=[
            ModuleField(name="project_name", label="项目名称", type="text", default="DataVisualization"),
            ModuleField(name="project_name_cn", label="项目中文名", type="text", default="数据可视化大屏"),
            ModuleField(name="data_source", label="数据来源", type="select", options=[
                {"value": "csv", "label": "CSV文件"},
                {"value": "api", "label": "API接口"},
                {"value": "crawler", "label": "网络爬虫"},
            ]),
            ModuleField(name="author", label="作者", type="text", default="Student"),
        ]
    ),
    ModuleInfo(
        id="algorithm_experiment",
        name="算法实验项目",
        description="数据结构与算法实验，包含排序、查找、图论等",
        icon="🧮",
        category="算法实验",
        tech_stack=["C++", "Python"],
        fields=[
            ModuleField(name="project_name", label="项目名称", type="text", default="AlgorithmExperiment"),
            ModuleField(name="project_name_cn", label="项目中文名", type="text", default="算法实验项目"),
            ModuleField(name="language", label="编程语言", type="select", options=[
                {"value": "cpp", "label": "C++"},
                {"value": "python", "label": "Python"},
                {"value": "java", "label": "Java"},
            ]),
            ModuleField(name="algorithms", label="算法类型", type="checkbox", options=[
                {"value": "sort", "label": "排序算法"},
                {"value": "search", "label": "查找算法"},
                {"value": "graph", "label": "图论算法"},
                {"value": "dp", "label": "动态规划"},
            ]),
            ModuleField(name="author", label="作者", type="text", default="Student"),
        ]
    ),
    ModuleInfo(
        id="plane_game",
        name="飞机大战游戏",
        description="经典飞机大战游戏，包含玩家控制、敌机AI、碰撞检测",
        icon="✈️",
        category="游戏开发",
        tech_stack=["C++", "EasyX"],
        fields=[
            ModuleField(name="project_name", label="项目名称", type="text", default="PlaneWar"),
            ModuleField(name="project_name_cn", label="项目中文名", type="text", default="飞机大战游戏"),
            ModuleField(name="author", label="作者", type="text", default="Student"),
            ModuleField(name="difficulty", label="难度等级", type="select", options=[
                {"value": "easy", "label": "简单"},
                {"value": "normal", "label": "普通"},
                {"value": "hard", "label": "困难"},
            ]),
        ]
    ),
]


@router.get("/", response_model=List[ModuleInfo])
async def get_all_modules():
    """获取所有可用的作业模块"""
    return AVAILABLE_MODULES


@router.get("/categories")
async def get_categories():
    """获取所有模块分类"""
    categories = list(set(m.category for m in AVAILABLE_MODULES))
    return {"categories": categories}


@router.get("/{module_id}", response_model=ModuleInfo)
async def get_module_by_id(module_id: str):
    """根据ID获取模块详情"""
    for module in AVAILABLE_MODULES:
        if module.id == module_id:
            return module
    return {"error": "Module not found"}
