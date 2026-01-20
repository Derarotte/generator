"""
酒店管理系统生成器 - 完整的酒店房间预订管理系统
"""
from pathlib import Path
from typing import Dict, Any
from app.core.modules.base import BaseGenerator


class HotelManagementGenerator(BaseGenerator):
    """酒店管理系统生成器"""
    
    def __init__(self):
        super().__init__()
        self.name = "酒店管理系统"
    
    async def generate(self, config: Dict[str, Any], output_dir: Path, templates_dir: Path) -> Dict[str, Any]:
        try:
            package_name = config.get("package_name", "com.example.hotel")
            package_path = package_name.replace(".", "/")
            
            backend_dir = output_dir / "backend"
            self._generate_backend(backend_dir, config, package_path)
            self._generate_frontend(output_dir / "frontend", config)
            self._generate_database(output_dir / "database", config)
            self._generate_readme(output_dir, config)
            self._generate_report(output_dir / "docs", config)
            
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _generate_backend(self, backend_dir: Path, config: Dict, package_path: str):
        package_name = config.get("package_name", "com.example.hotel")
        db_name = config.get("db_name", "hotel_db")
        
        src_main = backend_dir / "src/main/java" / package_path
        src_main.mkdir(parents=True, exist_ok=True)
        resources = backend_dir / "src/main/resources"
        resources.mkdir(parents=True, exist_ok=True)
        
        # pom.xml
        self.write_file(backend_dir / "pom.xml", f'''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-parent</artifactId><version>2.7.18</version></parent>
    <groupId>{package_name}</groupId><artifactId>hotel-management</artifactId><version>1.0.0</version>
    <properties><java.version>11</java.version></properties>
    <dependencies>
        <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-web</artifactId></dependency>
        <dependency><groupId>org.mybatis.spring.boot</groupId><artifactId>mybatis-spring-boot-starter</artifactId><version>2.3.1</version></dependency>
        <dependency><groupId>mysql</groupId><artifactId>mysql-connector-java</artifactId><version>8.0.33</version></dependency>
        <dependency><groupId>org.projectlombok</groupId><artifactId>lombok</artifactId><optional>true</optional></dependency>
    </dependencies>
</project>
''')
        
        # Application.java
        self.write_file(src_main / "Application.java", f'''package {package_name};
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
@SpringBootApplication
public class Application {{
    public static void main(String[] args) {{ SpringApplication.run(Application.class, args); }}
}}
''')
        
        # application.yml
        self.write_file(resources / "application.yml", f'''server:
  port: 8080
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/{db_name}?useSSL=false&serverTimezone=Asia/Shanghai
    username: root
    password: root123
mybatis:
  type-aliases-package: {package_name}.entity
  configuration:
    map-underscore-to-camel-case: true
''')
        
        # Entity
        entity_dir = src_main / "entity"
        entity_dir.mkdir(exist_ok=True)
        
        self.write_file(entity_dir / "Room.java", f'''package {package_name}.entity;
import lombok.Data;
@Data
public class Room {{
    private Long id;
    private String roomNo;
    private String roomType; // 单人间/双人间/豪华套房
    private Double price;
    private Integer status; // 0-空闲 1-已预订 2-入住中
    private String description;
}}
''')
        
        self.write_file(entity_dir / "Guest.java", f'''package {package_name}.entity;
import lombok.Data;
import java.util.Date;
@Data
public class Guest {{
    private Long id;
    private String name;
    private String idCard;
    private String phone;
    private Date createTime;
}}
''')
        
        self.write_file(entity_dir / "Order.java", f'''package {package_name}.entity;
import lombok.Data;
import java.util.Date;
@Data
public class Order {{
    private Long id;
    private Long guestId;
    private Long roomId;
    private Date checkInDate;
    private Date checkOutDate;
    private Double totalPrice;
    private Integer status; // 0-预订 1-入住 2-退房 3-取消
    private Date createTime;
}}
''')
        
        # Mapper
        mapper_dir = src_main / "mapper"
        mapper_dir.mkdir(exist_ok=True)
        
        self.write_file(mapper_dir / "RoomMapper.java", f'''package {package_name}.mapper;
import {package_name}.entity.Room;
import org.apache.ibatis.annotations.*;
import java.util.List;
@Mapper
public interface RoomMapper {{
    @Select("SELECT * FROM room")
    List<Room> findAll();
    @Select("SELECT * FROM room WHERE status = 0")
    List<Room> findAvailable();
    @Select("SELECT * FROM room WHERE id = #{{id}}")
    Room findById(Long id);
    @Update("UPDATE room SET status = #{{status}} WHERE id = #{{id}}")
    int updateStatus(@Param("id") Long id, @Param("status") Integer status);
    @Insert("INSERT INTO room(room_no, room_type, price, status, description) VALUES(#{{roomNo}}, #{{roomType}}, #{{price}}, #{{status}}, #{{description}})")
    int insert(Room room);
    @Delete("DELETE FROM room WHERE id = #{{id}}")
    int delete(Long id);
}}
''')
        
        self.write_file(mapper_dir / "OrderMapper.java", f'''package {package_name}.mapper;
import {package_name}.entity.Order;
import org.apache.ibatis.annotations.*;
import java.util.List;
@Mapper
public interface OrderMapper {{
    @Select("SELECT * FROM `order`")
    List<Order> findAll();
    @Insert("INSERT INTO `order`(guest_id, room_id, check_in_date, check_out_date, total_price, status, create_time) VALUES(#{{guestId}}, #{{roomId}}, #{{checkInDate}}, #{{checkOutDate}}, #{{totalPrice}}, #{{status}}, NOW())")
    @Options(useGeneratedKeys = true, keyProperty = "id")
    int insert(Order order);
    @Update("UPDATE `order` SET status = #{{status}} WHERE id = #{{id}}")
    int updateStatus(@Param("id") Long id, @Param("status") Integer status);
}}
''')
        
        # Service
        service_dir = src_main / "service"
        service_dir.mkdir(exist_ok=True)
        
        self.write_file(service_dir / "RoomService.java", f'''package {package_name}.service;
import {package_name}.entity.Room;
import {package_name}.mapper.RoomMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;
@Service
public class RoomService {{
    @Autowired private RoomMapper roomMapper;
    public List<Room> findAll() {{ return roomMapper.findAll(); }}
    public List<Room> findAvailable() {{ return roomMapper.findAvailable(); }}
    public Room findById(Long id) {{ return roomMapper.findById(id); }}
    public void updateStatus(Long id, Integer status) {{ roomMapper.updateStatus(id, status); }}
}}
''')
        
        self.write_file(service_dir / "OrderService.java", f'''package {package_name}.service;
import {package_name}.entity.Order;
import {package_name}.mapper.OrderMapper;
import {package_name}.mapper.RoomMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
@Service
public class OrderService {{
    @Autowired private OrderMapper orderMapper;
    @Autowired private RoomMapper roomMapper;
    public List<Order> findAll() {{ return orderMapper.findAll(); }}
    @Transactional
    public void createOrder(Order order) {{
        order.setStatus(0);
        orderMapper.insert(order);
        roomMapper.updateStatus(order.getRoomId(), 1);
    }}
    @Transactional
    public void checkIn(Long orderId, Long roomId) {{
        orderMapper.updateStatus(orderId, 1);
        roomMapper.updateStatus(roomId, 2);
    }}
    @Transactional
    public void checkOut(Long orderId, Long roomId) {{
        orderMapper.updateStatus(orderId, 2);
        roomMapper.updateStatus(roomId, 0);
    }}
}}
''')
        
        # Controller
        controller_dir = src_main / "controller"
        controller_dir.mkdir(exist_ok=True)
        
        self.write_file(controller_dir / "RoomController.java", f'''package {package_name}.controller;
import {package_name}.entity.Room;
import {package_name}.service.RoomService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.*;
@RestController @RequestMapping("/api/room") @CrossOrigin
public class RoomController {{
    @Autowired private RoomService roomService;
    @GetMapping("/list")
    public Map<String,Object> list() {{ Map<String,Object> r=new HashMap<>(); r.put("code",200); r.put("data",roomService.findAll()); return r; }}
    @GetMapping("/available")
    public Map<String,Object> available() {{ Map<String,Object> r=new HashMap<>(); r.put("code",200); r.put("data",roomService.findAvailable()); return r; }}
}}
''')
        
        self.write_file(controller_dir / "OrderController.java", f'''package {package_name}.controller;
import {package_name}.entity.Order;
import {package_name}.service.OrderService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.*;
@RestController @RequestMapping("/api/order") @CrossOrigin
public class OrderController {{
    @Autowired private OrderService orderService;
    @GetMapping("/list")
    public Map<String,Object> list() {{ Map<String,Object> r=new HashMap<>(); r.put("code",200); r.put("data",orderService.findAll()); return r; }}
    @PostMapping("/create")
    public Map<String,Object> create(@RequestBody Order order) {{ Map<String,Object> r=new HashMap<>(); orderService.createOrder(order); r.put("code",200); r.put("message","预订成功"); return r; }}
    @PostMapping("/checkin")
    public Map<String,Object> checkIn(@RequestParam Long orderId, @RequestParam Long roomId) {{ Map<String,Object> r=new HashMap<>(); orderService.checkIn(orderId, roomId); r.put("code",200); r.put("message","入住成功"); return r; }}
    @PostMapping("/checkout")
    public Map<String,Object> checkOut(@RequestParam Long orderId, @RequestParam Long roomId) {{ Map<String,Object> r=new HashMap<>(); orderService.checkOut(orderId, roomId); r.put("code",200); r.put("message","退房成功"); return r; }}
}}
''')
    
    def _generate_frontend(self, frontend_dir: Path, config: Dict):
        project_name_cn = config.get("project_name_cn", "酒店管理系统")
        
        self.write_file(frontend_dir / "package.json", '{"name":"hotel-frontend","scripts":{"dev":"vite"},"dependencies":{"vue":"^3.4.0","vue-router":"^4.2.0","axios":"^1.6.0","element-plus":"^2.4.0"},"devDependencies":{"@vitejs/plugin-vue":"^5.0.0","vite":"^5.0.0"}}')
        self.write_file(frontend_dir / "vite.config.js", 'import{defineConfig}from"vite";import vue from"@vitejs/plugin-vue";export default defineConfig({plugins:[vue()],server:{port:5173,proxy:{"/api":"http://localhost:8080"}}})')
        self.write_file(frontend_dir / "index.html", f'<!DOCTYPE html><html><head><meta charset="UTF-8"><title>{project_name_cn}</title></head><body><div id="app"></div><script type="module" src="/src/main.js"></script></body></html>')
        
        src = frontend_dir / "src"
        src.mkdir(exist_ok=True)
        self.write_file(src / "main.js", 'import{createApp}from"vue";import ElementPlus from"element-plus";import"element-plus/dist/index.css";import App from"./App.vue";import router from"./router";createApp(App).use(ElementPlus).use(router).mount("#app")')
        
        self.write_file(src / "App.vue", f'''<template>
<el-container style="height:100vh">
  <el-header style="background:linear-gradient(135deg,#f093fb,#f5576c);color:#fff;display:flex;align-items:center"><h1>🏨 {project_name_cn}</h1></el-header>
  <el-container>
    <el-aside width="200px" style="background:#304156">
      <el-menu router default-active="/" style="background:#304156;border:none">
        <el-menu-item index="/" style="color:#bfcbd9">🏠 首页</el-menu-item>
        <el-menu-item index="/rooms" style="color:#bfcbd9">🛏️ 房间管理</el-menu-item>
        <el-menu-item index="/orders" style="color:#bfcbd9">📋 订单管理</el-menu-item>
      </el-menu>
    </el-aside>
    <el-main style="background:#f0f2f5"><router-view /></el-main>
  </el-container>
</el-container>
</template>
''')
        
        router_dir = src / "router"
        router_dir.mkdir(exist_ok=True)
        self.write_file(router_dir / "index.js", 'import{createRouter,createWebHistory}from"vue-router";export default createRouter({history:createWebHistory(),routes:[{path:"/",component:()=>import("../views/Home.vue")},{path:"/rooms",component:()=>import("../views/RoomList.vue")},{path:"/orders",component:()=>import("../views/OrderList.vue")}]})')
        
        views_dir = src / "views"
        views_dir.mkdir(exist_ok=True)
        self.write_file(views_dir / "Home.vue", f'<template><el-card><h2>欢迎使用 {project_name_cn}</h2><p>基于 Spring Boot + Vue 3 的酒店房间预订系统</p></el-card></template>')
        self.write_file(views_dir / "RoomList.vue", '''<template><el-card><template #header>房间列表</template><el-table :data="rooms" stripe><el-table-column prop="roomNo" label="房间号" /><el-table-column prop="roomType" label="房型" /><el-table-column prop="price" label="价格" /><el-table-column prop="status" label="状态"><template #default="{row}">{{row.status===0?'空闲':row.status===1?'已预订':'入住中'}}</template></el-table-column></el-table></el-card></template><script setup>import{ref,onMounted}from"vue";import axios from"axios";const rooms=ref([]);onMounted(async()=>{const r=await axios.get("/api/room/list");rooms.value=r.data.data||[]})</script>''')
        self.write_file(views_dir / "OrderList.vue", '''<template><el-card><template #header>订单列表</template><el-table :data="orders" stripe><el-table-column prop="id" label="订单号" /><el-table-column prop="roomId" label="房间ID" /><el-table-column prop="checkInDate" label="入住日期" /><el-table-column prop="checkOutDate" label="退房日期" /><el-table-column prop="totalPrice" label="总价" /><el-table-column prop="status" label="状态"><template #default="{row}">{{['预订','入住','退房','取消'][row.status]}}</template></el-table-column></el-table></el-card></template><script setup>import{ref,onMounted}from"vue";import axios from"axios";const orders=ref([]);onMounted(async()=>{const r=await axios.get("/api/order/list");orders.value=r.data.data||[]})</script>''')
    
    def _generate_database(self, db_dir: Path, config: Dict):
        db_name = config.get("db_name", "hotel_db")
        db_dir.mkdir(exist_ok=True)
        self.write_file(db_dir / "init.sql", f'''CREATE DATABASE IF NOT EXISTS {db_name} DEFAULT CHARSET utf8mb4;
USE {db_name};
CREATE TABLE IF NOT EXISTS room (id BIGINT PRIMARY KEY AUTO_INCREMENT, room_no VARCHAR(20) UNIQUE, room_type VARCHAR(50), price DECIMAL(10,2), status INT DEFAULT 0, description TEXT);
CREATE TABLE IF NOT EXISTS guest (id BIGINT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(50), id_card VARCHAR(20), phone VARCHAR(20), create_time DATETIME DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS `order` (id BIGINT PRIMARY KEY AUTO_INCREMENT, guest_id BIGINT, room_id BIGINT, check_in_date DATE, check_out_date DATE, total_price DECIMAL(10,2), status INT DEFAULT 0, create_time DATETIME DEFAULT CURRENT_TIMESTAMP);
INSERT INTO room (room_no, room_type, price, status) VALUES ('101','单人间',188,0),('102','单人间',188,0),('201','双人间',288,0),('301','豪华套房',588,0);
''')
    
    def _generate_readme(self, output_dir: Path, config: Dict):
        self.write_file(output_dir / "README.md", f'''# {config.get("project_name_cn", "酒店管理系统")}
基于 Spring Boot + Vue 3 + MySQL 的酒店房间预订管理系统。
## 功能：房间管理、订单管理、入住/退房
## 启动：执行SQL -> mvn spring-boot:run -> npm run dev
## 作者：{config.get("author", "Student")}
''')
    
    def _generate_report(self, docs_dir: Path, config: Dict):
        docs_dir.mkdir(exist_ok=True)
        self.write_file(docs_dir / "实验报告.md", f'''# {config.get("project_name_cn", "酒店管理系统")} 课程设计报告
## 一、设计目的：掌握酒店业务管理系统开发
## 二、系统功能：房间管理、预订、入住、退房
## 三、技术栈：Spring Boot + MyBatis + Vue 3 + Element Plus
## 四、总结：成功完成系统开发
## 作者：{config.get("author", "Student")}
''')
