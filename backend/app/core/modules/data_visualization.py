"""
数据可视化大屏生成器 - 基于Python的数据分析与可视化系统
"""
from pathlib import Path
from typing import Dict, Any
from app.core.modules.base import BaseGenerator


class DataVisualizationGenerator(BaseGenerator):
    """数据可视化大屏生成器"""
    
    def __init__(self):
        super().__init__()
        self.name = "数据可视化大屏"
    
    async def generate(self, config: Dict[str, Any], output_dir: Path, templates_dir: Path) -> Dict[str, Any]:
        try:
            data_source = config.get("data_source", "csv")
            
            self._generate_backend(output_dir / "backend", config, data_source)
            self._generate_frontend(output_dir / "frontend", config)
            self._generate_sample_data(output_dir / "data", config)
            self._generate_readme(output_dir, config)
            self._generate_report(output_dir / "docs", config)
            
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _generate_backend(self, backend_dir: Path, config: Dict, data_source: str):
        """生成FastAPI后端"""
        backend_dir.mkdir(parents=True, exist_ok=True)
        
        self.write_file(backend_dir / "requirements.txt", '''fastapi
uvicorn
pandas
numpy
aiofiles
python-multipart
''')
        
        self.write_file(backend_dir / "main.py", f'''"""
{config.get("project_name_cn", "数据可视化大屏")} - FastAPI后端
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import pandas as pd
import numpy as np
from pathlib import Path
import json

app = FastAPI(title="{config.get("project_name_cn", "数据可视化大屏")}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据目录
DATA_DIR = Path(__file__).parent.parent / "data"

def load_sales_data():
    """加载销售数据"""
    csv_path = DATA_DIR / "sales_data.csv"
    if csv_path.exists():
        return pd.read_csv(csv_path)
    return pd.DataFrame()

@app.get("/")
def root():
    return {{"message": "{config.get("project_name_cn", "数据可视化大屏")} API", "status": "running"}}

@app.get("/api/overview")
def get_overview():
    """获取概览数据"""
    df = load_sales_data()
    if df.empty:
        return {{"total_sales": 0, "total_orders": 0, "total_customers": 0, "avg_order": 0}}
    
    return {{
        "total_sales": float(df["amount"].sum()),
        "total_orders": len(df),
        "total_customers": df["customer_id"].nunique() if "customer_id" in df.columns else 0,
        "avg_order": float(df["amount"].mean()),
        "growth_rate": 12.5  # 模拟增长率
    }}

@app.get("/api/sales/trend")
def get_sales_trend():
    """获取销售趋势(按月)"""
    df = load_sales_data()
    if df.empty:
        return {{"labels": [], "data": []}}
    
    df["date"] = pd.to_datetime(df["date"])
    monthly = df.groupby(df["date"].dt.strftime("%Y-%m"))["amount"].sum().reset_index()
    monthly.columns = ["month", "amount"]
    
    return {{
        "labels": monthly["month"].tolist(),
        "data": monthly["amount"].tolist()
    }}

@app.get("/api/sales/by_category")
def get_sales_by_category():
    """获取分类销售占比"""
    df = load_sales_data()
    if df.empty or "category" not in df.columns:
        return {{"labels": [], "data": []}}
    
    by_cat = df.groupby("category")["amount"].sum().reset_index()
    
    return {{
        "labels": by_cat["category"].tolist(),
        "data": by_cat["amount"].tolist()
    }}

@app.get("/api/sales/by_region")
def get_sales_by_region():
    """获取区域销售分布"""
    df = load_sales_data()
    if df.empty or "region" not in df.columns:
        return {{"labels": [], "data": []}}
    
    by_region = df.groupby("region")["amount"].sum().reset_index()
    
    return {{
        "labels": by_region["region"].tolist(),
        "data": by_region["amount"].tolist()
    }}

@app.get("/api/sales/top_products")
def get_top_products():
    """获取热销商品TOP10"""
    df = load_sales_data()
    if df.empty or "product" not in df.columns:
        return []
    
    top = df.groupby("product")["amount"].sum().nlargest(10).reset_index()
    
    return [
        {{"name": row["product"], "value": float(row["amount"])}}
        for _, row in top.iterrows()
    ]

@app.get("/api/realtime")
def get_realtime_data():
    """模拟实时数据"""
    import random
    return {{
        "current_visitors": random.randint(100, 500),
        "orders_today": random.randint(50, 200),
        "revenue_today": random.randint(10000, 50000),
        "conversion_rate": round(random.uniform(2, 8), 2)
    }}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
''')
    
    def _generate_frontend(self, frontend_dir: Path, config: Dict):
        """生成Vue + ECharts前端"""
        project_name_cn = config.get("project_name_cn", "数据可视化大屏")
        
        self.write_file(frontend_dir / "package.json", '''{
  "name": "data-visualization",
  "scripts": { "dev": "vite", "build": "vite build" },
  "dependencies": {
    "vue": "^3.4.0",
    "axios": "^1.6.0",
    "echarts": "^5.4.0",
    "vue-echarts": "^6.6.0"
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
  server: { port: 3000, proxy: { '/api': 'http://localhost:8000' } }
})
''')
        
        self.write_file(frontend_dir / "index.html", f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{project_name_cn}</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ background: linear-gradient(135deg, #0c0c1e 0%, #1a1a3e 100%); min-height: 100vh; font-family: 'Microsoft YaHei', sans-serif; }}
  </style>
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
createApp(App).mount('#app')
''')
        
        self.write_file(src / "App.vue", f'''<template>
  <div class="dashboard">
    <!-- 头部 -->
    <header class="header">
      <h1>📊 {project_name_cn}</h1>
      <div class="time">{{{{ currentTime }}}}</div>
    </header>
    
    <!-- 概览卡片 -->
    <div class="overview-cards">
      <div class="card">
        <div class="card-value">¥{{{{ formatNumber(overview.total_sales) }}}}</div>
        <div class="card-label">总销售额</div>
      </div>
      <div class="card">
        <div class="card-value">{{{{ overview.total_orders }}}}</div>
        <div class="card-label">总订单数</div>
      </div>
      <div class="card">
        <div class="card-value">{{{{ overview.total_customers }}}}</div>
        <div class="card-label">客户数</div>
      </div>
      <div class="card">
        <div class="card-value">¥{{{{ formatNumber(overview.avg_order) }}}}</div>
        <div class="card-label">客单价</div>
      </div>
    </div>
    
    <!-- 图表区域 -->
    <div class="charts-container">
      <div class="chart-box">
        <h3>销售趋势</h3>
        <div ref="trendChart" class="chart"></div>
      </div>
      <div class="chart-box">
        <h3>分类销售占比</h3>
        <div ref="pieChart" class="chart"></div>
      </div>
      <div class="chart-box">
        <h3>区域销售分布</h3>
        <div ref="barChart" class="chart"></div>
      </div>
      <div class="chart-box">
        <h3>热销商品TOP10</h3>
        <div ref="topChart" class="chart"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {{ ref, onMounted, onUnmounted }} from 'vue'
import * as echarts from 'echarts'
import axios from 'axios'

const currentTime = ref('')
const overview = ref({{ total_sales: 0, total_orders: 0, total_customers: 0, avg_order: 0 }})

const trendChart = ref(null)
const pieChart = ref(null)
const barChart = ref(null)
const topChart = ref(null)

let charts = []
let timer = null

const formatNumber = (num) => {{
  return num ? num.toLocaleString('zh-CN', {{ maximumFractionDigits: 0 }}) : '0'
}}

const updateTime = () => {{
  currentTime.value = new Date().toLocaleString('zh-CN')
}}

const initCharts = async () => {{
  // 获取概览数据
  try {{
    const res = await axios.get('/api/overview')
    overview.value = res.data
  }} catch (e) {{
    console.error('获取概览数据失败', e)
  }}
  
  // 销售趋势图
  const trend = echarts.init(trendChart.value)
  charts.push(trend)
  try {{
    const res = await axios.get('/api/sales/trend')
    trend.setOption({{
      tooltip: {{ trigger: 'axis' }},
      xAxis: {{ type: 'category', data: res.data.labels, axisLabel: {{ color: '#fff' }} }},
      yAxis: {{ type: 'value', axisLabel: {{ color: '#fff' }} }},
      series: [{{ data: res.data.data, type: 'line', smooth: true, areaStyle: {{ color: 'rgba(64, 158, 255, 0.3)' }}, lineStyle: {{ color: '#409EFF' }} }}]
    }})
  }} catch (e) {{
    trend.setOption({{ title: {{ text: '暂无数据', left: 'center', top: 'center', textStyle: {{ color: '#fff' }} }} }})
  }}
  
  // 饼图
  const pie = echarts.init(pieChart.value)
  charts.push(pie)
  try {{
    const res = await axios.get('/api/sales/by_category')
    pie.setOption({{
      tooltip: {{ trigger: 'item' }},
      legend: {{ orient: 'vertical', left: 'left', textStyle: {{ color: '#fff' }} }},
      series: [{{ type: 'pie', radius: ['40%', '70%'], data: res.data.labels.map((l, i) => ({{ name: l, value: res.data.data[i] }})), label: {{ color: '#fff' }} }}]
    }})
  }} catch (e) {{}}
  
  // 柱状图
  const bar = echarts.init(barChart.value)
  charts.push(bar)
  try {{
    const res = await axios.get('/api/sales/by_region')
    bar.setOption({{
      tooltip: {{ trigger: 'axis' }},
      xAxis: {{ type: 'category', data: res.data.labels, axisLabel: {{ color: '#fff' }} }},
      yAxis: {{ type: 'value', axisLabel: {{ color: '#fff' }} }},
      series: [{{ data: res.data.data, type: 'bar', itemStyle: {{ color: '#67C23A' }} }}]
    }})
  }} catch (e) {{}}
  
  // 横向柱状图
  const top = echarts.init(topChart.value)
  charts.push(top)
  try {{
    const res = await axios.get('/api/sales/top_products')
    const names = res.data.map(d => d.name).reverse()
    const values = res.data.map(d => d.value).reverse()
    top.setOption({{
      tooltip: {{ trigger: 'axis' }},
      xAxis: {{ type: 'value', axisLabel: {{ color: '#fff' }} }},
      yAxis: {{ type: 'category', data: names, axisLabel: {{ color: '#fff' }} }},
      series: [{{ data: values, type: 'bar', itemStyle: {{ color: '#E6A23C' }} }}]
    }})
  }} catch (e) {{}}
}}

onMounted(() => {{
  updateTime()
  timer = setInterval(updateTime, 1000)
  initCharts()
  
  window.addEventListener('resize', () => {{
    charts.forEach(c => c.resize())
  }})
}})

onUnmounted(() => {{
  if (timer) clearInterval(timer)
  charts.forEach(c => c.dispose())
}})
</script>

<style scoped>
.dashboard {{
  min-height: 100vh;
  padding: 20px;
  color: #fff;
}}

.header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  margin-bottom: 20px;
}}

