# 模块开发指南

本文档介绍如何为生成器添加新的作业模块。

## 模块结构

每个模块是 `templates/` 目录下的一个文件夹，结构如下：

```
templates/
└── your_module_name/
    ├── module.yaml          # 必需：模块配置文件
    ├── README.md.j2         # 可选：生成项目的README
    ├── backend/             # 后端模板目录
    │   ├── pom.xml.j2
    │   └── src/...
    ├── frontend/            # 前端模板目录
    │   ├── package.json.j2
    │   └── src/...
    ├── database/            # 数据库模板目录
    │   └── init.sql.j2
    └── docs/                # 文档模板目录
        └── 实验报告.md.j2
```

## module.yaml 配置

```yaml
# 模块唯一标识 (必需)
id: your_module_name

# 模块名称 (必需)
name: 你的模块名称

# 模块描述 (必需)
description: 模块的详细描述

# 版本号
version: "1.0.0"

# 作者
author: YourName

# 图标 (emoji)
icon: 🎯

# 分类
category: 管理系统

# 技术栈列表
tech_stack:
  - Java
  - Spring Boot
  - Vue 3

# 用户可配置的字段
fields:
  - name: project_name        # 字段名
    label: 项目名称           # 显示标签
    type: text                # 类型: text/number/select/checkbox
    required: true            # 是否必填
    default: MyProject        # 默认值
    placeholder: 请输入项目名  # 占位符
    description: 用于生成目录名 # 描述
    
  - name: features
    label: 功能模块
    type: checkbox
    options:
      - value: user
        label: 用户管理
      - value: order
        label: 订单管理
    default:
      - user
```

## Jinja2 模板语法

### 变量输出

```jinja2
{{ project_name }}           # 输出变量
{{ package_name | lower }}   # 使用过滤器
```

### 内置过滤器

| 过滤器 | 说明 | 示例 |
|--------|------|------|
| `camel_case` | 驼峰命名 | `student_info` → `studentInfo` |
| `pascal_case` | 帕斯卡命名 | `student_info` → `StudentInfo` |
| `snake_case` | 蛇形命名 | `StudentInfo` → `student_info` |
| `kebab_case` | 烤串命名 | `StudentInfo` → `student-info` |
| `package_path` | 包路径转换 | `com.example` → `com/example` |

### 条件渲染

```jinja2
{% if 'user' in features %}
// 用户管理相关代码
{% endif %}
```

### 循环

```jinja2
{% for feature in features %}
- {{ feature }}
{% endfor %}
```

### 路径变量

文件名和目录名可以包含变量：

```
backend/src/main/java/{{package_path}}/Application.java.j2
```

## 内置变量

模板中可以使用以下内置变量：

| 变量 | 说明 |
|------|------|
| `_module.id` | 模块ID |
| `_module.name` | 模块名称 |
| `_module.version` | 模块版本 |
| `_generated_at` | 生成时间 |

## 测试模块

```bash
# 使用 CLI 测试
python cli.py

# 使用 API 测试
curl -X POST http://localhost:8000/api/generator/generate \
  -H "Content-Type: application/json" \
  -d '{"module_id": "your_module_name", "config": {}}'
```

## 最佳实践

1. **命名规范**: 模块ID使用 snake_case
2. **默认值**: 为所有字段提供合理的默认值
3. **注释**: 在生成的代码中添加中文注释
4. **文档**: 为每个模块提供 README 模板
5. **测试数据**: 在数据库脚本中添加测试数据
