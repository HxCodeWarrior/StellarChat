<template>
  <div class="api-key-management-page">
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
          <div class="header-section">
            <h1 class="title">API Key 管理</h1>
            <p class="description">管理您的 API Key，包括创建、启用、停用和删除操作</p>
          </div>
          
          <!-- 创建 API Key 表单 -->
          <el-card class="create-card">
            <template #header>
              <div class="card-header">
                <span>创建新的 API Key</span>
              </div>
            </template>
            
            <el-form 
              :model="createForm" 
              :rules="createRules" 
              ref="createFormRef" 
              class="create-form"
              @submit.prevent="handleCreateKey"
            >
              <el-form-item label="API Key 名称" prop="name">
                <el-input 
                  v-model="createForm.name" 
                  placeholder="请输入 API Key 名称"
                  size="large"
                />
              </el-form-item>
              
              <el-form-item>
                <el-button 
                  type="primary" 
                  size="large" 
                  :loading="creating"
                  @click="handleCreateKey"
                  class="create-btn"
                >
                  创建 API Key
                </el-button>
              </el-form-item>
            </el-form>
          </el-card>
          
          <!-- API Key 列表 -->
          <el-card class="list-card">
            <template #header>
              <div class="card-header">
                <span>API Key 列表</span>
                <el-button @click="loadApiKeys" :loading="loading" size="small">
                  <el-icon><Refresh /></el-icon>
                  刷新
                </el-button>
              </div>
            </template>
            
            <el-table 
              :data="apiKeys" 
              v-loading="loading"
              empty-text="暂无 API Key"
              class="api-key-table"
            >
              <el-table-column prop="name" label="名称" />
              <el-table-column prop="created_at" label="创建时间" width="180">
                <template #default="scope">
                  {{ formatDate(scope.row.created_at) }}
                </template>
              </el-table-column>
              <el-table-column label="状态" width="100">
                <template #default="scope">
                  <el-tag :type="scope.row.is_active ? 'success' : 'danger'">
                    {{ scope.row.is_active ? '启用' : '停用' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="200">
                <template #default="scope">
                  <div class="action-buttons">
                    <el-button 
                      size="small" 
                      :type="scope.row.is_active ? 'danger' : 'success'"
                      @click="toggleApiKeyStatus(scope.row)"
                      :loading="scope.row.operating"
                    >
                      {{ scope.row.is_active ? '停用' : '启用' }}
                    </el-button>
                    <el-button 
                      size="small" 
                      type="danger" 
                      @click="handleDeleteApiKey(scope.row)"
                      :loading="scope.row.deleting"
                    >
                      删除
                    </el-button>
                  </div>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ArrowLeft, Refresh } from '@element-plus/icons-vue'
import {
  createApiKey,
  getApiKeys,
  deleteApiKey,
  deactivateApiKey,
  activateApiKey
} from '@/utils/apiKeys'
import { ElMessage, ElMessageBox } from 'element-plus'
const createFormRef = ref(null)
const loading = ref(false)
const creating = ref(false)

// 创建表单数据
const createForm = reactive({
  name: ''
})

// 创建表单验证规则
const createRules = {
  name: [
    { required: true, message: '请输入 API Key 名称', trigger: 'blur' }
  ]
}

// API Key 列表
const apiKeys = ref([])

// 格式化日期
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

// 获取 API Key 列表
const loadApiKeys = async () => {
  loading.value = true
  try {
    const data = await getApiKeys()
    // 为每个 API Key 添加操作状态字段
    apiKeys.value = data.map(key => ({
      ...key,
      operating: false,
      deleting: false
    }))
  } catch (error) {
    console.error('获取 API Key 列表失败:', error)
    ElMessage.error('获取 API Key 列表失败: ' + error.message)
  } finally {
    loading.value = false
  }
}

// 创建 API Key
const handleCreateKey = async () => {
  try {
    await createFormRef.value.validate()
    creating.value = true
    
    await createApiKey(createForm.name)
    
    // 重新加载 API Key 列表
    await loadApiKeys()
    
    // 重置表单
    createForm.name = ''
    
    // 显示成功消息
    ElMessage.success('API Key 创建成功')
  } catch (error) {
    console.error('创建 API Key 失败:', error)
    ElMessage.error('创建 API Key 失败: ' + error.message)
  } finally {
    creating.value = false
  }
}

// 删除 API Key
const handleDeleteApiKey = async (apiKey) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除这个 API Key 吗？此操作不可恢复。',
      '确认删除',
      {
        type: 'warning',
        confirmButtonText: '确定',
        cancelButtonText: '取消'
      }
    )
    
    apiKey.deleting = true
    await deleteApiKey(apiKey.id)
    
    // 重新加载 API Key 列表
    await loadApiKeys()
    
    ElMessage.success('API Key 删除成功')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除 API Key 失败:', error)
      ElMessage.error('删除 API Key 失败: ' + error.message)
    }
  } finally {
    apiKey.deleting = false
  }
}

// 切换 API Key 状态
const toggleApiKeyStatus = async (apiKey) => {
  try {
    apiKey.operating = true
    
    if (apiKey.is_active) {
      await deactivateApiKey(apiKey.id)
      ElMessage.success('API Key 已停用')
    } else {
      await activateApiKey(apiKey.id)
      ElMessage.success('API Key 已启用')
    }
    
    // 重新加载 API Key 列表
    await loadApiKeys()
  } catch (error) {
    console.error('操作 API Key 失败:', error)
    ElMessage.error('操作 API Key 失败: ' + error.message)
  } finally {
    apiKey.operating = false
  }
}

// 组件挂载时加载 API Key 列表
onMounted(() => {
  loadApiKeys()
})
</script>

<style lang="scss" scoped>
.api-key-management-page {
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
    max-width: 1000px;
    margin: 0 auto;
    
    .card {
      background: #fff;
      border-radius: 12px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
      padding: 40px;
      
      .header-section {
        text-align: center;
        margin-bottom: 32px;
        
        .title {
          font-size: 28px;
          font-weight: 700;
          color: #1a1a1a;
          margin-bottom: 16px;
        }
        
        .description {
          font-size: 16px;
          color: #666;
          margin: 0;
        }
      }
      
      .create-card {
        margin-bottom: 32px;
        
        :deep(.el-card__header) {
          padding: 16px 20px;
          border-bottom: 1px solid #eee;
        }
        
        .card-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          font-weight: 600;
          color: #1a1a1a;
        }
        
        .create-form {
          :deep(.el-form-item__label) {
            font-weight: 500;
            color: #1a1a1a;
          }
          
          .create-btn {
            width: 100%;
            margin-top: 24px;
          }
        }
      }
      
      .list-card {
        :deep(.el-card__header) {
          padding: 16px 20px;
          border-bottom: 1px solid #eee;
        }
        
        .card-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          font-weight: 600;
          color: #1a1a1a;
        }
        
        .api-key-table {
          :deep(.el-table__cell) {
            padding: 8px 0;
          }
          
          .action-buttons {
            display: flex;
            gap: 8px;
          }
        }
      }
    }
  }
}

// 自定义对话框样式
:global(.api-key-dialog) {
  .el-message-box__message {
    word-break: break-all;
    font-family: monospace;
    background: #f5f5f5;
    padding: 12px;
    border-radius: 4px;
    margin: 16px 0;
  }
}
</style>