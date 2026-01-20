"""
电商购物平台生成器 - 完整的在线商城系统
"""
from pathlib import Path
from typing import Dict, Any
from app.core.modules.base import BaseGenerator


class EcommerceGenerator(BaseGenerator):
    """电商购物平台生成器"""
    
    def __init__(self):
        super().__init__()
        self.name = "电商购物平台"
    
    async def generate(self, config: Dict[str, Any], output_dir: Path, templates_dir: Path) -> Dict[str, Any]:
        try:
            package_name = config.get("package_name", "com.example.shop")
            package_path = package_name.replace(".", "/")
            
            self._generate_backend(output_dir / "backend", config, package_path)
            self._generate_frontend(output_dir / "frontend", config)
            self._generate_database(output_dir / "database", config)
            self._generate_readme(output_dir, config)
            self._generate_report(output_dir / "docs", config)
            
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _generate_backend(self, backend_dir: Path, config: Dict, package_path: str):
        package_name = config.get("package_name", "com.example.shop")
        db_name = config.get("db_name", "shop_db")
        
        src_main = backend_dir / "src/main/java" / package_path
        src_main.mkdir(parents=True, exist_ok=True)
        resources = backend_dir / "src/main/resources"
        resources.mkdir(parents=True, exist_ok=True)
        
        self.write_file(backend_dir / "pom.xml", f'''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"><modelVersion>4.0.0</modelVersion>
<parent><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-parent</artifactId><version>2.7.18</version></parent>
<groupId>{package_name}</groupId><artifactId>ecommerce</artifactId><version>1.0.0</version>
<properties><java.version>11</java.version></properties>
<dependencies>
<dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-web</artifactId></dependency>
<dependency><groupId>org.mybatis.spring.boot</groupId><artifactId>mybatis-spring-boot-starter</artifactId><version>2.3.1</version></dependency>
<dependency><groupId>mysql</groupId><artifactId>mysql-connector-java</artifactId><version>8.0.33</version></dependency>
<dependency><groupId>org.projectlombok</groupId><artifactId>lombok</artifactId><optional>true</optional></dependency>
</dependencies></project>
''')
        
        self.write_file(src_main / "Application.java", f'''package {package_name};
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
@SpringBootApplication
public class Application {{ public static void main(String[] args) {{ SpringApplication.run(Application.class, args); }} }}
''')
        
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
        
        self.write_file(entity_dir / "Product.java", f'''package {package_name}.entity;
import lombok.Data;
import java.math.BigDecimal;
@Data
public class Product {{
    private Long id;
    private String name;
    private String description;
    private BigDecimal price;
    private Integer stock;
    private String image;
    private Long categoryId;
    private Integer status;
}}
''')
        
        self.write_file(entity_dir / "User.java", f'''package {package_name}.entity;
import lombok.Data;
@Data
public class User {{
    private Long id;
    private String username;
    private String password;
    private String nickname;
    private String phone;
    private String address;
}}
''')
        
        self.write_file(entity_dir / "CartItem.java", f'''package {package_name}.entity;
import lombok.Data;
@Data
public class CartItem {{
    private Long id;
    private Long userId;
    private Long productId;
    private Integer quantity;
    private Product product;
}}
''')
        
        self.write_file(entity_dir / "Order.java", f'''package {package_name}.entity;
import lombok.Data;
import java.math.BigDecimal;
import java.util.Date;
import java.util.List;
@Data
public class Order {{
    private Long id;
    private String orderNo;
    private Long userId;
    private BigDecimal totalAmount;
    private Integer status; // 0-待支付 1-已支付 2-已发货 3-已完成 4-已取消
    private String address;
    private Date createTime;
    private List<OrderItem> items;
}}
''')
        
        self.write_file(entity_dir / "OrderItem.java", f'''package {package_name}.entity;
import lombok.Data;
import java.math.BigDecimal;
@Data
public class OrderItem {{
    private Long id;
    private Long orderId;
    private Long productId;
    private String productName;
    private BigDecimal price;
    private Integer quantity;
}}
''')
        
        # Mapper
        mapper_dir = src_main / "mapper"
        mapper_dir.mkdir(exist_ok=True)
        
        self.write_file(mapper_dir / "ProductMapper.java", f'''package {package_name}.mapper;
import {package_name}.entity.Product;
import org.apache.ibatis.annotations.*;
import java.util.List;
@Mapper
public interface ProductMapper {{
    @Select("SELECT * FROM product WHERE status = 1")
    List<Product> findAll();
    @Select("SELECT * FROM product WHERE id = #{{id}}")
    Product findById(Long id);
    @Select("SELECT * FROM product WHERE name LIKE CONCAT('%',#{{keyword}},'%')")
    List<Product> search(String keyword);
    @Update("UPDATE product SET stock = stock - #{{quantity}} WHERE id = #{{id}} AND stock >= #{{quantity}}")
    int decreaseStock(@Param("id") Long id, @Param("quantity") Integer quantity);
}}
''')
        
        self.write_file(mapper_dir / "CartMapper.java", f'''package {package_name}.mapper;
import {package_name}.entity.CartItem;
import org.apache.ibatis.annotations.*;
import java.util.List;
@Mapper
public interface CartMapper {{
    @Select("SELECT c.*, p.name as 'product.name', p.price as 'product.price', p.image as 'product.image' FROM cart_item c LEFT JOIN product p ON c.product_id = p.id WHERE c.user_id = #{{userId}}")
    @Results({{ @Result(property = "product.name", column = "product.name"), @Result(property = "product.price", column = "product.price"), @Result(property = "product.image", column = "product.image") }})
    List<CartItem> findByUserId(Long userId);
    @Insert("INSERT INTO cart_item(user_id, product_id, quantity) VALUES(#{{userId}}, #{{productId}}, #{{quantity}}) ON DUPLICATE KEY UPDATE quantity = quantity + #{{quantity}}")
    int addItem(CartItem item);
    @Delete("DELETE FROM cart_item WHERE id = #{{id}}")
    int removeItem(Long id);
    @Delete("DELETE FROM cart_item WHERE user_id = #{{userId}}")
    int clearCart(Long userId);
}}
''')
        
        self.write_file(mapper_dir / "OrderMapper.java", f'''package {package_name}.mapper;
import {package_name}.entity.Order;
import {package_name}.entity.OrderItem;
import org.apache.ibatis.annotations.*;
import java.util.List;
@Mapper
public interface OrderMapper {{
    @Select("SELECT * FROM `order` WHERE user_id = #{{userId}} ORDER BY create_time DESC")
    List<Order> findByUserId(Long userId);
    @Insert("INSERT INTO `order`(order_no, user_id, total_amount, status, address, create_time) VALUES(#{{orderNo}}, #{{userId}}, #{{totalAmount}}, #{{status}}, #{{address}}, NOW())")
    @Options(useGeneratedKeys = true, keyProperty = "id")
    int insert(Order order);
    @Insert("INSERT INTO order_item(order_id, product_id, product_name, price, quantity) VALUES(#{{orderId}}, #{{productId}}, #{{productName}}, #{{price}}, #{{quantity}})")
    int insertItem(OrderItem item);
}}
''')
        
        # Service
        service_dir = src_main / "service"
        service_dir.mkdir(exist_ok=True)
        
        self.write_file(service_dir / "ProductService.java", f'''package {package_name}.service;
import {package_name}.entity.Product;
import {package_name}.mapper.ProductMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;
@Service
public class ProductService {{
    @Autowired private ProductMapper productMapper;
    public List<Product> findAll() {{ return productMapper.findAll(); }}
    public Product findById(Long id) {{ return productMapper.findById(id); }}
    public List<Product> search(String keyword) {{ return productMapper.search(keyword); }}
}}
''')
        
        self.write_file(service_dir / "CartService.java", f'''package {package_name}.service;
import {package_name}.entity.CartItem;
import {package_name}.mapper.CartMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;
@Service
public class CartService {{
    @Autowired private CartMapper cartMapper;
    public List<CartItem> getCart(Long userId) {{ return cartMapper.findByUserId(userId); }}
    public void addToCart(Long userId, Long productId, Integer quantity) {{
        CartItem item = new CartItem();
        item.setUserId(userId);
        item.setProductId(productId);
        item.setQuantity(quantity);
        cartMapper.addItem(item);
    }}
    public void removeFromCart(Long id) {{ cartMapper.removeItem(id); }}
    public void clearCart(Long userId) {{ cartMapper.clearCart(userId); }}
}}
''')
        
        self.write_file(service_dir / "OrderService.java", f'''package {package_name}.service;
import {package_name}.entity.*;
import {package_name}.mapper.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.math.BigDecimal;
import java.util.*;
@Service
public class OrderService {{
    @Autowired private OrderMapper orderMapper;
    @Autowired private CartMapper cartMapper;
    @Autowired private ProductMapper productMapper;
    
    public List<Order> getOrders(Long userId) {{ return orderMapper.findByUserId(userId); }}
    
    @Transactional
    public Order createOrder(Long userId, String address) {{
        List<CartItem> cartItems = cartMapper.findByUserId(userId);
        if (cartItems.isEmpty()) throw new RuntimeException("购物车为空");
        
        Order order = new Order();
        order.setOrderNo("ORD" + System.currentTimeMillis());
        order.setUserId(userId);
        order.setAddress(address);
        order.setStatus(0);
        BigDecimal total = BigDecimal.ZERO;
        
        for (CartItem item : cartItems) {{
            Product p = productMapper.findById(item.getProductId());
            total = total.add(p.getPrice().multiply(BigDecimal.valueOf(item.getQuantity())));
            productMapper.decreaseStock(p.getId(), item.getQuantity());
        }}
        order.setTotalAmount(total);
        orderMapper.insert(order);
        
        for (CartItem item : cartItems) {{
            Product p = productMapper.findById(item.getProductId());
            OrderItem oi = new OrderItem();
            oi.setOrderId(order.getId());
            oi.setProductId(p.getId());
            oi.setProductName(p.getName());
            oi.setPrice(p.getPrice());
            oi.setQuantity(item.getQuantity());
            orderMapper.insertItem(oi);
        }}
        cartMapper.clearCart(userId);
        return order;
    }}
}}
''')
        
        # Controller
        controller_dir = src_main / "controller"
        controller_dir.mkdir(exist_ok=True)
        
        self.write_file(controller_dir / "ProductController.java", f'''package {package_name}.controller;
import {package_name}.service.ProductService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.*;
@RestController @RequestMapping("/api/product") @CrossOrigin
public class ProductController {{
    @Autowired private ProductService productService;
    @GetMapping("/list") public Map<String,Object> list() {{ Map<String,Object> r=new HashMap<>(); r.put("code",200); r.put("data",productService.findAll()); return r; }}
    @GetMapping("/{{id}}") public Map<String,Object> detail(@PathVariable Long id) {{ Map<String,Object> r=new HashMap<>(); r.put("code",200); r.put("data",productService.findById(id)); return r; }}
    @GetMapping("/search") public Map<String,Object> search(@RequestParam String q) {{ Map<String,Object> r=new HashMap<>(); r.put("code",200); r.put("data",productService.search(q)); return r; }}
}}
''')
        
        self.write_file(controller_dir / "CartController.java", f'''package {package_name}.controller;
import {package_name}.service.CartService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.*;
@RestController @RequestMapping("/api/cart") @CrossOrigin
public class CartController {{
    @Autowired private CartService cartService;
    @GetMapping("/{{userId}}") public Map<String,Object> getCart(@PathVariable Long userId) {{ Map<String,Object> r=new HashMap<>(); r.put("code",200); r.put("data",cartService.getCart(userId)); return r; }}
    @PostMapping("/add") public Map<String,Object> add(@RequestParam Long userId, @RequestParam Long productId, @RequestParam(defaultValue="1") Integer quantity) {{ Map<String,Object> r=new HashMap<>(); cartService.addToCart(userId, productId, quantity); r.put("code",200); r.put("message","已加入购物车"); return r; }}
    @DeleteMapping("/{{id}}") public Map<String,Object> remove(@PathVariable Long id) {{ Map<String,Object> r=new HashMap<>(); cartService.removeFromCart(id); r.put("code",200); return r; }}
}}
''')
        
        self.write_file(controller_dir / "OrderController.java", f'''package {package_name}.controller;
import {package_name}.service.OrderService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.*;
@RestController @RequestMapping("/api/order") @CrossOrigin
public class OrderController {{
    @Autowired private OrderService orderService;
    @GetMapping("/{{userId}}") public Map<String,Object> list(@PathVariable Long userId) {{ Map<String,Object> r=new HashMap<>(); r.put("code",200); r.put("data",orderService.getOrders(userId)); return r; }}
    @PostMapping("/create") public Map<String,Object> create(@RequestParam Long userId, @RequestParam String address) {{ Map<String,Object> r=new HashMap<>(); r.put("code",200); r.put("data",orderService.createOrder(userId, address)); return r; }}
}}
''')
    
    def _generate_frontend(self, frontend_dir: Path, config: Dict):
        project_name_cn = config.get("project_name_cn", "电商购物平台")
        
        self.write_file(frontend_dir / "package.json", '{"name":"shop-frontend","scripts":{"dev":"vite"},"dependencies":{"vue":"^3.4.0","vue-router":"^4.2.0","axios":"^1.6.0","element-plus":"^2.4.0"},"devDependencies":{"@vitejs/plugin-vue":"^5.0.0","vite":"^5.0.0"}}')
        self.write_file(frontend_dir / "vite.config.js", 'import{defineConfig}from"vite";import vue from"@vitejs/plugin-vue";export default defineConfig({plugins:[vue()],server:{port:5173,proxy:{"/api":"http://localhost:8080"}}})')
        self.write_file(frontend_dir / "index.html", f'<!DOCTYPE html><html><head><meta charset="UTF-8"><title>{project_name_cn}</title></head><body><div id="app"></div><script type="module" src="/src/main.js"></script></body></html>')
        
        src = frontend_dir / "src"
        src.mkdir(exist_ok=True)
        self.write_file(src / "main.js", 'import{createApp}from"vue";import ElementPlus from"element-plus";import"element-plus/dist/index.css";import App from"./App.vue";import router from"./router";createApp(App).use(ElementPlus).use(router).mount("#app")')
        
        self.write_file(src / "App.vue", f'''<template>
<el-container style="height:100vh">
  <el-header style="background:linear-gradient(135deg,#ff6b6b,#feca57);color:#fff;display:flex;align-items:center;justify-content:space-between">
    <h1>🛒 {project_name_cn}</h1>
    <div><el-button @click="$router.push('/cart')">购物车</el-button></div>
  </el-header>
  <el-main style="background:#f5f5f5;padding:20px"><router-view /></el-main>
</el-container>
</template>
''')
        
        router_dir = src / "router"
        router_dir.mkdir(exist_ok=True)
        self.write_file(router_dir / "index.js", 'import{createRouter,createWebHistory}from"vue-router";export default createRouter({history:createWebHistory(),routes:[{path:"/",component:()=>import("../views/ProductList.vue")},{path:"/product/:id",component:()=>import("../views/ProductDetail.vue")},{path:"/cart",component:()=>import("../views/Cart.vue")},{path:"/orders",component:()=>import("../views/OrderList.vue")}]})')
        
        views_dir = src / "views"
        views_dir.mkdir(exist_ok=True)
        
        self.write_file(views_dir / "ProductList.vue", '''<template>
<div><el-input v-model="keyword" placeholder="搜索商品" style="width:300px;margin-bottom:20px" @keyup.enter="search" />
<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:20px">
  <el-card v-for="p in products" :key="p.id" shadow="hover" style="cursor:pointer" @click="$router.push('/product/'+p.id)">
    <img :src="p.image||'https://via.placeholder.com/200'" style="width:100%;height:150px;object-fit:cover" />
    <h3>{{p.name}}</h3>
    <p style="color:#f56c6c;font-size:20px">¥{{p.price}}</p>
    <el-button type="primary" size="small" @click.stop="addCart(p.id)">加入购物车</el-button>
  </el-card>
</div></div>
</template>
<script setup>
import{ref,onMounted}from"vue";import axios from"axios";import{ElMessage}from"element-plus";
const products=ref([]);const keyword=ref("");
const fetch=async()=>{const r=await axios.get("/api/product/list");products.value=r.data.data||[]};
const search=async()=>{const r=await axios.get("/api/product/search",{params:{q:keyword.value}});products.value=r.data.data||[]};
const addCart=async(id)=>{await axios.post("/api/cart/add",null,{params:{userId:1,productId:id}});ElMessage.success("已加入购物车")};
onMounted(fetch);
</script>
''')
        
        self.write_file(views_dir / "ProductDetail.vue", '''<template>
<el-card v-if="product"><el-row :gutter="40">
  <el-col :span="10"><img :src="product.image||'https://via.placeholder.com/400'" style="width:100%" /></el-col>
  <el-col :span="14"><h1>{{product.name}}</h1><p style="color:#f56c6c;font-size:32px">¥{{product.price}}</p><p>{{product.description}}</p><p>库存: {{product.stock}}</p>
    <el-button type="primary" size="large" @click="addCart">加入购物车</el-button>
  </el-col>
</el-row></el-card>
</template>
<script setup>
import{ref,onMounted}from"vue";import{useRoute}from"vue-router";import axios from"axios";import{ElMessage}from"element-plus";
const route=useRoute();const product=ref(null);
onMounted(async()=>{const r=await axios.get("/api/product/"+route.params.id);product.value=r.data.data});
const addCart=async()=>{await axios.post("/api/cart/add",null,{params:{userId:1,productId:product.value.id}});ElMessage.success("已加入购物车")};
</script>
''')
        
        self.write_file(views_dir / "Cart.vue", '''<template>
<el-card><template #header>购物车</template>
<el-table :data="items"><el-table-column label="商品">{{row.product?.name}}</el-table-column><el-table-column prop="quantity" label="数量" /><el-table-column label="操作"><template #default="{row}"><el-button size="small" type="danger" @click="remove(row.id)">删除</el-button></template></el-table-column></el-table>
<div style="margin-top:20px;text-align:right"><el-button type="primary" @click="checkout">结算</el-button></div>
</el-card>
</template>
<script setup>
import{ref,onMounted}from"vue";import axios from"axios";import{ElMessage}from"element-plus";
const items=ref([]);
const fetch=async()=>{const r=await axios.get("/api/cart/1");items.value=r.data.data||[]};
const remove=async(id)=>{await axios.delete("/api/cart/"+id);fetch()};
const checkout=async()=>{await axios.post("/api/order/create",null,{params:{userId:1,address:"默认地址"}});ElMessage.success("下单成功");fetch()};
onMounted(fetch);
</script>
''')
        
        self.write_file(views_dir / "OrderList.vue", '''<template><el-card><template #header>我的订单</template><el-table :data="orders"><el-table-column prop="orderNo" label="订单号" /><el-table-column prop="totalAmount" label="金额" /><el-table-column prop="status" label="状态"><template #default="{row}">{{["待支付","已支付","已发货","已完成","已取消"][row.status]}}</template></el-table-column><el-table-column prop="createTime" label="下单时间" /></el-table></el-card></template>
<script setup>import{ref,onMounted}from"vue";import axios from"axios";const orders=ref([]);onMounted(async()=>{const r=await axios.get("/api/order/1");orders.value=r.data.data||[]})</script>
''')
    
    def _generate_database(self, db_dir: Path, config: Dict):
        db_name = config.get("db_name", "shop_db")
        db_dir.mkdir(exist_ok=True)
        self.write_file(db_dir / "init.sql", f'''CREATE DATABASE IF NOT EXISTS {db_name} DEFAULT CHARSET utf8mb4; USE {db_name};
CREATE TABLE product (id BIGINT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(200), description TEXT, price DECIMAL(10,2), stock INT, image VARCHAR(500), category_id BIGINT, status INT DEFAULT 1);
CREATE TABLE user (id BIGINT PRIMARY KEY AUTO_INCREMENT, username VARCHAR(50) UNIQUE, password VARCHAR(100), nickname VARCHAR(50), phone VARCHAR(20), address VARCHAR(200));
CREATE TABLE cart_item (id BIGINT PRIMARY KEY AUTO_INCREMENT, user_id BIGINT, product_id BIGINT, quantity INT, UNIQUE KEY(user_id, product_id));
CREATE TABLE `order` (id BIGINT PRIMARY KEY AUTO_INCREMENT, order_no VARCHAR(50), user_id BIGINT, total_amount DECIMAL(10,2), status INT, address VARCHAR(200), create_time DATETIME);
CREATE TABLE order_item (id BIGINT PRIMARY KEY AUTO_INCREMENT, order_id BIGINT, product_id BIGINT, product_name VARCHAR(200), price DECIMAL(10,2), quantity INT);
INSERT INTO product (name, description, price, stock, image) VALUES ('iPhone 15 Pro','苹果最新旗舰手机',8999,100,'https://via.placeholder.com/200'),('MacBook Pro','M3芯片笔记本电脑',14999,50,'https://via.placeholder.com/200'),('AirPods Pro','主动降噪耳机',1899,200,'https://via.placeholder.com/200');
INSERT INTO user (username, password, nickname) VALUES ('user1','123456','测试用户');
''')
    
    def _generate_readme(self, output_dir: Path, config: Dict):
        self.write_file(output_dir / "README.md", f'''# {config.get("project_name_cn", "电商购物平台")}
基于 Spring Boot + Vue 3 + MySQL 的在线购物商城系统。
## 功能：商品展示、购物车、订单管理
## 启动：执行SQL -> mvn spring-boot:run -> npm run dev
## 作者：{config.get("author", "Student")}
''')
    
    def _generate_report(self, docs_dir: Path, config: Dict):
        docs_dir.mkdir(exist_ok=True)
        self.write_file(docs_dir / "实验报告.md", f'''# {config.get("project_name_cn", "电商购物平台")} 课程设计报告
## 一、设计目的：掌握电商系统开发流程
## 二、系统功能：商品浏览、购物车、下单结算、订单管理
## 三、技术栈：Spring Boot + MyBatis + Vue 3 + Element Plus
## 四、总结：成功完成电商平台开发
## 作者：{config.get("author", "Student")}
''')
