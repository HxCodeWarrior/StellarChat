<script setup>
import { ref, watch, computed, onMounted } from 'vue'
import { useSettingStore, defaultModelOptions } from '@/stores/setting'
import { fetchModelList } from '@/utils/models'
import { QuestionFilled } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

const settingStore = useSettingStore()
const router = useRouter()

// 控制抽屉显示
const visible = ref(false)

// 模型选项
const modelOptions = ref(defaultModelOptions)



// 计算当前选中模型的最大 tokens
const currentMaxTokens = computed(() => {
  const selectedModel = modelOptions.value.find((option) => option.value === settingStore.settings.model)
  return selectedModel ? selectedModel.maxTokens : 4096
})

// 监听模型变化
watch(
  () => settingStore.settings.model,
  (newModel) => {
    const selectedModel = modelOptions.value.find((option) => option.value === newModel)
    if (selectedModel) {
      // 更新 maxTokens，并确保不超过模型的最大值
      settingStore.settings.maxTokens = Math.min(
        settingStore.settings.maxTokens,
        selectedModel.maxTokens,
      )
    }
  },
)

// 获取模型列表
const loadModelList = async () => {
  try {
    // 只有当用户设置了API Key时才从后端获取模型列表
    if (settingStore.settings.apiKey) {
      const models = await fetchModelList()
      modelOptions.value = models
    }
  } catch (error) {
    console.error('获取模型列表失败，使用默认模型列表:', error)
    modelOptions.value = defaultModelOptions
  }
}

// 打开抽屉
const openDrawer = () => {
  visible.value = true
  // 每次打开抽屉时重新加载模型列表
  loadModelList()
}

// 打开API Key管理对话框
const openApiKeyManagement = () => {
  // 跳转到API Key管理页面
  router.push('/api-key-management')
}

// 生成新的API Key
const generateApiKey = async () => {
  // 跳转到获取API Key页面
  router.push('/get-api-key')
}

// 组件挂载时加载模型列表
onMounted(() => {
  loadModelList()
})

// 导出方法供父组件调用
defineExpose({
  openDrawer,
})
</script>