.header h1 {{
  font-size: 28px;
  background: linear-gradient(90deg, #409EFF, #67C23A);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}}

.time {{
  font-size: 18px;
  color: #a0aec0;
}}

.overview-cards {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}}

.card {{
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  padding: 20px;
  text-align: center;
  border: 1px solid rgba(255, 255, 255, 0.1);
}}

.card-value {{
  font-size: 32px;
  font-weight: bold;
  color: #409EFF;
  margin-bottom: 10px;
}}

.card-label {{
  font-size: 14px;
  color: #a0aec0;
}}

.charts-container {{
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}}

.chart-box {{
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  padding: 20px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}}

.chart-box h3 {{
  font-size: 16px;
  margin-bottom: 15px;
  color: #fff;
}}

.chart {{
  height: 300px;
}}

@media (max-width: 768px) {{
  .overview-cards {{ grid-template-columns: repeat(2, 1fr); }}
  .charts-container {{ grid-template-columns: 1fr; }}
}}
</style>
''')
    
    def _generate_sample_data(self, data_dir: Path, config: Dict):
        """生成示例CSV数据"""
        data_dir.mkdir(exist_ok=True)
        
        # 生成销售数据CSV
        import random
        from datetime import datetime, timedelta
        
        categories = ["电子产品", "服装", "食品", "家居", "美妆"]
        regions = ["华东", "华南", "华北", "西南", "东北"]
        products = [
            "iPhone 15", "MacBook Pro", "iPad Air", "AirPods", "Apple Watch",
            "华为Mate60", "小米14", "OPPO Find", "vivo X100", "荣耀Magic",
            "羽绒服", "运动鞋", "牛仔裤", "T恤", "连衣裙",
            "零食大礼包", "进口坚果", "牛奶礼盒", "咖啡豆", "茶叶",
            "床上四件套", "收纳箱", "台灯", "办公椅", "书架"
        ]
        
        lines = ["date,customer_id,product,category,region,amount,quantity"]
        
        start_date = datetime(2024, 1, 1)
        for i in range(1000):
            date = start_date + timedelta(days=random.randint(0, 365))
            customer_id = f"C{random.randint(1000, 9999)}"
            product = random.choice(products)
            category = random.choice(categories)
            region = random.choice(regions)
            quantity = random.randint(1, 5)
            amount = round(random.uniform(50, 2000) * quantity, 2)
            
            lines.append(f"{date.strftime('%Y-%m-%d')},{customer_id},{product},{category},{region},{amount},{quantity}")
        
        self.write_file(data_dir / "sales_data.csv", "\n".join(lines))
    
    def _generate_readme(self, output_dir: Path, config: Dict):
        self.write_file(output_dir / "README.md", f'''# {config.get("project_name_cn", "数据可视化大屏")}

## 项目简介
基于 FastAPI + Vue 3 + ECharts 的数据可视化大屏系统。

## 技术栈
- 后端：FastAPI + Pandas
- 前端：Vue 3 + ECharts
- 数据：CSV文件

## 快速开始

### 启动后端
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### 启动前端
```bash
cd frontend
npm install
npm run dev
```

### 访问
打开浏览器访问 http://localhost:3000

## 作者
{config.get("author", "Student")}
''')
    
    def _generate_report(self, docs_dir: Path, config: Dict):
        docs_dir.mkdir(exist_ok=True)
        self.write_file(docs_dir / "实验报告.md", f'''# {config.get("project_name_cn", "数据可视化大屏")} 课程设计报告

## 一、设计目的
掌握数据可视化技术，学习使用ECharts进行数据展示。

## 二、开发环境
- Python 3.8+, Node.js 18+
- FastAPI, Vue 3, ECharts

## 三、系统功能
- 销售数据概览
- 销售趋势分析
- 分类销售占比
- 区域销售分布
- 热销商品排行

## 四、数据说明
使用CSV文件存储1000条模拟销售数据，包含日期、客户、商品、分类、区域、金额等字段。

## 五、可视化实现
使用ECharts实现折线图、饼图、柱状图等多种图表类型。

## 六、总结
成功完成数据可视化大屏的开发，掌握了前后端分离的数据可视化方案。

## 作者：{config.get("author", "Student")}
''')
