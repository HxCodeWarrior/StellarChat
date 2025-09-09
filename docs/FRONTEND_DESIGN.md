# StellarChat 聊天界面前端开发方案

## 项目概述

StellarChat 是一款仿 DeepSeek 风格的现代化聊天应用前端界面，专注于提供流畅的AI对话体验。本方案采用 Vue 3 + JavaScript 技术栈，结合响应式设计和可访问性考量，打造高性能、美观的用户界面。

## 技术栈详述

- **前端框架**: Vue 3 (Composition API)
- **语言**: JavaScript (ES6+)
- **构建工具**: Vite 6.0+
- **样式方案**: SCSS + 自定义CSS变量
- **UI组件库**: Element Plus
- **状态管理**: Pinia (支持持久化)
- **路由**: Vue Router v4
- **HTTP客户端**: Fetch API (原生)
- **Markdown渲染**: markdown-it + highlight.js
- **代码质量**: ESLint + Prettier + Husky (Git钩子)
- **动画库**: animate.css

## 项目结构优化

```
src/
├── assets/                    # 静态资源
│   ├── photo/                 # 图片资源
│   ├── sampels/               # 示例图片
│   └── styles/                # 全局样式
│       ├── main.scss
│       └── variables.scss
├── components/                # 可复用组件
│   ├── ChatInput.vue          # 聊天输入组件
│   ├── ChatMessage.vue        # 消息展示组件
│   ├── DialogEdit.vue         # 对话编辑组件
│   ├── PopupMenu.vue          # 弹出菜单组件
│   ├── SearchDialog.vue       # 搜索对话框组件
│   └── SettingsPanel.vue      # 设置面板组件
├── router/                    # 路由配置
│   └── index.js
├── stores/                    # 状态管理(Pinia)
│   ├── chat.js                # 聊天状态管理
│   └── setting.js             # 设置状态管理
├── utils/                     # 工具函数
│   ├── api.js                 # API接口封装
│   ├── markdown.js            # Markdown渲染工具
│   └── messageHandler.js      # 消息处理工具
├── views/                     # 页面视图
│   ├── ChatView.vue           # 聊天主页面
│   └── HomePage.vue           # 首页
├── App.vue                    # 根组件
└── main.js                    # 入口文件
```

## 组件设计与开发详述

### 1. 页面组件 (Views)

**ChatView.vue**
- 聊天主页面，包含整个聊天界面
- 管理消息列表展示和滚动
- 处理消息发送和重新生成逻辑
- 集成聊天输入组件和消息展示组件
- 管理对话创建和切换
- 集成设置面板和弹出菜单

**HomePage.vue**
- 应用首页，提供进入聊天界面的入口
- 展示应用介绍和功能说明
- 提供快速开始聊天的按钮

### 2. 聊天组件 (Chat)

**ChatMessage.vue**
- 单条消息展示组件
- 区分用户消息和AI消息样式
- 支持消息操作(复制、重新生成、点赞、点踩)
- Markdown内容渲染与代码语法高亮
- 显示消息状态(发送中、发送成功、发送失败)
- 支持文件预览展示
- 显示tokens信息和生成速度
- 支持深度思考内容展示和折叠

**ChatInput.vue**
- 消息输入区域
- 支持多行文本输入和自动调整高度
- 支持文件拖拽上传
- 支持图片预览
- 实现发送按钮和加载状态
- 支持键盘快捷键(Enter发送，Shift+Enter换行)
- 文件上传限制和验证

### 3. UI组件系统

**SettingsPanel.vue**
- 侧边抽屉形式的设置面板
- 包含模型选择、参数设置等功能
- 支持主题切换(明亮/暗黑模式)
- 支持流式输出开关
- 设置项持久化存储

**DialogEdit.vue**
- 对话框编辑组件
- 支持对话标题的编辑和删除
- 支持新建对话功能

**PopupMenu.vue**
- 弹出菜单组件
- 显示对话列表
- 支持对话切换、删除操作
- 支持新建对话

**SearchDialog.vue**
- 搜索对话框组件
- 支持对话历史搜索
- 快速跳转到指定对话

## 样式与设计系统详述

### 颜色方案

**主色调 (Primary)**
- 蓝色: `#3f7af1` (主要操作)
- 深蓝: `#2563EB` (悬停状态)

**中性色 (Neutral)**
- 白色: `#FFFFFF` (背景)
- 浅灰: `#F3F4F6` (次要背景)
- 中灰: `#E5E7EB` (边框/分隔线)
- 深灰: `#909399` (次要文本)
- 黑灰: `#000000` (主要文本)

