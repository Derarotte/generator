# 中国学生作业代码生成器

一个模块化的学生作业代码生成系统，支持多种作业类型一键生成完整项目。

## ✨ 功能特性

- 🎯 **多种作业类型** - 管理系统、Web应用、算法实验、数据分析、游戏开发
- ⚡ **一键生成** - 选择模块，配置参数，即刻生成完整可运行项目
- 📝 **配套文档** - 自动生成实验报告、README等中文文档
- 🔧 **灵活配置** - 项目名称、功能模块、技术栈均可自定义

## 🚀 快速开始

### 后端启动

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 前端启动

```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:3000 开始使用！

## 📁 项目结构

```
homework-generator/
├── backend/                 # Python FastAPI 后端
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── core/           # 核心生成引擎
│   │   │   └── modules/    # 各类作业生成器
│   │   └── main.py
│   └── requirements.txt
├── frontend/                # Vue 3 前端
│   ├── src/
│   │   ├── views/          # 页面组件
│   │   ├── router/         # 路由
│   │   └── styles/         # 样式
│   └── package.json
└── output/                  # 生成输出目录
```

## 📦 支持的作业类型

| 类型 | 名称 | 技术栈 |
|------|------|--------|
| 🎓 | 学生信息管理系统 | Spring Boot + Vue + MySQL |
| 📚 | 图书管理系统 | Spring Boot + Vue + MySQL |
| 🏨 | 酒店管理系统 | Spring Boot + Vue + MySQL |
| 🛒 | 电商购物平台 | Spring Boot + Vue + MySQL |
| 📝 | 个人博客系统 | Flask + Vue + SQLite |
| 📊 | 数据可视化大屏 | FastAPI + ECharts + Vue |
| 🧮 | 算法实验项目 | C++ / Python |
| ✈️ | 飞机大战游戏 | C++ + EasyX |

## 📄 License

MIT
