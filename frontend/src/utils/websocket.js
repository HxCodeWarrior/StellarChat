export class WebSocketClient {
  constructor() {
    this.ws = null
    this.sessionId = null
    this.isConnected = false
    this.messageHandlers = new Map()
    this.eventHandlers = new Map()
  }

  // 连接到WebSocket服务器
  connect(sessionId = null) {
    // 构建WebSocket URL
    let wsUrl = 'ws://localhost:8080/api/ws/chat'
    if (sessionId) {
      wsUrl += `?session_id=${sessionId}`
    }

    // 创建WebSocket连接
    this.ws = new WebSocket(wsUrl)

    // 设置事件处理程序
    this.ws.onopen = () => {
      this.isConnected = true
      console.log('WebSocket连接已建立')
      this.handleEvent('open')
    }

    this.ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        this.handleMessage(data)
      } catch (error) {
        console.error('解析WebSocket消息失败:', error)
      }
    }

    this.ws.onclose = () => {
      this.isConnected = false
      console.log('WebSocket连接已关闭')
      this.handleEvent('close')
    }

    this.ws.onerror = (error) => {
      console.error('WebSocket错误:', error)
      this.handleEvent('error', error)
    }
  }

  // 发送消息
  sendMessage(content) {
    if (!this.isConnected) {
      console.warn('WebSocket未连接')
      return
    }

    const message = {
      type: 'chat.message',
      content: content
    }

    this.ws.send(JSON.stringify(message))
  }

  // 处理接收到的消息
  handleMessage(data) {
    const event = data.event || 'message'
    
    if (this.messageHandlers.has(event)) {
      this.messageHandlers.get(event)(data)
    } else {
      console.log('未处理的WebSocket消息:', data)
    }
    
    // 特别处理会话开始事件，保存会话ID
    if (event === 'session_start') {
      this.sessionId = data.data?.session_id
      console.log('会话ID:', this.sessionId)
    }
  }

  // 注册消息处理器
  on(event, handler) {
    this.messageHandlers.set(event, handler)
  }

  // 注册连接事件处理器
  onEvent(event, handler) {
    if (!this.eventHandlers.has(event)) {
      this.eventHandlers.set(event, [])
    }
    this.eventHandlers.get(event).push(handler)
  }

  // 处理连接事件
  handleEvent(event, data) {
    if (this.eventHandlers.has(event)) {
      this.eventHandlers.get(event).forEach(handler => handler(data))
    }
  }

  // 关闭连接
  close() {
    if (this.ws) {
      this.ws.close()
    }
  }

  // 获取会话ID
  getSessionId() {
    return this.sessionId
  }
}