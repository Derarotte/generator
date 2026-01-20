"""
学生信息管理系统生成器
"""
from pathlib import Path
from typing import Dict, Any
from app.core.modules.base import BaseGenerator


class StudentManagementGenerator(BaseGenerator):
    """学生信息管理系统生成器"""
    
    def __init__(self):
        super().__init__()
        self.name = "学生信息管理系统"
    
    async def generate(self, config: Dict[str, Any], output_dir: Path, templates_dir: Path) -> Dict[str, Any]:
        try:
            project_name = config.get("project_name", "StudentManagement")
            project_name_cn = config.get("project_name_cn", "学生信息管理系统")
            package_name = config.get("package_name", "com.example.student")
            author = config.get("author", "Student")
            db_name = config.get("db_name", "student_db")
            
            package_path = package_name.replace(".", "/")
            
            # 创建后端目录结构
            backend_dir = output_dir / "backend"
            self._generate_backend(backend_dir, config, package_path)
            
            # 创建前端目录结构
            frontend_dir = output_dir / "frontend"
            self._generate_frontend(frontend_dir, config)
            
            # 创建数据库脚本
            self._generate_database(output_dir / "database", config)
            
            # 创建README
            self._generate_readme(output_dir, config)
            
            # 创建实验报告
            self._generate_report(output_dir / "docs", config)
            
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _generate_backend(self, backend_dir: Path, config: Dict, package_path: str):
        """生成Spring Boot后端"""
        package_name = config.get("package_name", "com.example.student")
        project_name = config.get("project_name", "StudentManagement")
        db_name = config.get("db_name", "student_db")
        
        src_main = backend_dir / "src/main/java" / package_path
        src_main.mkdir(parents=True, exist_ok=True)
        resources = backend_dir / "src/main/resources"
        resources.mkdir(parents=True, exist_ok=True)
        
        # pom.xml
        self.write_file(backend_dir / "pom.xml", self._get_pom_xml(config))
        
        # Application.java
        self.write_file(src_main / "Application.java", f'''package {package_name};

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * {config.get("project_name_cn", "学生信息管理系统")} - 启动类
 * @author {config.get("author", "Student")}
 */
@SpringBootApplication
public class Application {{
    public static void main(String[] args) {{
        SpringApplication.run(Application.class, args);
    }}
}}
''')
        
        # application.yml
        self.write_file(resources / "application.yml", f'''server:
  port: 8080

spring:
  datasource:
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://localhost:3306/{db_name}?useSSL=false&serverTimezone=Asia/Shanghai&characterEncoding=utf-8
    username: root
    password: root123
  
mybatis:
  mapper-locations: classpath:mapper/*.xml
  type-aliases-package: {package_name}.entity
  configuration:
    map-underscore-to-camel-case: true
''')
        
        # Entity - Student.java
        entity_dir = src_main / "entity"
        entity_dir.mkdir(exist_ok=True)
        self.write_file(entity_dir / "Student.java", f'''package {package_name}.entity;

import lombok.Data;
import java.util.Date;

/**
 * 学生实体类
 */
@Data
public class Student {{
    private Long id;
    private String studentNo;
    private String name;
    private String gender;
    private Date birthday;
    private String phone;
    private String email;
    private Long classId;
    private String address;
    private Date createTime;
    private Date updateTime;
}}
''')
        
        # Mapper
        mapper_dir = src_main / "mapper"
        mapper_dir.mkdir(exist_ok=True)
        self.write_file(mapper_dir / "StudentMapper.java", f'''package {package_name}.mapper;

import {package_name}.entity.Student;
import org.apache.ibatis.annotations.*;
import java.util.List;

@Mapper
public interface StudentMapper {{
    @Select("SELECT * FROM student")
    List<Student> findAll();
    
    @Select("SELECT * FROM student WHERE id = #{{id}}")
    Student findById(Long id);
    
    @Insert("INSERT INTO student(student_no, name, gender, birthday, phone, email, class_id, address, create_time) VALUES(#{{studentNo}}, #{{name}}, #{{gender}}, #{{birthday}}, #{{phone}}, #{{email}}, #{{classId}}, #{{address}}, NOW())")
    @Options(useGeneratedKeys = true, keyProperty = "id")
    int insert(Student student);
    
    @Update("UPDATE student SET name=#{{name}}, gender=#{{gender}}, birthday=#{{birthday}}, phone=#{{phone}}, email=#{{email}}, class_id=#{{classId}}, address=#{{address}}, update_time=NOW() WHERE id=#{{id}}")
    int update(Student student);
    
    @Delete("DELETE FROM student WHERE id = #{{id}}")
    int delete(Long id);
}}
''')
        
        # Service
        service_dir = src_main / "service"
        service_dir.mkdir(exist_ok=True)
        self.write_file(service_dir / "StudentService.java", f'''package {package_name}.service;

import {package_name}.entity.Student;
import {package_name}.mapper.StudentMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class StudentService {{
    @Autowired
    private StudentMapper studentMapper;
    
    public List<Student> findAll() {{
        return studentMapper.findAll();
    }}
    
    public Student findById(Long id) {{
        return studentMapper.findById(id);
    }}
    
    public int save(Student student) {{
        if (student.getId() == null) {{
            return studentMapper.insert(student);
        }}
        return studentMapper.update(student);
    }}
    
    public int delete(Long id) {{
        return studentMapper.delete(id);
    }}
}}
''')
        
        # Controller
        controller_dir = src_main / "controller"
        controller_dir.mkdir(exist_ok=True)
        self.write_file(controller_dir / "StudentController.java", f'''package {package_name}.controller;

import {package_name}.entity.Student;
import {package_name}.service.StudentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/student")
@CrossOrigin
public class StudentController {{
    @Autowired
    private StudentService studentService;
    
    @GetMapping("/list")
    public Map<String, Object> list() {{
        Map<String, Object> result = new HashMap<>();
        result.put("code", 200);
        result.put("data", studentService.findAll());
        return result;
    }}
    
    @GetMapping("/{{id}}")
    public Map<String, Object> getById(@PathVariable Long id) {{
        Map<String, Object> result = new HashMap<>();
        result.put("code", 200);
        result.put("data", studentService.findById(id));
        return result;
    }}
    
    @PostMapping("/save")
    public Map<String, Object> save(@RequestBody Student student) {{
        Map<String, Object> result = new HashMap<>();
        studentService.save(student);
        result.put("code", 200);
        result.put("message", "保存成功");
        return result;
    }}
    
    @DeleteMapping("/{{id}}")
    public Map<String, Object> delete(@PathVariable Long id) {{
        Map<String, Object> result = new HashMap<>();
        studentService.delete(id);
        result.put("code", 200);
        result.put("message", "删除成功");
        return result;
    }}
}}
''')
    
    def _get_pom_xml(self, config: Dict) -> str:
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.7.18</version>
    </parent>
    
    <groupId>{config.get("package_name", "com.example.student")}</groupId>
    <artifactId>{config.get("project_name", "StudentManagement").lower()}</artifactId>
    <version>1.0.0</version>
    
    <properties>
        <java.version>11</java.version>
    </properties>
    
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.mybatis.spring.boot</groupId>
            <artifactId>mybatis-spring-boot-starter</artifactId>
            <version>2.3.1</version>
        </dependency>
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <version>8.0.33</version>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
    </dependencies>
    
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
'''

    def _generate_frontend(self, frontend_dir: Path, config: Dict):
        """生成Vue前端"""
        project_name_cn = config.get("project_name_cn", "学生信息管理系统")
        
        # package.json
        self.write_file(frontend_dir / "package.json", '''{
  "name": "student-management-frontend",
  "version": "1.0.0",
  "scripts": {
    "dev": "vite",
    "build": "vite build"
  },
  "dependencies": {
    "vue": "^3.4.0",
    "vue-router": "^4.2.0",
    "axios": "^1.6.0",
    "element-plus": "^2.4.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.0",
    "vite": "^5.0.0"
  }
}
''')
        
        # vite.config.js
        self.write_file(frontend_dir / "vite.config.js", '''import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:8080'
    }
  }
})
''')
        
        # index.html
        self.write_file(frontend_dir / "index.html", f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{project_name_cn}</title>
</head>
<body>
  <div id="app"></div>
  <script type="module" src="/src/main.js"></script>
</body>
</html>
''')
        
        src = frontend_dir / "src"
        src.mkdir(exist_ok=True)
        
        # main.js
        self.write_file(src / "main.js", '''import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'

const app = createApp(App)
app.use(ElementPlus)
app.use(router)
app.mount('#app')
''')
        
        # App.vue
        self.write_file(src / "App.vue", f'''<template>
  <div class="app-container">
    <el-container>
      <el-header class="header">
        <h1>🎓 {project_name_cn}</h1>
      </el-header>
      <el-container>
        <el-aside width="200px" class="sidebar">
          <el-menu router default-active="/" class="menu">
            <el-menu-item index="/">
              <span>📊 首页</span>
            </el-menu-item>
            <el-menu-item index="/students">
              <span>👨‍🎓 学生管理</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main class="main">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
.app-container {{ height: 100vh; }}
.header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; display: flex; align-items: center; }}
.header h1 {{ font-size: 20px; }}
.sidebar {{ background: #304156; }}
.menu {{ background: #304156; border: none; }}
.menu .el-menu-item {{ color: #bfcbd9; }}
.menu .el-menu-item:hover {{ background: #263445; }}
.main {{ background: #f0f2f5; padding: 20px; }}
</style>
''')
        
        # router/index.js
        router_dir = src / "router"
        router_dir.mkdir(exist_ok=True)
        self.write_file(router_dir / "index.js", '''import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', component: () => import('../views/Home.vue') },
  { path: '/students', component: () => import('../views/StudentList.vue') }
]

export default createRouter({
  history: createWebHistory(),
  routes
})
''')
        
        # views
        views_dir = src / "views"
        views_dir.mkdir(exist_ok=True)
        
        self.write_file(views_dir / "Home.vue", f'''<template>
  <div class="home">
    <el-card class="welcome-card">
      <h2>欢迎使用 {project_name_cn}</h2>
      <p>这是一个基于 Spring Boot + Vue 3 的管理系统</p>
    </el-card>
  </div>
</template>
<style scoped>
.welcome-card {{ text-align: center; padding: 40px; }}
.welcome-card h2 {{ color: #409EFF; margin-bottom: 20px; }}
</style>
''')
        
        self.write_file(views_dir / "StudentList.vue", '''<template>
  <div class="student-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>学生列表</span>
          <el-button type="primary" @click="showDialog = true">新增学生</el-button>
        </div>
      </template>
      <el-table :data="students" stripe>
        <el-table-column prop="studentNo" label="学号" width="120" />
        <el-table-column prop="name" label="姓名" width="100" />
        <el-table-column prop="gender" label="性别" width="80" />
        <el-table-column prop="phone" label="电话" width="140" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button size="small" @click="editStudent(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteStudent(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <el-dialog v-model="showDialog" :title="form.id ? \'编辑学生\' : \'新增学生\'">
      <el-form :model="form" label-width="80px">
        <el-form-item label="学号"><el-input v-model="form.studentNo" /></el-form-item>
        <el-form-item label="姓名"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="性别">
          <el-radio-group v-model="form.gender">
            <el-radio label="男">男</el-radio>
            <el-radio label="女">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="电话"><el-input v-model="form.phone" /></el-form-item>
        <el-form-item label="邮箱"><el-input v-model="form.email" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" @click="saveStudent">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from \'vue\'
import axios from \'axios\'
import { ElMessage, ElMessageBox } from \'element-plus\'

const students = ref([])
const showDialog = ref(false)
const form = ref({ studentNo: \'\', name: \'\', gender: \'男\', phone: \'\', email: \'\' })

const fetchStudents = async () => {
  const res = await axios.get(\'/api/student/list\')
  students.value = res.data.data || []
}

const saveStudent = async () => {
  await axios.post(\'/api/student/save\', form.value)
  ElMessage.success(\'保存成功\')
  showDialog.value = false
  form.value = { studentNo: \'\', name: \'\', gender: \'男\', phone: \'\', email: \'\' }
  fetchStudents()
}

const editStudent = (row) => {
  form.value = { ...row }
  showDialog.value = true
}

const deleteStudent = async (id) => {
  await ElMessageBox.confirm(\'确定删除?\', \'提示\')
  await axios.delete(`/api/student/${id}`)
  ElMessage.success(\'删除成功\')
  fetchStudents()
}

onMounted(fetchStudents)
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>
''')

    def _generate_database(self, db_dir: Path, config: Dict):
        """生成数据库脚本"""
        db_name = config.get("db_name", "student_db")
        db_dir.mkdir(exist_ok=True)
        
        self.write_file(db_dir / "init.sql", f'''-- {config.get("project_name_cn", "学生信息管理系统")} 数据库初始化脚本

CREATE DATABASE IF NOT EXISTS {db_name} DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE {db_name};

-- 学生表
CREATE TABLE IF NOT EXISTS student (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    student_no VARCHAR(20) NOT NULL UNIQUE COMMENT '学号',
    name VARCHAR(50) NOT NULL COMMENT '姓名',
    gender VARCHAR(10) DEFAULT '男' COMMENT '性别',
    birthday DATE COMMENT '出生日期',
    phone VARCHAR(20) COMMENT '电话',
    email VARCHAR(100) COMMENT '邮箱',
    class_id BIGINT COMMENT '班级ID',
    address VARCHAR(200) COMMENT '地址',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='学生表';

-- 插入测试数据
INSERT INTO student (student_no, name, gender, phone, email) VALUES
('2024001', '张三', '男', '13800138001', 'zhangsan@example.com'),
('2024002', '李四', '男', '13800138002', 'lisi@example.com'),
('2024003', '王五', '女', '13800138003', 'wangwu@example.com');
''')

    def _generate_readme(self, output_dir: Path, config: Dict):
        """生成README"""
        project_name_cn = config.get("project_name_cn", "学生信息管理系统")
        
        self.write_file(output_dir / "README.md", f'''# {project_name_cn}

## 项目简介
这是一个基于 Spring Boot + Vue 3 + MySQL 的{project_name_cn}。

## 技术栈
- 后端：Spring Boot 2.7 + MyBatis + MySQL
- 前端：Vue 3 + Vite + Element Plus
- 数据库：MySQL 8.0

## 快速开始

### 1. 数据库初始化
```sql
source database/init.sql
```

### 2. 启动后端
```bash
cd backend
mvn spring-boot:run
```

### 3. 启动前端
```bash
cd frontend
npm install
npm run dev
```

### 4. 访问系统
打开浏览器访问：http://localhost:5173

## 作者
{config.get("author", "Student")}
''')

    def _generate_report(self, docs_dir: Path, config: Dict):
        """生成实验报告"""
        project_name_cn = config.get("project_name_cn", "学生信息管理系统")
        docs_dir.mkdir(exist_ok=True)
        
        self.write_file(docs_dir / "实验报告.md", f'''# {project_name_cn} 课程设计报告

## 一、设计目的
通过本次课程设计，掌握Spring Boot和Vue.js的开发技术，了解前后端分离架构的设计方法。

## 二、开发环境
- 操作系统：Windows 11
- 开发工具：IntelliJ IDEA, VS Code
- 数据库：MySQL 8.0
- JDK版本：JDK 11
- Node.js版本：v18+

## 三、系统设计
### 3.1 系统架构
采用前后端分离的B/S架构设计。

### 3.2 数据库设计
使用MySQL数据库，设计了学生表(student)等核心数据表。

## 四、系统实现
### 4.1 后端实现
使用Spring Boot框架实现RESTful API接口。

### 4.2 前端实现
使用Vue 3 + Element Plus实现用户界面。

## 五、总结
通过本次课程设计，成功完成了{project_name_cn}的开发。

## 作者：{config.get("author", "Student")}
''')
