<template>
  <div class="generate-page">
    <div class="page-header">
      <el-button @click="$router.back()" plain>← 返回</el-button>
      <h1 class="page-title">
        <span class="module-icon">{{ moduleInfo?.icon }}</span>
        {{ moduleInfo?.name || '生成项目' }}
      </h1>
    </div>

    <div class="generate-content">
      <!-- 配置表单 -->
      <div class="config-panel glass-card">
        <h2>项目配置</h2>
        <el-form :model="config" label-position="top" class="config-form">
          <el-form-item v-for="field in moduleInfo?.fields" :key="field.name" :label="field.label">
            <el-input v-if="field.type === 'text'" v-model="config[field.name]" :placeholder="field.placeholder" />
            <el-select v-else-if="field.type === 'select'" v-model="config[field.name]" style="width: 100%">
              <el-option v-for="opt in field.options" :key="opt.value" :label="opt.label" :value="opt.value" />
            </el-select>
            <el-checkbox-group v-else-if="field.type === 'checkbox'" v-model="config[field.name]">
              <el-checkbox v-for="opt in field.options" :key="opt.value" :label="opt.value">{{ opt.label }}</el-checkbox>
            </el-checkbox-group>
          </el-form-item>
        </el-form>

        <div class="generate-actions">
          <button class="gradient-btn generate-btn" @click="generateProject" :disabled="generating">
            <span v-if="!generating">🚀 生成项目</span>
            <span v-else>⏳ 生成中...</span>
          </button>
        </div>
      </div>

      <!-- 预览/结果区 -->
      <div class="preview-panel glass-card">
        <h2>生成结果</h2>
        <div v-if="!result" class="preview-placeholder">
          <div class="placeholder-icon">📦</div>
          <p>配置参数后点击"生成项目"按钮</p>
        </div>
        <div v-else class="result-content">
          <div class="result-success" v-if="result.success">
            <div class="success-icon">✅</div>
            <h3>生成成功！</h3>
            <p>共 {{ result.files_count }} 个文件</p>
            <a :href="result.download_url" class="download-btn gradient-btn">
              📥 下载项目 (ZIP)
            </a>
          </div>
          <div class="result-error" v-else>
            <div class="error-icon">❌</div>
            <p>{{ result.message }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 技术栈信息 -->
    <div class="tech-info glass-card" v-if="moduleInfo">
      <h3>技术栈</h3>
      <div class="tech-tags">
        <span v-for="tech in moduleInfo.tech_stack" :key="tech" class="tech-tag">{{ tech }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const route = useRoute()
const moduleInfo = ref(null)
const config = reactive({})
const generating = ref(false)
const result = ref(null)

// 模块数据（后备）
const modulesData = {
  student_management: { id: 'student_management', name: '学生信息管理系统', icon: '🎓', category: '管理系统', tech_stack: ['Java', 'Spring Boot', 'MyBatis', 'Vue 3', 'MySQL'], fields: [
    { name: 'project_name', label: '项目名称', type: 'text', default: 'StudentManagementSystem', placeholder: '英文项目名' },
    { name: 'project_name_cn', label: '项目中文名', type: 'text', default: '学生信息管理系统' },
    { name: 'package_name', label: '包名', type: 'text', default: 'com.example.student' },
    { name: 'author', label: '作者', type: 'text', default: 'Student' },
    { name: 'db_name', label: '数据库名', type: 'text', default: 'student_db' },
  ]},
  library_management: { id: 'library_management', name: '图书管理系统', icon: '📚', category: '管理系统', tech_stack: ['Java', 'Spring Boot', 'MyBatis', 'Vue 3', 'MySQL'], fields: [
    { name: 'project_name', label: '项目名称', type: 'text', default: 'LibraryManagementSystem' },
    { name: 'project_name_cn', label: '项目中文名', type: 'text', default: '图书管理系统' },
    { name: 'package_name', label: '包名', type: 'text', default: 'com.example.library' },
    { name: 'author', label: '作者', type: 'text', default: 'Student' },
  ]},
}

// 获取模块信息
const fetchModuleInfo = async () => {
  const moduleId = route.params.moduleId
  try {
    const res = await axios.get(`/api/modules/${moduleId}`)
    moduleInfo.value = res.data
  } catch (e) {
    moduleInfo.value = modulesData[moduleId] || { name: '未知模块', icon: '❓', fields: [], tech_stack: [] }
  }
  
  // 初始化配置默认值
  if (moduleInfo.value?.fields) {
    moduleInfo.value.fields.forEach(f => {
      if (f.type === 'checkbox') {
        config[f.name] = f.options?.map(o => o.value) || []
      } else {
        config[f.name] = f.default || ''
      }
    })
  }
}

// 生成项目
const generateProject = async () => {
  generating.value = true
  result.value = null
  
  try {
    const res = await axios.post('/api/generator/generate', {
      module_id: route.params.moduleId,
      config: config
    })
    result.value = res.data
    if (res.data.success) {
      ElMessage.success('项目生成成功！')
    }
  } catch (e) {
    result.value = { success: false, message: e.response?.data?.detail || '生成失败' }
    ElMessage.error('生成失败')
  } finally {
    generating.value = false
  }
}

onMounted(fetchModuleInfo)
watch(() => route.params.moduleId, fetchModuleInfo)
</script>

<style scoped>
.generate-page { max-width: 1200px; margin: 0 auto; }

.page-header { display: flex; align-items: center; gap: 20px; margin-bottom: 32px; }
.page-title { font-size: 28px; display: flex; align-items: center; gap: 12px; }
.module-icon { font-size: 36px; }

.generate-content { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 24px; }

.config-panel h2, .preview-panel h2 { font-size: 18px; margin-bottom: 24px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 16px; }

.config-form { max-height: 400px; overflow-y: auto; padding-right: 12px; }

.generate-actions { margin-top: 24px; }
.generate-btn { width: 100%; padding: 16px; font-size: 18px; }
.generate-btn:disabled { opacity: 0.7; cursor: not-allowed; }

.preview-placeholder { text-align: center; padding: 60px 20px; color: var(--text-secondary); }
.placeholder-icon { font-size: 64px; margin-bottom: 16px; opacity: 0.5; }

.result-success, .result-error { text-align: center; padding: 40px 20px; }
.success-icon, .error-icon { font-size: 64px; margin-bottom: 16px; }
.result-success h3 { font-size: 24px; margin-bottom: 12px; color: var(--success-color); }
.download-btn { display: inline-block; margin-top: 24px; text-decoration: none; }

.tech-info h3 { font-size: 16px; margin-bottom: 16px; }
.tech-tags { display: flex; gap: 8px; flex-wrap: wrap; }
.tech-tag { padding: 6px 16px; background: rgba(102, 126, 234, 0.2); color: var(--primary-color); border-radius: 20px; font-size: 14px; }

@media (max-width: 768px) {
  .generate-content { grid-template-columns: 1fr; }
}
</style>
