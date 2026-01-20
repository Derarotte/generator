<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content animate-slide-up">
        <h1 class="hero-title">
          <span class="gradient-text">中国学生作业</span>
          <br>代码生成器
        </h1>
        <p class="hero-desc">
          选择作业类型 → 配置参数 → 一键生成完整项目
          <br>支持管理系统、Web应用、算法实验、数据分析等多种类型
        </p>
      </div>
    </section>

    <!-- 模块选择区 -->
    <section class="modules-section">
      <h2 class="section-title">选择作业类型</h2>
      
      <!-- 分类筛选 -->
      <div class="category-filter">
        <button 
          v-for="cat in categories" 
          :key="cat"
          :class="['filter-btn', { active: activeCategory === cat }]"
          @click="activeCategory = cat"
        >
          {{ cat }}
        </button>
      </div>

      <!-- 模块卡片 -->
      <div class="modules-grid">
        <div 
          v-for="mod in filteredModules" 
          :key="mod.id"
          class="module-card glass-card"
          @click="selectModule(mod)"
        >
          <div class="module-icon">{{ mod.icon }}</div>
          <h3 class="module-name">{{ mod.name }}</h3>
          <p class="module-desc">{{ mod.description }}</p>
          <div class="module-tech">
            <span v-for="tech in mod.tech_stack.slice(0, 3)" :key="tech" class="tech-tag">
              {{ tech }}
            </span>
          </div>
          <button class="select-btn gradient-btn">开始生成 →</button>
        </div>
      </div>
    </section>

    <!-- 特性介绍 -->
    <section class="features-section">
      <h2 class="section-title">为什么选择我们？</h2>
      <div class="features-grid">
        <div class="feature-card glass-card">
          <div class="feature-icon">⚡</div>
          <h3>一键生成</h3>
          <p>选择模块，配置参数，即刻生成完整可运行的项目代码</p>
        </div>
        <div class="feature-card glass-card">
          <div class="feature-icon">📝</div>
          <h3>配套文档</h3>
          <p>自动生成实验报告、README等中文文档，省时省力</p>
        </div>
        <div class="feature-card glass-card">
          <div class="feature-icon">🎯</div>
          <h3>针对性设计</h3>
          <p>专为中国高校作业场景设计，符合老师的要求</p>
        </div>
        <div class="feature-card glass-card">
          <div class="feature-icon">🔧</div>
          <h3>灵活配置</h3>
          <p>项目名称、功能模块、技术栈均可自定义配置</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const modules = ref([])
const activeCategory = ref('全部')

// 获取模块列表
const fetchModules = async () => {
  try {
    const res = await axios.get('/api/modules/')
    modules.value = res.data
  } catch (e) {
    // 使用静态数据作为后备
    modules.value = [
      { id: 'student_management', name: '学生信息管理系统', description: '完整的学生信息管理系统，包含学生、课程、成绩管理等功能', icon: '🎓', category: '管理系统', tech_stack: ['Java', 'Spring Boot', 'Vue 3', 'MySQL'] },
      { id: 'library_management', name: '图书管理系统', description: '图书馆管理系统，支持图书借阅、归还、用户管理等', icon: '📚', category: '管理系统', tech_stack: ['Java', 'Spring Boot', 'Vue 3', 'MySQL'] },
      { id: 'hotel_management', name: '酒店管理系统', description: '酒店房间预订与管理系统', icon: '🏨', category: '管理系统', tech_stack: ['Java', 'Spring Boot', 'Vue 3', 'MySQL'] },
      { id: 'ecommerce', name: '电商购物平台', description: '在线购物商城，包含商品展示、购物车、订单管理', icon: '🛒', category: 'Web应用', tech_stack: ['Java', 'Spring Boot', 'Vue 3', 'MySQL'] },
      { id: 'blog_system', name: '个人博客系统', description: '个人博客网站，支持文章发布、评论、分类标签', icon: '📝', category: 'Web应用', tech_stack: ['Python', 'Flask', 'Vue 3', 'SQLite'] },
      { id: 'data_visualization', name: '数据可视化大屏', description: '数据采集与可视化展示系统', icon: '📊', category: '数据分析', tech_stack: ['Python', 'FastAPI', 'ECharts', 'Vue 3'] },
      { id: 'algorithm_experiment', name: '算法实验项目', description: '数据结构与算法实验，包含排序、查找、图论等', icon: '🧮', category: '算法实验', tech_stack: ['C++', 'Python'] },
      { id: 'plane_game', name: '飞机大战游戏', description: '经典飞机大战游戏，包含玩家控制、敌机AI', icon: '✈️', category: '游戏开发', tech_stack: ['C++', 'EasyX'] },
    ]
  }
}

// 分类列表
const categories = computed(() => {
  const cats = ['全部', ...new Set(modules.value.map(m => m.category))]
  return cats
})

// 筛选后的模块
const filteredModules = computed(() => {
  if (activeCategory.value === '全部') return modules.value
  return modules.value.filter(m => m.category === activeCategory.value)
})

// 选择模块
const selectModule = (mod) => {
  router.push(`/generate/${mod.id}`)
}

onMounted(fetchModules)
</script>

<style scoped>
.home-page {
  max-width: 1400px;
  margin: 0 auto;
}

/* Hero */
.hero {
  text-align: center;
  padding: 60px 0 80px;
}

.hero-title {
  font-size: 56px;
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 24px;
}

.hero-desc {
  font-size: 18px;
  color: var(--text-secondary);
  line-height: 1.8;
}

/* Section */
.section-title {
  font-size: 32px;
  text-align: center;
  margin-bottom: 40px;
}

/* Category Filter */
.category-filter {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-bottom: 40px;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 10px 24px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: transparent;
  color: var(--text-secondary);
  border-radius: 30px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-btn:hover,
.filter-btn.active {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  border-color: transparent;
  color: white;
}

/* Modules Grid */
.modules-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 80px;
}

.module-card {
  cursor: pointer;
  text-align: center;
  padding: 32px 24px;
}

.module-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.module-name {
  font-size: 20px;
  margin-bottom: 12px;
}

.module-desc {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 20px;
  line-height: 1.6;
}

.module-tech {
  display: flex;
  justify-content: center;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 24px;
}

.tech-tag {
  padding: 4px 12px;
  background: rgba(102, 126, 234, 0.2);
  color: var(--primary-color);
  border-radius: 20px;
  font-size: 12px;
}

.select-btn {
  width: 100%;
  padding: 12px;
}

/* Features */
.features-section {
  padding: 60px 0;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 24px;
}

.feature-card {
  text-align: center;
}

.feature-icon {
  font-size: 40px;
  margin-bottom: 16px;
}

.feature-card h3 {
  font-size: 18px;
  margin-bottom: 12px;
}

.feature-card p {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 36px;
  }
}
</style>
