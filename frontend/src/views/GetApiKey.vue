<template>
  <div class="api-key-page">
    <header class="header">
      <div class="header-left">
        <span class="logo-text">LLM Chat</span>
      </div>
      <div class="header-right">
        <router-link to="/" class="back-link">
          <el-icon><ArrowLeft /></el-icon>
          返回首页
        </router-link>
      </div>
    </header>

    <main class="main-content">
      <div class="container">
        <div class="card">
          <h1 class="title">获取 API KEY</h1>
          <p class="description">创建一个新的 API KEY 以开始使用 LLM Chat 服务</p>
          
          <el-form 
            :model="form" 
            :rules="rules" 
            ref="formRef" 
            class="api-key-form"
            @submit.prevent="handleGenerateKey"
          >
            <el-form-item label="API KEY 名称" prop="name">
              <el-input 
                v-model="form.name" 
                placeholder="请输入 API KEY 名称"
                size="large"
              />
            </el-form-item>
            
            <el-form-item>
              <el-button 
                type="primary" 
                size="large" 
                :loading="loading"
                @click="handleGenerateKey"
                class="generate-btn"
              >
                生成 API KEY
              </el-button>
            </el-form-item>
          </el-form>
          
          <div v-if="generatedKey" class="result-section">
            <h3>您的 API KEY 已生成：</h3>
            <div class="key-display">
              <el-input 
                v-model="generatedKey" 
                readonly 
                size="large"
                class="key-input"
              />
              <el-button 
                type="primary" 
                @click="copyToClipboard"
                class="copy-btn"
              >
                {{ copyButtonText }}
              </el-button>
            </div>
            <p class="warning">
              <el-icon><Warning /></el-icon>
              请妥善保管您的 API KEY，它只会显示一次。
            </p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ArrowLeft, Warning } from '@element-plus/icons-vue'
import { createApiKey } from '@/utils/apiKeys'
import { ElMessage } from 'element-plus'
const formRef = ref(null)
const loading = ref(false)
const generatedKey = ref('')
const copyButtonText = ref('复制')

const form = reactive({
  name: ''
})

const rules = {
  name: [
    { required: true, message: '请输入 API KEY 名称', trigger: 'blur' }
  ]
}

const handleGenerateKey = async () => {
  try {
    await formRef.value.validate()
    loading.value = true
    
    const data = await createApiKey(form.name)
    generatedKey.value = data.key
    
    ElMessage.success('API KEY 生成成功')
  } catch (error) {
    console.error('生成 API KEY 失败:', error)
    ElMessage.error('生成 API KEY 失败: ' + error.message)
  } finally {
    loading.value = false
  }
}

const copyToClipboard = async () => {
  try {
    await navigator.clipboard.writeText(generatedKey.value)
    copyButtonText.value = '已复制'
    setTimeout(() => {
      copyButtonText.value = '复制'
    }, 2000)
    ElMessage.success('API KEY 已复制到剪贴板')
  } catch (error) {
    console.error('复制失败:', error)
    ElMessage.error('复制失败')
  }
}
</script>

<style lang="scss" scoped>
.api-key-page {
  min-height: 100vh;
  background-color: var(--el-bg-color);
}

.header {
  height: 64px;
  padding: 0 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--el-border-color);
  background-color: var(--el-bg-color);

  .header-left {
    flex-shrink: 0;
    .logo-text {
      font-size: 20px;
      font-weight: 600;
      color: #171717;
      cursor: pointer;
      user-select: none;
      white-space: nowrap;
    }
  }

  .header-right {
    .back-link {
      display: flex;
      align-items: center;
      gap: 8px;
      text-decoration: none;
      color: var(--el-color-primary);
      font-size: 14px;
      
      &:hover {
        color: var(--el-color-primary-light-3);
      }
    }
  }
}

.main-content {
  padding: 40px 20px;
  
  .container {
    max-width: 600px;
    margin: 0 auto;
    
    .card {
      background: #fff;
      border-radius: 12px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
      padding: 40px;
      
      .title {
        font-size: 28px;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 16px;
        text-align: center;
      }
      
      .description {
        font-size: 16px;
        color: #666;
        text-align: center;
        margin-bottom: 32px;
      }
      
      .api-key-form {
        margin-bottom: 24px;
        
        :deep(.el-form-item__label) {
          font-weight: 500;
          color: #1a1a1a;
        }
        
        .generate-btn {
          width: 100%;
          margin-top: 24px;
        }
      }
      
      .result-section {
        margin-top: 32px;
        padding-top: 32px;
        border-top: 1px solid #eee;
        
        h3 {
          font-size: 18px;
          font-weight: 600;
          color: #1a1a1a;
          margin-bottom: 16px;
        }
        
        .key-display {
          display: flex;
          gap: 12px;
          margin-bottom: 16px;
          
          .key-input {
            flex: 1;
          }
          
          .copy-btn {
            flex-shrink: 0;
          }
        }
        
        .warning {
          display: flex;
          align-items: center;
          gap: 8px;
          font-size: 14px;
          color: #faad14;
          margin: 0;
          
          :deep(.el-icon) {
            font-size: 16px;
          }
        }
      }
    }
  }
}
</style>