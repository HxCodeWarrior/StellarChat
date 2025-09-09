import { useSettingStore } from '@/stores/setting'

// 如果使用提供的模型列表，那么这里的API_BASE_URL就要设置为https://openrouter.ai/api/v1
// 如果使用本地的模型，那么这里的API_BASE_URL就要设置为http://localhost:8080/api
const API_BASE_URL = 'http://localhost:8080/api'

export const createChatCompletion = async (messages, sessionId = null) => {
  const settingStore = useSettingStore()
  const payload = {
    model: settingStore.settings.model,
    messages,
    stream: settingStore.settings.stream,
    max_tokens: settingStore.settings.maxTokens,
    temperature: settingStore.settings.temperature,
    top_p: settingStore.settings.topP,
    top_k: settingStore.settings.topK,
  }

  // 构建查询参数
  let url = `${API_BASE_URL}/chat/completions`
  if (sessionId) {
    url += `?session_id=${sessionId}`
  }

  const options = {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${settingStore.settings.apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  }

  try {
    const startTime = Date.now() // 记录开始时间
    const response = await fetch(url, options)

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    if (settingStore.settings.stream) {
      return response // 直接返回响应对象以支持流式读取
    } else {
      const data = await response.json()
      const duration = (Date.now() - startTime) / 1000 // 使用本地计时
      // 后端返回的usage字段可能不同，需要适配
      const completionTokens = data.usage?.completion_tokens || 0
      data.speed = (completionTokens / duration).toFixed(2)
      return data
    }
  } catch (error) {
    console.error('Chat API Error:', error)
    throw error
  }
}
