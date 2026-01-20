# 部署指南

## 开发环境

### 后端

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 前端

```bash
cd frontend
npm install
npm run dev
```

## 生产环境

### Docker 部署 (推荐)

```bash
docker-compose up -d
```

### 手动部署

#### 后端

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### 前端

```bash
cd frontend
npm install
npm run build
# 部署 dist/ 到 Nginx
```

### Nginx 配置示例

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /var/www/generator/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # API 代理
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # 下载文件
    location /output {
        proxy_pass http://127.0.0.1:8000;
    }
}
```

## 环境变量

创建 `.env` 文件：

```env
# 应用配置
APP_NAME=中国学生作业代码生成器
DEBUG=false

# 日志
LOG_LEVEL=INFO

# 路径 (可选)
# TEMPLATES_DIR=/path/to/templates
# OUTPUT_DIR=/path/to/output
```

## 目录权限

确保以下目录可写：

- `output/` - 生成的项目文件
- `logs/` - 日志文件
- `data/` - 数据库文件

```bash
chmod 755 output logs data
```
