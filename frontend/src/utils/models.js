import { useSettingStore } from '@/stores/setting'

// 如果使用提供的模型列表，那么这里的API_BASE_URL就要设置为https://openrouter.ai/api/v1
// 如果使用本地的模型，那么这里的API_BASE_URL就要设置为http://localhost:8080/api
const API_BASE_URL = 'http://localhost:8080/api'

export const fetchModelList = async () => {
  const settingStore = useSettingStore()
  
  try {
    const response = await fetch(`${API_BASE_URL}/models`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${settingStore.settings.apiKey}`,
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    return data.data.map(model => ({
      label: model.id,
      value: model.id,
      maxTokens: 4096 // 默认值，可以根据需要调整
    }))
  } catch (error) {
    console.error('获取模型列表失败:', error)
    throw error
  }
}