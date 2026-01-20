# API 接口文档

## 基础信息

- **Base URL**: `http://localhost:8000`
- **认证**: 无 (开发环境)
- **响应格式**: JSON

## 接口列表

### 健康检查

```
GET /api/health
```

**响应**:
```json
{
  "status": "healthy",
  "version": "2.0.0"
}
```

---

### 获取所有模块

```
GET /api/modules/
```

**响应**:
```json
[
  {
    "id": "student_management",
    "name": "学生信息管理系统",
    "description": "完整的学生信息管理系统...",
    "icon": "🎓",
    "category": "管理系统",
    "tech_stack": ["Java", "Spring Boot", "Vue 3", "MySQL"],
    "fields": [...]
  }
]
```

---

### 获取单个模块

```
GET /api/modules/{module_id}
```

**参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| module_id | string | 模块ID |

---

### 获取模块分类

```
GET /api/modules/categories
```

**响应**:
```json
{
  "categories": ["管理系统", "Web应用", "数据分析"]
}
```

---

### 生成项目

```
POST /api/generator/generate
```

**请求体**:
```json
{
  "module_id": "student_management",
  "config": {
    "project_name": "StudentSystem",
    "project_name_cn": "学生管理系统",
    "package_name": "com.example.student",
    "author": "张三",
    "db_name": "student_db"
  }
}
```

**响应**:
```json
{
  "success": true,
  "project_id": "abc12345",
  "message": "成功生成 学生信息管理系统",
  "files_count": 25,
  "download_url": "/api/generator/download/abc12345",
  "duration": 1.23
}
```

---

### 下载项目

```
GET /api/generator/download/{project_id}
```

**参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| project_id | string | 项目ID |

**响应**: ZIP 文件

---

### 预览项目结构

```
GET /api/generator/preview/{project_id}
```

**响应**:
```json
{
  "project_id": "abc12345",
  "files": [
    {"type": "directory", "name": "backend", "path": "backend"},
    {"type": "file", "name": "pom.xml", "path": "backend/pom.xml", "size": 2048}
  ]
}
```

---

### 内部测试接口

#### 系统状态

```
GET /api/internal/status
```

#### 快速生成

```
POST /api/internal/quick-gen
```

**请求体**:
```json
{
  "module_id": "student_management",
  "config": {}
}
```

---

## 错误码

| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

## 错误响应格式

```json
{
  "detail": "错误信息描述"
}
```