**功能色 (Functional)**
- 成功: `#10B981` (绿色)
- 警告: `#F59E0B` (琥珀色)
- 错误: `#EF4444` (红色)
- 信息: `#3B82F6` (蓝色)

**明暗主题**
- 支持明亮主题
- 暗色主题正在开发中

### CSS变量系统

```scss
:root {
  // 基础颜色
  --text-color: #000000;
  --text-color-secondary: #bbbfc4;
  --bg-color: #ffffff;
  --border-color: #c5c5c5;

  // 代码相关的颜色和字体
  --code-font-family: 'Fira Code', 'Consolas', 'Monaco', 'Courier New', monospace;
  --code-lang-text: #000000;
  --code-block-bg: #fcfcfc;
  --code-header-bg: #f3f4f6;
  --code-border: #ebebeb;
  --code-text: #383a42; /* 添加默认代码文本颜色 - 接近黑色 */
  --code-header-button-hover-bg: #e5e6e8;
}
```

### 响应式设计

- 使用弹性布局和视口单位实现响应式
- 最大宽度限制: 796px
- 支持移动端和桌面端显示
- 自适应高度和滚动区域

## 功能开发详述

### 核心功能模块

**1. 消息系统**
- 实时消息发送与接收
- 消息状态管理(发送中、成功、失败)
- 消息重新生成
- 消息复制
- 消息点赞/点踩反馈

**2. 会话管理**
- 创建新会话
- 会话重命名
- 会话删除
- 会话切换
- 会话持久化存储

**3. 文件处理**
- 支持拖拽上传图片文件
- 图片预览功能
- 文件类型和大小限制

**4. 用户偏好设置**
- 模型选择
- 参数设置(temperature, max_tokens等)
- 主题选择(明亮/暗黑)
- 流式输出开关

### 高级功能

**1. Markdown渲染**
- 支持代码块语法高亮
- 支持代码块主题切换(明亮/暗黑)
- 支持代码块复制
- 支持表格、列表、引用等Markdown语法

**2. 深度思考展示**
- 显示模型的推理过程
- 支持折叠/展开推理内容

**3. Tokens信息显示**
- 显示生成的tokens数量
- 显示生成速度(tokens/s)

**4. 快捷键系统**
- Enter发送消息
- Shift+Enter换行
- Ctrl+Enter发送消息

## API接口设计

### API封装

```javascript
// utils/api.js - API接口封装

// 创建聊天完成请求
export async function createChatCompletion(messages) {
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
  
  const response = await fetch(`${API_BASE_URL}/v1/chat/completions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      messages: messages,
      stream: true,  // 默认使用流式输出
    }),
  })
  
  if (!response.ok) {
    throw new Error(`API request failed with status ${response.status}`)
  }
  
  return response
}
```

### 消息处理

```javascript
// utils/messageHandler.js - 消息处理工具

