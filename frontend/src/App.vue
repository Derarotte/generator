<template>
  <div class="app-container">
    <!-- 顶部导航 -->
    <header class="app-header">
      <div class="logo" @click="$router.push('/')">
        <span class="logo-icon">🎓</span>
        <span class="logo-text gradient-text">作业代码生成器</span>
      </div>
      <nav class="nav-links">
        <a href="/" class="nav-link active">首页</a>
        <a href="#" class="nav-link">模板市场</a>
        <a href="#" class="nav-link">帮助文档</a>
      </nav>
    </header>
    
    <!-- 主内容区 -->
    <main class="app-main">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    
    <!-- 底部 -->
    <footer class="app-footer">
      <p>中国学生作业代码生成器 © 2026 | 让作业更轻松 ✨</p>
    </footer>
  </div>
</template>

<script setup>
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 60px;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.logo:hover {
  transform: scale(1.05);
}

.logo-icon {
  font-size: 32px;
  animation: float 3s ease-in-out infinite;
}

.logo-text {
  font-size: 24px;
  font-weight: 700;
}

.nav-links {
  display: flex;
  gap: 32px;
}

.nav-link {
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 15px;
  transition: color 0.3s ease;
  position: relative;
}

.nav-link:hover,
.nav-link.active {
  color: white;
}

.nav-link.active::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
  border-radius: 1px;
}

.app-main {
  flex: 1;
  padding: 40px 60px;
}

.app-footer {
  text-align: center;
  padding: 24px;
  color: var(--text-secondary);
  font-size: 14px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

/* 页面过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

@media (max-width: 768px) {
  .app-header {
    padding: 16px 20px;
    flex-direction: column;
    gap: 16px;
  }
  
  .app-main {
    padding: 20px;
  }
}
</style>
