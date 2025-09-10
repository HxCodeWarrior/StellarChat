// 如果使用提供的模型列表，那么这里的API_BASE_URL就要设置为https://openrouter.ai/api/v1
// 如果使用本地的模型，那么这里的API_BASE_URL就要设置为http://localhost:8080/api
const API_BASE_URL = 'http://localhost:8080/api'

export const createApiKey = async (name) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api-keys`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name }),
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    return data
  } catch (error) {
    console.error('创建API Key失败:', error)
    throw error
  }
}

export const getApiKeys = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api-keys`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    return data.data
  } catch (error) {
    console.error('获取API Key列表失败:', error)
    throw error
  }
}

export const deleteApiKey = async (keyId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api-keys/${keyId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    return data
  } catch (error) {
    console.error('删除API Key失败:', error)
    throw error
  }
}

export const deactivateApiKey = async (keyId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api-keys/${keyId}/deactivate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    return data
  } catch (error) {
    console.error('停用API Key失败:', error)
    throw error
  }
}

export const activateApiKey = async (keyId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api-keys/${keyId}/activate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    return data
  } catch (error) {
    console.error('启用API Key失败:', error)
    throw error
  }
}