export const messageHandler = {
  // 格式化消息
  formatMessage(role, content, reasoning_content = '', files = []) {
    return {
      role,
      content,
      reasoning_content,
      files,
      timestamp: new Date().toISOString(),
    }
  },
  
  // 处理流式响应
  async handleResponse(response, isStream, onProgress) {
    if (isStream) {
      // 处理流式响应
      await this.handleStreamResponse(response, onProgress)
    } else {
      // 处理非流式响应
      await this.handleNormalResponse(response, onProgress)
    }
  },
  
  // 处理流式响应
  async handleStreamResponse(response, onProgress) {
    const reader = response.body.getReader()
    const decoder = new TextDecoder('utf-8')
    let buffer = ''
    let content = ''
    let reasoning_content = ''
    let tokens = 0
    let startTime = Date.now()
    
    try {
      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        
        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split(/\r?\n/)
        buffer = lines.pop() || ''
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6)
            if (data === '[DONE]') break
            
            try {
              const parsed = JSON.parse(data)
              if (parsed.content) {
                content += parsed.content
                tokens += 1
              }
              if (parsed.reasoning_content) {
                reasoning_content = parsed.reasoning_content
              }
              
              const speed = tokens / ((Date.now() - startTime) / 1000)
              onProgress(content, reasoning_content, tokens, speed.toFixed(1))
            } catch (e) {
              console.warn('Failed to parse stream data:', e)
            }
          }
        }
      }
    } finally {
      reader.releaseLock()
    }
  },
  
  // 处理非流式响应
  async handleNormalResponse(response, onProgress) {
    const data = await response.json()
    const content = data.choices[0].message.content
    const tokens = data.usage?.completion_tokens || 0
    const speed = 0
    
    onProgress(content, '', tokens, speed)
  }
}
```

## 状态管理详细设计

### Pinia 状态管理

StellarChat 使用 Pinia 作为状态管理方案，具有轻量、易用、支持 Vue DevTools 调试等优点，并通过 pinia-plugin-persistedstate 插件实现状态持久化。

#### 聊天状态管理 (chat.js)

```javascript
// stores/chat.js
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useChatStore = defineStore('llm-chat', () => {
  // 所有对话列表
  const conversations = ref([
    {
      id: '1',
      title: '日常问候',
      messages: [],
      createdAt: Date.now(),
    },
  ])

  // 当前选中的对话 ID
  const currentConversationId = ref('1')

  // 加载状态
  const isLoading = ref(false)

  // 获取当前对话
  const currentConversation = computed(() => {
    return conversations.value.find((conv) => conv.id === currentConversationId.value)
  })

  // 获取当前对话的消息
  const currentMessages = computed(() => currentConversation.value?.messages || [])

  // 状态操作方法
  const createConversation = () => { /* ... */ }
  const switchConversation = (conversationId) => { /* ... */ }
  const addMessage = (message) => { /* ... */ }
  const setIsLoading = (value) => { /* ... */ }
  const updateLastMessage = (content, reasoning_content, completion_tokens, speed) => { /* ... */ }
  const getLastMessage = () => { /* ... */ }
  const updateConversationTitle = (conversationId, newTitle) => { /* ... */ }
  const deleteConversation = (conversationId) => { /* ... */ }

  return {
    conversations,
    currentConversationId,
    currentConversation,
    currentMessages,
    isLoading,
    addMessage,
    setIsLoading,
    updateLastMessage,
    getLastMessage,
    createConversation,
    switchConversation,
    updateConversationTitle,
    deleteConversation,
  }
}, {
  persist: true, // 启用状态持久化
})
```

#### 设置状态管理 (setting.js)

```javascript
// stores/setting.js
import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useSettingStore = defineStore('setting', () => {
  // 设置状态
  const settings = ref({
    model: 'glm-4-plus',
    temperature: 0.5,
    max_tokens: 1024,
    stream: true,
    theme: 'light',
  })

  // 更新设置
  const updateSetting = (key, value) => {
    settings.value[key] = value
  }

  // 重置设置
  const resetSettings = () => {
    settings.value = {
      model: 'glm-4-plus',
      temperature: 0.5,
      max_tokens: 1024,
      stream: true,
      theme: 'light',
    }
  }

  return {
    settings,
    updateSetting,
    resetSettings,
  }
}, {
  persist: true, // 启用状态持久化
})
```

## 性能优化策略

### 1. 组件级别优化
- 使用 Vue 3 Composition API 实现精细化响应式更新
- 合理使用 computed 计算属性缓存派生数据
- 使用 watch 监听器精确控制副作用
- 组件懒加载

### 2. 资源加载优化
- 代码分割和动态导入
- 图片懒加载
- SCSS 模块化和样式优化
- 静态资源压缩

### 3. 渲染优化
- 虚拟滚动(对于大量消息的场景)
- 合理使用 v-show 和 v-if 控制元素显示
- 避免不必要的 DOM 操作
- 使用 keep-alive 缓存页面组件

## 测试策略

### 单元测试
- 组件渲染测试
- 工具函数测试
- 状态管理测试

### 集成测试
- 用户交互流程测试
- API集成测试

### E2E测试
- 关键用户旅程测试
- 跨浏览器兼容性测试

## 部署与维护

### 构建配置
- 多环境配置(development, production)
- 环境变量管理
- 打包优化

### 监控
- 浏览器控制台错误监控
- 性能监控

## 开发阶段详细规划

### 第一阶段：基础框架搭建
1. 项目初始化与开发环境配置
2. 基础组件系统搭建
3. 样式系统实现
4. 路由配置
5. 状态管理基础架构

### 第二阶段：核心功能开发
1. 聊天界面主组件开发
2. 消息列表和消息项组件
3. 输入区域实现
4. 会话管理功能
5. 本地数据持久化

### 第三阶段：API集成与高级功能
1. REST API客户端实现
2. 流式消息处理
3. 文件上传和预览功能
4. Markdown渲染和代码高亮
5. 深度思考内容展示

### 第四阶段：优化与测试
1. 性能优化实施
2. 响应式设计和移动端适配
3. 测试覆盖(单元、集成)
4. 代码审查和重构

### 第五阶段：部署与迭代
1. 部署配置
2. 监控集成
3. 用户反馈收集机制
4. 迭代计划制定