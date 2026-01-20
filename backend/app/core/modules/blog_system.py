"""
个人博客系统生成器 - Flask + Vue 博客
"""
from pathlib import Path
from typing import Dict, Any
from app.core.modules.base import BaseGenerator


class BlogSystemGenerator(BaseGenerator):
    """博客系统生成器"""
    
    def __init__(self):
        super().__init__()
        self.name = "个人博客系统"
    
    async def generate(self, config: Dict[str, Any], output_dir: Path, templates_dir: Path) -> Dict[str, Any]:
        try:
            self._generate_backend(output_dir / "backend", config)
            self._generate_frontend(output_dir / "frontend", config)
            self._generate_readme(output_dir, config)
            self._generate_report(output_dir / "docs", config)
            
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _generate_backend(self, backend_dir: Path, config: Dict):
        """生成Flask后端"""
        backend_dir.mkdir(parents=True, exist_ok=True)
        
        self.write_file(backend_dir / "requirements.txt", '''flask
flask-cors
flask-sqlalchemy
''')
        
        self.write_file(backend_dir / "app.py", f'''"""
{config.get("project_name_cn", "个人博客系统")} - Flask后端
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# 数据库配置
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "blog.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ==================== 模型 ====================

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    articles = db.relationship("Article", backref="category", lazy=True)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

article_tags = db.Table("article_tags",
    db.Column("article_id", db.Integer, db.ForeignKey("article.id")),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"))
)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.String(500))
    cover_image = db.Column(db.String(500))
    views = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    tags = db.relationship("Tag", secondary=article_tags, backref="articles")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {{
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "summary": self.summary,
            "cover_image": self.cover_image,
            "views": self.views,
            "category": self.category.name if self.category else None,
            "category_id": self.category_id,
            "tags": [t.name for t in self.tags],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }}

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey("article.id"), nullable=False)
    nickname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100))
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {{
            "id": self.id,
            "article_id": self.article_id,
            "nickname": self.nickname,
            "content": self.content,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }}

# ==================== API ====================

@app.route("/")
def index():
    return jsonify({{"message": "{config.get("project_name_cn", "个人博客系统")} API", "status": "running"}})

# 文章API
@app.route("/api/articles")
def get_articles():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    category_id = request.args.get("category_id", type=int)
    
    query = Article.query.order_by(Article.created_at.desc())
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({{
        "articles": [a.to_dict() for a in pagination.items],
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": page
    }})

@app.route("/api/articles/<int:id>")
def get_article(id):
    article = Article.query.get_or_404(id)
    article.views += 1
    db.session.commit()
    return jsonify(article.to_dict())

@app.route("/api/articles", methods=["POST"])
def create_article():
    data = request.json
    article = Article(
        title=data["title"],
        content=data["content"],
        summary=data.get("summary", data["content"][:200]),
        cover_image=data.get("cover_image"),
        category_id=data.get("category_id")
    )
    db.session.add(article)
    db.session.commit()
    return jsonify(article.to_dict()), 201

@app.route("/api/articles/<int:id>", methods=["PUT"])
def update_article(id):
    article = Article.query.get_or_404(id)
    data = request.json
    article.title = data.get("title", article.title)
    article.content = data.get("content", article.content)
    article.summary = data.get("summary", article.summary)
    article.cover_image = data.get("cover_image", article.cover_image)
    article.category_id = data.get("category_id", article.category_id)
    db.session.commit()
    return jsonify(article.to_dict())

@app.route("/api/articles/<int:id>", methods=["DELETE"])
def delete_article(id):
    article = Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    return jsonify({{"message": "删除成功"}})

# 分类API
@app.route("/api/categories")
def get_categories():
    categories = Category.query.all()
    return jsonify([{{"id": c.id, "name": c.name, "count": len(c.articles)}} for c in categories])

@app.route("/api/categories", methods=["POST"])
def create_category():
    data = request.json
    category = Category(name=data["name"])
    db.session.add(category)
    db.session.commit()
    return jsonify({{"id": category.id, "name": category.name}}), 201

# 评论API
@app.route("/api/articles/<int:article_id>/comments")
def get_comments(article_id):
    comments = Comment.query.filter_by(article_id=article_id).order_by(Comment.created_at.desc()).all()
    return jsonify([c.to_dict() for c in comments])

@app.route("/api/articles/<int:article_id>/comments", methods=["POST"])
def create_comment(article_id):
    data = request.json
    comment = Comment(
        article_id=article_id,
        nickname=data["nickname"],
        email=data.get("email"),
        content=data["content"]
    )
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_dict()), 201

# 统计API
@app.route("/api/stats")
def get_stats():
    return jsonify({{
        "articles_count": Article.query.count(),
        "categories_count": Category.query.count(),
        "comments_count": Comment.query.count(),
        "total_views": db.session.query(db.func.sum(Article.views)).scalar() or 0
    }})

# 初始化数据库
def init_db():
    db.create_all()
    # 添加示例分类
    if Category.query.count() == 0:
        categories = ["技术", "生活", "随笔", "教程"]
        for name in categories:
            db.session.add(Category(name=name))
        db.session.commit()
    # 添加示例文章
    if Article.query.count() == 0:
        articles = [
            ("欢迎来到我的博客", "这是我的第一篇博客文章，欢迎大家！", 1),
            ("Python入门教程", "Python是一门简单易学的编程语言...", 4),
            ("Vue 3新特性介绍", "Vue 3带来了许多新特性，包括Composition API...", 1),
        ]
        for title, content, cat_id in articles:
            db.session.add(Article(title=title, content=content, summary=content[:100], category_id=cat_id))
        db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(debug=True, port=5000)
''')
    
    def _generate_frontend(self, frontend_dir: Path, config: Dict):
        """生成Vue前端"""
        project_name_cn = config.get("project_name_cn", "个人博客系统")
        
        self.write_file(frontend_dir / "package.json", '''{
  "name": "blog-frontend",
  "scripts": { "dev": "vite", "build": "vite build" },
  "dependencies": {
    "vue": "^3.4.0",
    "vue-router": "^4.2.0",
    "axios": "^1.6.0",
    "marked": "^11.0.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.0",
    "vite": "^5.0.0"
  }
}
''')
        
        self.write_file(frontend_dir / "vite.config.js", '''import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
export default defineConfig({
  plugins: [vue()],
  server: { port: 3000, proxy: { '/api': 'http://localhost:5000' } }
})
''')
        
        self.write_file(frontend_dir / "index.html", f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{project_name_cn}</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&display=swap" rel="stylesheet">
</head>
<body>
  <div id="app"></div>
  <script type="module" src="/src/main.js"></script>
</body>
</html>
''')
        
        src = frontend_dir / "src"
        src.mkdir(exist_ok=True)
        
        self.write_file(src / "main.js", '''import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './style.css'
createApp(App).use(router).mount('#app')
''')
        
        self.write_file(src / "style.css", '''* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Noto Serif SC', serif; background: #f8f9fa; color: #333; line-height: 1.8; }
a { color: #2c3e50; text-decoration: none; }
a:hover { color: #3498db; }
.container { max-width: 1000px; margin: 0 auto; padding: 0 20px; }
''')
        
        self.write_file(src / "App.vue", f'''<template>
  <div id="app">
    <header class="header">
      <div class="container">
        <h1 class="logo" @click="$router.push('/')">📝 {project_name_cn}</h1>
        <nav class="nav">
          <router-link to="/">首页</router-link>
          <router-link to="/archives">归档</router-link>
          <router-link to="/about">关于</router-link>
        </nav>
      </div>
    </header>
    <main class="main"><div class="container"><router-view /></div></main>
    <footer class="footer"><p>© 2024 {project_name_cn} | Powered by Flask + Vue</p></footer>
  </div>
</template>

<style scoped>
.header {{ background: #fff; box-shadow: 0 2px 10px rgba(0,0,0,0.1); padding: 20px 0; position: sticky; top: 0; z-index: 100; }}
.header .container {{ display: flex; justify-content: space-between; align-items: center; }}
.logo {{ font-size: 24px; cursor: pointer; }}
.nav {{ display: flex; gap: 30px; }}
.nav a {{ font-size: 16px; }}
.nav a.router-link-active {{ color: #3498db; border-bottom: 2px solid #3498db; }}
.main {{ min-height: calc(100vh - 200px); padding: 40px 0; }}
.footer {{ text-align: center; padding: 30px; color: #999; font-size: 14px; }}
</style>
''')
        
        router_dir = src / "router"
        router_dir.mkdir(exist_ok=True)
        self.write_file(router_dir / "index.js", '''import { createRouter, createWebHistory } from 'vue-router'
export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: () => import('../views/Home.vue') },
    { path: '/article/:id', component: () => import('../views/Article.vue') },
    { path: '/archives', component: () => import('../views/Archives.vue') },
    { path: '/about', component: () => import('../views/About.vue') }
  ]
})
''')
        
        views_dir = src / "views"
        views_dir.mkdir(exist_ok=True)
        
        self.write_file(views_dir / "Home.vue", '''<template>
  <div class="home">
    <div class="articles">
      <article v-for="article in articles" :key="article.id" class="article-card" @click="$router.push('/article/' + article.id)">
        <h2 class="article-title">{{ article.title }}</h2>
        <div class="article-meta">
          <span>📅 {{ formatDate(article.created_at) }}</span>
          <span>📁 {{ article.category || '未分类' }}</span>
          <span>👁️ {{ article.views }}</span>
        </div>
        <p class="article-summary">{{ article.summary }}</p>
      </article>
    </div>
    <div class="pagination" v-if="totalPages > 1">
      <button @click="page--" :disabled="page <= 1">上一页</button>
      <span>{{ page }} / {{ totalPages }}</span>
      <button @click="page++" :disabled="page >= totalPages">下一页</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'

const articles = ref([])
const page = ref(1)
const totalPages = ref(1)

const fetchArticles = async () => {
  const res = await axios.get('/api/articles', { params: { page: page.value, per_page: 10 } })
  articles.value = res.data.articles
  totalPages.value = res.data.pages
}

const formatDate = (date) => date ? new Date(date).toLocaleDateString('zh-CN') : ''

onMounted(fetchArticles)
watch(page, fetchArticles)
</script>

<style scoped>
.article-card { background: #fff; padding: 30px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); cursor: pointer; transition: transform 0.3s, box-shadow 0.3s; }
.article-card:hover { transform: translateY(-5px); box-shadow: 0 5px 20px rgba(0,0,0,0.1); }
.article-title { font-size: 24px; margin-bottom: 15px; }
.article-meta { color: #999; font-size: 14px; margin-bottom: 15px; display: flex; gap: 20px; }
.article-summary { color: #666; }
.pagination { display: flex; justify-content: center; align-items: center; gap: 20px; margin-top: 30px; }
.pagination button { padding: 10px 20px; border: none; background: #3498db; color: #fff; border-radius: 5px; cursor: pointer; }
.pagination button:disabled { background: #ccc; cursor: not-allowed; }
</style>
''')
        
        self.write_file(views_dir / "Article.vue", '''<template>
  <div class="article-page" v-if="article">
    <h1 class="title">{{ article.title }}</h1>
    <div class="meta">
      <span>📅 {{ formatDate(article.created_at) }}</span>
      <span>📁 {{ article.category || '未分类' }}</span>
      <span>👁️ {{ article.views }}</span>
    </div>
    <div class="content" v-html="article.content"></div>
    <div class="comments-section">
      <h3>评论 ({{ comments.length }})</h3>
      <div class="comment-form">
        <input v-model="newComment.nickname" placeholder="昵称" />
        <textarea v-model="newComment.content" placeholder="写下你的评论..."></textarea>
        <button @click="submitComment">发表评论</button>
      </div>
      <div class="comments-list">
        <div v-for="c in comments" :key="c.id" class="comment">
          <strong>{{ c.nickname }}</strong>
          <span class="time">{{ formatDate(c.created_at) }}</span>
          <p>{{ c.content }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const article = ref(null)
const comments = ref([])
const newComment = ref({ nickname: '', content: '' })

const formatDate = (date) => date ? new Date(date).toLocaleDateString('zh-CN') : ''

const fetchArticle = async () => {
  const res = await axios.get('/api/articles/' + route.params.id)
  article.value = res.data
}

const fetchComments = async () => {
  const res = await axios.get('/api/articles/' + route.params.id + '/comments')
  comments.value = res.data
}

const submitComment = async () => {
  if (!newComment.value.nickname || !newComment.value.content) return
  await axios.post('/api/articles/' + route.params.id + '/comments', newComment.value)
  newComment.value = { nickname: '', content: '' }
  fetchComments()
}

onMounted(() => { fetchArticle(); fetchComments(); })
</script>

<style scoped>
.article-page { background: #fff; padding: 40px; border-radius: 8px; }
.title { font-size: 32px; margin-bottom: 20px; }
.meta { color: #999; margin-bottom: 30px; display: flex; gap: 20px; }
.content { font-size: 18px; line-height: 2; }
.comments-section { margin-top: 50px; border-top: 1px solid #eee; padding-top: 30px; }
.comment-form { margin-bottom: 30px; }
.comment-form input, .comment-form textarea { width: 100%; padding: 10px; margin-bottom: 10px; border: 1px solid #ddd; border-radius: 5px; }
.comment-form textarea { height: 100px; }
.comment-form button { padding: 10px 30px; background: #3498db; color: #fff; border: none; border-radius: 5px; cursor: pointer; }
.comment { padding: 15px 0; border-bottom: 1px solid #eee; }
.comment .time { color: #999; font-size: 12px; margin-left: 10px; }
</style>
''')
        
        self.write_file(views_dir / "Archives.vue", '''<template>
  <div class="archives">
    <h2>归档</h2>
    <div class="timeline">
      <div v-for="article in articles" :key="article.id" class="timeline-item" @click="$router.push('/article/' + article.id)">
        <span class="date">{{ formatDate(article.created_at) }}</span>
        <span class="title">{{ article.title }}</span>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
const articles = ref([])
const formatDate = (d) => d ? new Date(d).toLocaleDateString('zh-CN') : ''
onMounted(async () => { const r = await axios.get('/api/articles?per_page=100'); articles.value = r.data.articles })
</script>
<style scoped>
.archives h2 { margin-bottom: 30px; }
.timeline-item { padding: 15px 0; border-left: 2px solid #3498db; padding-left: 20px; cursor: pointer; }
.timeline-item:hover .title { color: #3498db; }
.date { color: #999; margin-right: 20px; }
</style>
''')
        
        self.write_file(views_dir / "About.vue", f'''<template>
  <div class="about">
    <h2>关于我</h2>
    <p>欢迎来到 {project_name_cn}！</p>
    <p>这是一个基于 Flask + Vue 3 开发的个人博客系统。</p>
    <h3>统计</h3>
    <ul>
      <li>文章数: {{{{ stats.articles_count }}}}</li>
      <li>分类数: {{{{ stats.categories_count }}}}</li>
      <li>评论数: {{{{ stats.comments_count }}}}</li>
      <li>总浏览: {{{{ stats.total_views }}}}</li>
    </ul>
  </div>
</template>
<script setup>
import {{ ref, onMounted }} from 'vue'
import axios from 'axios'
const stats = ref({{ articles_count: 0, categories_count: 0, comments_count: 0, total_views: 0 }})
onMounted(async () => {{ const r = await axios.get('/api/stats'); stats.value = r.data }})
</script>
<style scoped>
.about h2 {{ margin-bottom: 20px; }}
.about h3 {{ margin-top: 30px; margin-bottom: 15px; }}
.about ul {{ padding-left: 20px; }}
.about li {{ margin-bottom: 10px; }}
</style>
''')
    
    def _generate_readme(self, output_dir: Path, config: Dict):
        self.write_file(output_dir / "README.md", f'''# {config.get("project_name_cn", "个人博客系统")}

基于 Flask + Vue 3 的个人博客系统。

## 功能
- 文章发布与管理
- 分类管理
- 评论系统
- 文章归档

## 启动

### 后端
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### 前端
```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:3000

## 作者
{config.get("author", "Student")}
''')
    
    def _generate_report(self, docs_dir: Path, config: Dict):
        docs_dir.mkdir(exist_ok=True)
        self.write_file(docs_dir / "实验报告.md", f'''# {config.get("project_name_cn", "个人博客系统")} 课程设计报告

## 一、设计目的
掌握博客系统开发，学习Flask和Vue的使用。

## 二、技术栈
- 后端：Flask + SQLAlchemy + SQLite
- 前端：Vue 3 + Vue Router

## 三、功能模块
- 文章展示与详情
- 分类筛选
- 评论功能
- 归档页面

## 四、数据库设计
- Category: 分类表
- Article: 文章表
- Comment: 评论表
- Tag: 标签表

## 五、总结
成功完成博客系统开发，掌握了前后端分离的开发模式。

## 作者：{config.get("author", "Student")}
''')