<template>
  <el-drawer v-model="visible" title="设置" direction="rtl" size="350px">
    <div class="setting-container">
      <!-- 模型选择 -->
      <div class="setting-item">
        <div class="setting-label">Model</div>
        <el-select
          v-model="settingStore.settings.model"
          class="model-select"
          placeholder="选择模型"
        >
          <el-option
            v-for="option in modelOptions"
            :key="option.value"
            :label="option.label"
            :value="option.value"
          />
        </el-select>
        <div class="model-refresh">
          <el-button size="small" @click="loadModelList">刷新模型列表</el-button>
        </div>
      </div>

      <!-- 流式响应开关 -->
      <div class="setting-item">
        <div class="setting-label-row">
          <div class="label-with-tooltip">
            <span>流式响应</span>
            <el-tooltip content="开启后将流式响应 AI 的回复" placement="top">
              <el-icon><QuestionFilled /></el-icon>
            </el-tooltip>
          </div>
          <el-switch v-model="settingStore.settings.stream" />
        </div>
      </div>

      <!-- API Key -->
      <div class="setting-item">
        <div class="setting-label-row">
          <div class="label-with-tooltip">
            <span>API Key</span>
            <el-tooltip content="设置 API KEY" placement="top">
              <el-icon><QuestionFilled /></el-icon>
            </el-tooltip>
          </div>
          <div class="api-key-management">
            <el-button size="small" @click="openApiKeyManagement">管理 API KEY</el-button>
          </div>
        </div>
        <el-input
          v-model="settingStore.settings.apiKey"
          type="password"
          placeholder="请输入 API Key"
          show-password
        />
        <div class="api-key-hint">
          <el-button type="primary" size="small" @click="generateApiKey">获取 API KEY</el-button>
        </div>
      </div>

      <!-- Max Tokens -->
      <div class="setting-item">
        <div class="setting-label">
          Max Tokens
          <el-tooltip content="生成文本的最大长度" placement="top">
            <el-icon><QuestionFilled /></el-icon>
          </el-tooltip>
        </div>
        <div class="setting-control">
          <el-slider
            v-model="settingStore.settings.maxTokens"
            :min="1"
            :max="currentMaxTokens"
            :step="1"
            :show-tooltip="false"
            class="setting-slider"
          />
          <el-input-number
            v-model="settingStore.settings.maxTokens"
            :min="1"
            :max="currentMaxTokens"
            :step="1"
            controls-position="right"
          />
        </div>
      </div>

      <!-- Temperature -->
      <div class="setting-item">
        <div class="setting-label">
          Temperature
          <el-tooltip content="值越高，回答越随机" placement="top">
            <el-icon><QuestionFilled /></el-icon>
          </el-tooltip>
        </div>
        <div class="setting-control">
          <el-slider
            v-model="settingStore.settings.temperature"
            :min="0"
            :max="2"
            :step="0.1"
            :show-tooltip="false"
            class="setting-slider"
          />
          <el-input-number
            v-model="settingStore.settings.temperature"
            :min="0"
            :max="2"
            :step="0.1"
            controls-position="right"
          />
        </div>
      </div>

      <!-- Top-P -->
      <div class="setting-item">
        <div class="setting-label">
          Top-P
          <el-tooltip content="核采样阈值" placement="top">
            <el-icon><QuestionFilled /></el-icon>
          </el-tooltip>
        </div>
        <div class="setting-control">
          <el-slider
            v-model="settingStore.settings.topP"
            :min="0"
            :max="1"
            :step="0.1"
            :show-tooltip="false"
            class="setting-slider"
          />
          <el-input-number
            v-model="settingStore.settings.topP"
            :min="0"
            :max="1"
            :step="0.1"
            controls-position="right"
          />
        </div>
      </div>

      <!-- Top-K -->
      <div class="setting-item">
        <div class="setting-label">
          Top-K
          <el-tooltip content="保留概率最高的 K 个词" placement="top">
            <el-icon><QuestionFilled /></el-icon>
          </el-tooltip>
        </div>
        <div class="setting-control">
          <el-slider
            v-model="settingStore.settings.topK"
            :min="1"
            :max="100"
            :step="1"
            :show-tooltip="false"
            class="setting-slider"
          />
          <el-input-number
            v-model="settingStore.settings.topK"
            :min="1"
            :max="100"
            :step="1"
            controls-position="right"
          />
        </div>
      </div>
    </div>
  </el-drawer>
</template>

<style lang="scss" scoped>
.setting-container {
  padding: 20px;
  color: #27272a;
}

.setting-item {
  margin-bottom: 24px;

  // 基础标签样式
  .setting-label {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
    font-weight: 500;
    color: #27272a;
  }

  // 水平布局的标签行，用于标签和控件在同一行的情况
  .setting-label-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
    color: #27272a;

    // 标签和提示图标的容器
    .label-with-tooltip {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    // 获取 API Key 链接样式
    .get-key-link {
      font-size: 14px;
      color: #3f7af1;
      text-decoration: none;
    }
  }

  // 控件容器样式，用于包含滑块和数字输入框
  .setting-control {
    display: flex;
    align-items: center;
    gap: 16px;

    // 滑块占据剩余空间
    .setting-slider {
      flex: 1;
    }

    // 数字输入框固定宽度
    :deep(.el-input-number) {
      width: 120px;
    }
  }

  // 模型选择下拉框宽度
  .model-select {
    width: 100%;
  }

  // 模型刷新按钮样式
  .model-refresh {
    margin-top: 8px;
    display: flex;
    justify-content: flex-end;
  }

  // 下拉选项文字颜色
  :deep(.el-select-dropdown__item) {
    color: #27272a;
  }
  
  // API Key提示链接样式
  .api-key-hint {
    margin-top: 8px;
    
    .get-key-link {
      font-size: 14px;
      color: #3f7af1;
      text-decoration: none;
    }
  }
}
</style>


