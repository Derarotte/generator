"""
图书管理系统生成器 - 完整的图书借阅管理系统
"""
from pathlib import Path
from typing import Dict, Any
from app.core.modules.base import BaseGenerator


class LibraryManagementGenerator(BaseGenerator):
    """图书管理系统生成器"""
    
    def __init__(self):
        super().__init__()
        self.name = "图书管理系统"
    
    async def generate(self, config: Dict[str, Any], output_dir: Path, templates_dir: Path) -> Dict[str, Any]:
        try:
            project_name = config.get("project_name", "LibraryManagement")
            project_name_cn = config.get("project_name_cn", "图书管理系统")
            package_name = config.get("package_name", "com.example.library")
            author = config.get("author", "Student")
            db_name = config.get("db_name", "library_db")
            
            package_path = package_name.replace(".", "/")
            
            # 创建后端
            backend_dir = output_dir / "backend"
            self._generate_backend(backend_dir, config, package_path)
            
            # 创建前端
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
        package_name = config.get("package_name", "com.example.library")
        db_name = config.get("db_name", "library_db")
        
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
 * {config.get("project_name_cn", "图书管理系统")} - 启动类
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
        
        # Entity 实体类
        entity_dir = src_main / "entity"
        entity_dir.mkdir(exist_ok=True)
        
        # Book.java
        self.write_file(entity_dir / "Book.java", f'''package {package_name}.entity;

import lombok.Data;
import java.util.Date;

/**
 * 图书实体类
 */
@Data
public class Book {{
    private Long id;
    private String isbn;
    private String title;
    private String author;
    private String publisher;
    private Double price;
    private Integer stock;
    private Long categoryId;
    private String description;
    private Date createTime;
    private Date updateTime;
}}
''')
        
        # User.java
        self.write_file(entity_dir / "User.java", f'''package {package_name}.entity;

import lombok.Data;
import java.util.Date;

/**
 * 用户实体类
 */
@Data
public class User {{
    private Long id;
    private String username;
    private String password;
    private String realName;
    private String phone;
    private String email;
    private Integer role; // 0-普通用户, 1-管理员
    private Date createTime;
}}
''')
        
        # BorrowRecord.java
        self.write_file(entity_dir / "BorrowRecord.java", f'''package {package_name}.entity;

import lombok.Data;
import java.util.Date;

/**
 * 借阅记录实体类
 */
@Data
public class BorrowRecord {{
    private Long id;
    private Long userId;
    private Long bookId;
    private Date borrowDate;
    private Date dueDate;
    private Date returnDate;
    private Integer status; // 0-借阅中, 1-已归还, 2-逾期
}}
''')
        
        # Mapper
        mapper_dir = src_main / "mapper"
        mapper_dir.mkdir(exist_ok=True)
        
        self.write_file(mapper_dir / "BookMapper.java", f'''package {package_name}.mapper;

import {package_name}.entity.Book;
import org.apache.ibatis.annotations.*;
import java.util.List;

@Mapper
public interface BookMapper {{
    @Select("SELECT * FROM book")
    List<Book> findAll();
    
    @Select("SELECT * FROM book WHERE id = #{{id}}")
    Book findById(Long id);
    
    @Select("SELECT * FROM book WHERE title LIKE CONCAT('%', #{{keyword}}, '%') OR author LIKE CONCAT('%', #{{keyword}}, '%')")
    List<Book> search(String keyword);
    
    @Insert("INSERT INTO book(isbn, title, author, publisher, price, stock, category_id, description, create_time) VALUES(#{{isbn}}, #{{title}}, #{{author}}, #{{publisher}}, #{{price}}, #{{stock}}, #{{categoryId}}, #{{description}}, NOW())")
    @Options(useGeneratedKeys = true, keyProperty = "id")
    int insert(Book book);
    
    @Update("UPDATE book SET title=#{{title}}, author=#{{author}}, publisher=#{{publisher}}, price=#{{price}}, stock=#{{stock}}, description=#{{description}}, update_time=NOW() WHERE id=#{{id}}")
    int update(Book book);
    
    @Delete("DELETE FROM book WHERE id = #{{id}}")
    int delete(Long id);
    
    @Update("UPDATE book SET stock = stock - 1 WHERE id = #{{id}} AND stock > 0")
    int decreaseStock(Long id);
    
    @Update("UPDATE book SET stock = stock + 1 WHERE id = #{{id}}")
    int increaseStock(Long id);
}}
''')
        
        self.write_file(mapper_dir / "BorrowRecordMapper.java", f'''package {package_name}.mapper;

import {package_name}.entity.BorrowRecord;
import org.apache.ibatis.annotations.*;
import java.util.List;

@Mapper
public interface BorrowRecordMapper {{
    @Select("SELECT * FROM borrow_record WHERE user_id = #{{userId}}")
    List<BorrowRecord> findByUserId(Long userId);
    
    @Insert("INSERT INTO borrow_record(user_id, book_id, borrow_date, due_date, status) VALUES(#{{userId}}, #{{bookId}}, NOW(), DATE_ADD(NOW(), INTERVAL 30 DAY), 0)")
    @Options(useGeneratedKeys = true, keyProperty = "id")
    int insert(BorrowRecord record);
    
    @Update("UPDATE borrow_record SET return_date=NOW(), status=1 WHERE id=#{{id}}")
    int returnBook(Long id);
}}
''')
        
        # Service
        service_dir = src_main / "service"
        service_dir.mkdir(exist_ok=True)
        
        self.write_file(service_dir / "BookService.java", f'''package {package_name}.service;

import {package_name}.entity.Book;
import {package_name}.mapper.BookMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class BookService {{
    @Autowired
    private BookMapper bookMapper;
    
    public List<Book> findAll() {{ return bookMapper.findAll(); }}
    public Book findById(Long id) {{ return bookMapper.findById(id); }}
    public List<Book> search(String keyword) {{ return bookMapper.search(keyword); }}
    public int save(Book book) {{ return book.getId() == null ? bookMapper.insert(book) : bookMapper.update(book); }}
    public int delete(Long id) {{ return bookMapper.delete(id); }}
}}
''')
        
        self.write_file(service_dir / "BorrowService.java", f'''package {package_name}.service;

import {package_name}.entity.BorrowRecord;
import {package_name}.mapper.BorrowRecordMapper;
import {package_name}.mapper.BookMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;

@Service
public class BorrowService {{
    @Autowired
    private BorrowRecordMapper borrowRecordMapper;
    @Autowired
    private BookMapper bookMapper;
    
    public List<BorrowRecord> findByUserId(Long userId) {{
        return borrowRecordMapper.findByUserId(userId);
    }}
    
    @Transactional
    public boolean borrowBook(Long userId, Long bookId) {{
        if (bookMapper.decreaseStock(bookId) > 0) {{
            BorrowRecord record = new BorrowRecord();
            record.setUserId(userId);
            record.setBookId(bookId);
            borrowRecordMapper.insert(record);
            return true;
        }}
        return false;
    }}
    
    @Transactional
    public boolean returnBook(Long recordId, Long bookId) {{
        borrowRecordMapper.returnBook(recordId);
        bookMapper.increaseStock(bookId);
        return true;
    }}
}}
''')
        
        # Controller
        controller_dir = src_main / "controller"
        controller_dir.mkdir(exist_ok=True)
        
        self.write_file(controller_dir / "BookController.java", f'''package {package_name}.controller;

import {package_name}.entity.Book;
import {package_name}.service.BookService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.*;

@RestController
@RequestMapping("/api/book")
@CrossOrigin
public class BookController {{
    @Autowired
    private BookService bookService;
    
    @GetMapping("/list")
    public Map<String, Object> list() {{
        Map<String, Object> r = new HashMap<>();
        r.put("code", 200);
        r.put("data", bookService.findAll());
        return r;
    }}
    
    @GetMapping("/search")
    public Map<String, Object> search(@RequestParam String keyword) {{
        Map<String, Object> r = new HashMap<>();
        r.put("code", 200);
        r.put("data", bookService.search(keyword));
        return r;
    }}
    
    @GetMapping("/{{id}}")
    public Map<String, Object> getById(@PathVariable Long id) {{
        Map<String, Object> r = new HashMap<>();
        r.put("code", 200);
        r.put("data", bookService.findById(id));
        return r;
    }}
    
    @PostMapping("/save")
    public Map<String, Object> save(@RequestBody Book book) {{
        Map<String, Object> r = new HashMap<>();
        bookService.save(book);
        r.put("code", 200);
        r.put("message", "保存成功");
        return r;
    }}
    
    @DeleteMapping("/{{id}}")
    public Map<String, Object> delete(@PathVariable Long id) {{
        Map<String, Object> r = new HashMap<>();
        bookService.delete(id);
        r.put("code", 200);
        r.put("message", "删除成功");
        return r;
    }}
}}
''')
        
        self.write_file(controller_dir / "BorrowController.java", f'''package {package_name}.controller;

import {package_name}.service.BorrowService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.*;

@RestController
@RequestMapping("/api/borrow")
@CrossOrigin
public class BorrowController {{
    @Autowired
    private BorrowService borrowService;
    
    @GetMapping("/my/{{userId}}")
    public Map<String, Object> myRecords(@PathVariable Long userId) {{
        Map<String, Object> r = new HashMap<>();
        r.put("code", 200);
        r.put("data", borrowService.findByUserId(userId));
        return r;
    }}
    
    @PostMapping("/borrow")
    public Map<String, Object> borrow(@RequestParam Long userId, @RequestParam Long bookId) {{
        Map<String, Object> r = new HashMap<>();
        if (borrowService.borrowBook(userId, bookId)) {{
            r.put("code", 200);
            r.put("message", "借阅成功");
        }} else {{
            r.put("code", 400);
            r.put("message", "库存不足");
        }}
        return r;
    }}
    
    @PostMapping("/return")
    public Map<String, Object> returnBook(@RequestParam Long recordId, @RequestParam Long bookId) {{
        Map<String, Object> r = new HashMap<>();
        borrowService.returnBook(recordId, bookId);
        r.put("code", 200);
        r.put("message", "归还成功");
        return r;
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
    <groupId>{config.get("package_name", "com.example.library")}</groupId>
    <artifactId>{config.get("project_name", "LibraryManagement").lower()}</artifactId>
    <version>1.0.0</version>
    <properties><java.version>11</java.version></properties>
    <dependencies>
        <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-web</artifactId></dependency>
        <dependency><groupId>org.mybatis.spring.boot</groupId><artifactId>mybatis-spring-boot-starter</artifactId><version>2.3.1</version></dependency>
        <dependency><groupId>mysql</groupId><artifactId>mysql-connector-java</artifactId><version>8.0.33</version></dependency>
        <dependency><groupId>org.projectlombok</groupId><artifactId>lombok</artifactId><optional>true</optional></dependency>
    </dependencies>
    <build><plugins><plugin><groupId>org.springframework.boot</groupId><artifactId>spring-boot-maven-plugin</artifactId></plugin></plugins></build>
</project>
'''

    def _generate_frontend(self, frontend_dir: Path, config: Dict):
        """生成Vue前端"""
        project_name_cn = config.get("project_name_cn", "图书管理系统")
        
        self.write_file(frontend_dir / "package.json", '''{
  "name": "library-management-frontend",
  "version": "1.0.0",
  "scripts": { "dev": "vite", "build": "vite build" },
  "dependencies": { "vue": "^3.4.0", "vue-router": "^4.2.0", "axios": "^1.6.0", "element-plus": "^2.4.0" },
  "devDependencies": { "@vitejs/plugin-vue": "^5.0.0", "vite": "^5.0.0" }
}
''')
        
        self.write_file(frontend_dir / "vite.config.js", '''import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
export default defineConfig({
  plugins: [vue()],
  server: { port: 5173, proxy: { '/api': 'http://localhost:8080' } }
})
''')
        
        self.write_file(frontend_dir / "index.html", f'''<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{project_name_cn}</title></head>
<body><div id="app"></div><script type="module" src="/src/main.js"></script></body>
</html>
''')
        
        src = frontend_dir / "src"
        src.mkdir(exist_ok=True)
        
        self.write_file(src / "main.js", '''import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'
createApp(App).use(ElementPlus).use(router).mount('#app')
''')
        
        self.write_file(src / "App.vue", f'''<template>
  <el-container style="height:100vh">
    <el-header style="background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;display:flex;align-items:center">
      <h1>📚 {project_name_cn}</h1>
    </el-header>
    <el-container>
      <el-aside width="200px" style="background:#304156">
        <el-menu router default-active="/" style="background:#304156;border:none">
          <el-menu-item index="/" style="color:#bfcbd9">📊 首页</el-menu-item>
          <el-menu-item index="/books" style="color:#bfcbd9">📖 图书管理</el-menu-item>
          <el-menu-item index="/borrow" style="color:#bfcbd9">📝 借阅管理</el-menu-item>
        </el-menu>
      </el-aside>
      <el-main style="background:#f0f2f5"><router-view /></el-main>
    </el-container>
  </el-container>
</template>
''')
        
        router_dir = src / "router"
        router_dir.mkdir(exist_ok=True)
        self.write_file(router_dir / "index.js", '''import { createRouter, createWebHistory } from 'vue-router'
const routes = [
  { path: '/', component: () => import('../views/Home.vue') },
  { path: '/books', component: () => import('../views/BookList.vue') },
  { path: '/borrow', component: () => import('../views/BorrowList.vue') }
]
export default createRouter({ history: createWebHistory(), routes })
''')
        
        views_dir = src / "views"
        views_dir.mkdir(exist_ok=True)
        
        self.write_file(views_dir / "Home.vue", f'''<template>
  <el-card><h2>欢迎使用 {project_name_cn}</h2><p>基于 Spring Boot + Vue 3 的图书借阅管理系统</p></el-card>
</template>
''')
        
        self.write_file(views_dir / "BookList.vue", '''<template>
  <el-card>
    <template #header><div style="display:flex;justify-content:space-between"><span>图书列表</span><el-button type="primary" @click="showDialog=true">新增图书</el-button></div></template>
    <el-input v-model="keyword" placeholder="搜索图书..." style="width:300px;margin-bottom:20px" @keyup.enter="search"><template #append><el-button @click="search">搜索</el-button></template></el-input>
    <el-table :data="books" stripe>
      <el-table-column prop="isbn" label="ISBN" width="140" />
      <el-table-column prop="title" label="书名" />
      <el-table-column prop="author" label="作者" width="120" />
      <el-table-column prop="publisher" label="出版社" width="150" />
      <el-table-column prop="price" label="价格" width="80" />
      <el-table-column prop="stock" label="库存" width="80" />
      <el-table-column label="操作" width="180">
        <template #default="{row}"><el-button size="small" @click="edit(row)">编辑</el-button><el-button size="small" type="danger" @click="del(row.id)">删除</el-button></template>
      </el-table-column>
    </el-table>
  </el-card>
  <el-dialog v-model="showDialog" :title="form.id?\'编辑图书\':\'新增图书\'">
    <el-form :model="form" label-width="80px">
      <el-form-item label="ISBN"><el-input v-model="form.isbn" /></el-form-item>
      <el-form-item label="书名"><el-input v-model="form.title" /></el-form-item>
      <el-form-item label="作者"><el-input v-model="form.author" /></el-form-item>
      <el-form-item label="出版社"><el-input v-model="form.publisher" /></el-form-item>
      <el-form-item label="价格"><el-input-number v-model="form.price" :min="0" /></el-form-item>
      <el-form-item label="库存"><el-input-number v-model="form.stock" :min="0" /></el-form-item>
    </el-form>
    <template #footer><el-button @click="showDialog=false">取消</el-button><el-button type="primary" @click="save">保存</el-button></template>
  </el-dialog>
</template>
<script setup>
import { ref, onMounted } from \'vue\'
import axios from \'axios\'
import { ElMessage, ElMessageBox } from \'element-plus\'
const books = ref([])
const keyword = ref(\'\')
const showDialog = ref(false)
const form = ref({ isbn:\'\', title:\'\', author:\'\', publisher:\'\', price:0, stock:0 })
const fetch = async () => { const r = await axios.get(\'/api/book/list\'); books.value = r.data.data || [] }
const search = async () => { const r = await axios.get(\'/api/book/search\', { params: { keyword: keyword.value } }); books.value = r.data.data || [] }
const save = async () => { await axios.post(\'/api/book/save\', form.value); ElMessage.success(\'保存成功\'); showDialog.value=false; form.value={isbn:\'\',title:\'\',author:\'\',publisher:\'\',price:0,stock:0}; fetch() }
const edit = (row) => { form.value = {...row}; showDialog.value = true }
const del = async (id) => { await ElMessageBox.confirm(\'确定删除?\'); await axios.delete(`/api/book/${id}`); ElMessage.success(\'删除成功\'); fetch() }
onMounted(fetch)
</script>
''')
        
        self.write_file(views_dir / "BorrowList.vue", '''<template>
  <el-card><template #header>我的借阅记录</template>
    <el-table :data="records" stripe>
      <el-table-column prop="bookId" label="图书ID" />
      <el-table-column prop="borrowDate" label="借阅日期" />
      <el-table-column prop="dueDate" label="应还日期" />
      <el-table-column prop="status" label="状态"><template #default="{row}">{{ row.status===0?\'借阅中\':row.status===1?\'已归还\':\'逾期\' }}</template></el-table-column>
    </el-table>
  </el-card>
</template>
<script setup>
import { ref, onMounted } from \'vue\'
import axios from \'axios\'
const records = ref([])
onMounted(async () => { const r = await axios.get(\'/api/borrow/my/1\'); records.value = r.data.data || [] })
</script>
''')

    def _generate_database(self, db_dir: Path, config: Dict):
        """生成数据库脚本"""
        db_name = config.get("db_name", "library_db")
        db_dir.mkdir(exist_ok=True)
        
        self.write_file(db_dir / "init.sql", f'''-- {config.get("project_name_cn", "图书管理系统")} 数据库初始化脚本
CREATE DATABASE IF NOT EXISTS {db_name} DEFAULT CHARSET utf8mb4;
USE {db_name};

-- 图书表
CREATE TABLE IF NOT EXISTS book (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    isbn VARCHAR(20) UNIQUE,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100),
    publisher VARCHAR(100),
    price DECIMAL(10,2),
    stock INT DEFAULT 0,
    category_id BIGINT,
    description TEXT,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='图书表';

-- 用户表
CREATE TABLE IF NOT EXISTS user (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    real_name VARCHAR(50),
    phone VARCHAR(20),
    email VARCHAR(100),
    role INT DEFAULT 0,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 借阅记录表
CREATE TABLE IF NOT EXISTS borrow_record (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    book_id BIGINT NOT NULL,
    borrow_date DATETIME,
    due_date DATETIME,
    return_date DATETIME,
    status INT DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='借阅记录表';

-- 测试数据
INSERT INTO book (isbn, title, author, publisher, price, stock) VALUES
('978-7-111-11111-1', 'Java编程思想', 'Bruce Eckel', '机械工业出版社', 108.00, 10),
('978-7-111-22222-2', '深入理解计算机系统', 'Randal E.Bryant', '机械工业出版社', 139.00, 5),
('978-7-111-33333-3', '算法导论', 'Thomas H.Cormen', '机械工业出版社', 128.00, 8);

INSERT INTO user (username, password, real_name, role) VALUES
('admin', '123456', '管理员', 1),
('user1', '123456', '张三', 0);
''')

    def _generate_readme(self, output_dir: Path, config: Dict):
        """生成README"""
        project_name_cn = config.get("project_name_cn", "图书管理系统")
        self.write_file(output_dir / "README.md", f'''# {project_name_cn}

## 项目简介
基于 Spring Boot + Vue 3 + MySQL 的{project_name_cn}，支持图书管理、借阅管理等功能。

## 技术栈
- 后端：Spring Boot 2.7 + MyBatis + MySQL
- 前端：Vue 3 + Vite + Element Plus

## 快速开始
1. 执行 `database/init.sql` 初始化数据库
2. 启动后端：`cd backend && mvn spring-boot:run`
3. 启动前端：`cd frontend && npm install && npm run dev`
4. 访问 http://localhost:5173

## 作者
{config.get("author", "Student")}
''')

    def _generate_report(self, docs_dir: Path, config: Dict):
        """生成实验报告"""
        project_name_cn = config.get("project_name_cn", "图书管理系统")
        docs_dir.mkdir(exist_ok=True)
        self.write_file(docs_dir / "实验报告.md", f'''# {project_name_cn} 课程设计报告

## 一、设计目的
掌握Spring Boot和Vue.js的开发技术，了解图书借阅业务流程。

## 二、开发环境
- JDK 11, Maven, Node.js 18+, MySQL 8.0, IntelliJ IDEA, VS Code

## 三、系统设计
### 3.1 功能模块
- 图书管理：图书的增删改查
- 借阅管理：借阅、归还、逾期处理
- 用户管理：用户注册、登录、权限

### 3.2 数据库设计
- book表：存储图书信息
- user表：存储用户信息
- borrow_record表：存储借阅记录

## 四、系统实现
使用Spring Boot实现RESTful API，Vue 3实现前端界面。

## 五、总结
成功完成了{project_name_cn}的开发，掌握了前后端分离的开发模式。

## 作者：{config.get("author", "Student")}
''')
