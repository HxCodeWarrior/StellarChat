<template>
  <el-dialog v-model="visible" title="API KEY管理" width="600px" @close="handleClose">
    <div class="api-key-management">
      <!-- 创建API KEY表单 -->
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px" class="create-form">
        <el-form-item label="API KEY名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入API KEY名称" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleCreateApiKey" :loading="creating">创建API KEY</el-button>
        </el-form-item>
      </el-form>

      <!-- API Key列表 -->
      <div class="api-key-list">
        <h3>API Key列表</h3>
        <el-table :data="apiKeys" style="width: 100%" v-loading="loading">
          <el-table-column prop="name" label="名称" />
          <el-table-column prop="created_at" label="创建时间">
            <template #default="scope">
              {{ formatDate(scope.row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="状态">
            <template #default="scope">
              <el-tag :type="scope.row.is_active ? 'success' : 'danger'">
                {{ scope.row.is_active ? '启用' : '停用' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200">
            <template #default="scope">
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
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import {
  createApiKey,
  getApiKeys,
  deleteApiKey,
  deactivateApiKey,
  activateApiKey
} from '@/utils/apiKeys'
import { ElMessage, ElMessageBox } from 'element-plus'

const visible = defineModel('visible', { type: Boolean, default: false })

// 表单数据
const form = reactive({
  name: ''
})

// 表单验证规则
const rules = {
  name: [
    { required: true, message: '请输入API KEY名称', trigger: 'blur' }
  ]
}

// API KEY列表
const apiKeys = ref([])

// 状态
const loading = ref(false)
const creating = ref(false)
const formRef = ref(null)

// 格式化日期
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

// 获取API Key列表
const loadApiKeys = async () => {
  loading.value = true
  try {
    const data = await getApiKeys()
    // 为每个API KEY添加操作状态字段
    apiKeys.value = data.map(key => ({
      ...key,
      operating: false,
      deleting: false
    }))
  } catch (error) {
    console.error('获取API KEY列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 创建API KEY
const handleCreateApiKey = async () => {
  try {
    await formRef.value.validate()
    creating.value = true
    
    await createApiKey(form.name)
    
    // 重新加载API KEY列表
    await loadApiKeys()
    
    // 重置表单
    form.name = ''
    
    // 显示成功消息
    ElMessage.success('API KEY创建成功')
  } catch (error) {
    console.error('创建API KEY失败:', error)
    ElMessage.error('创建API KEY失败: ' + error.message)
  } finally {
    creating.value = false
  }
}

// 删除API Key
const handleDeleteApiKey = async (apiKey) => {
  try {
    await ElMessageBox.confirm('确定要删除这个API KEY吗？此操作不可恢复。', '确认删除', {
      type: 'warning'
    })
    
    apiKey.deleting = true
    await deleteApiKey(apiKey.id)
    
    // 重新加载API KEY列表
    await loadApiKeys()
    
    ElMessage.success('API KEY删除成功')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除API KEY失败:', error)
      ElMessage.error('删除API KEY失败: ' + error.message)
    }
  } finally {
    apiKey.deleting = false
  }
}

// 切换API KEY状态
const toggleApiKeyStatus = async (apiKey) => {
  try {
    apiKey.operating = true
    
    if (apiKey.is_active) {
      await deactivateApiKey(apiKey.id)
      ElMessage.success('API KEY已停用')
    } else {
      await activateApiKey(apiKey.id)
      ElMessage.success('API KEY已启用')
    }
    
    // 重新加载API KEY列表
    await loadApiKeys()
  } catch (error) {
    console.error('操作API KEY失败:', error)
    ElMessage.error('操作API KEY失败: ' + error.message)
  } finally {
    apiKey.operating = false
  }
}

// 关闭对话框
const handleClose = () => {
  visible.value = false
}

// 组件挂载时加载API Key列表
onMounted(() => {
  loadApiKeys()
})

// 暴露方法给父组件
defineExpose({
  loadApiKeys
})
</script>

<style lang="scss" scoped>
.api-key-management {
  .create-form {
    margin-bottom: 30px;
    padding-bottom: 20px;
    border-bottom: 1px solid #eee;
  }
  
  .api-key-list {
    h3 {
      margin-top: 0;
      margin-bottom: 15px;
    }
  }
}
</style>