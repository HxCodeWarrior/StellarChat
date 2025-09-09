# StellarChat聊天界面前端开发方案

## 项目概述
开发一个类似DeepSeek网页版聊天界面的React应用，包含现代化的聊天界面、消息交互功能和流畅的用户体验。

## 技术栈
- **前端框架**: React 18 + TypeScript
- **构建工具**: Vite
- **样式方案**: Tailwind CSS
- **状态管理**: React Hooks (useState, useReducer)
- **HTTP客户端**: Axios
- **代码质量**: ESLint + Prettier

## 项目结构
```
src/
├── components/
│   ├── layout/
│   │   ├── Header.tsx
│   │   ├── Sidebar.tsx
│   │   └── Layout.tsx
│   ├── chat/
│   │   ├── MessageList.tsx
│   │   ├── MessageItem.tsx
│   │   ├── InputArea.tsx
│   │   └── TypingIndicator.tsx
│   └── ui/
│       ├── Button.tsx
│       ├── IconButton.tsx
│       ├── Modal.tsx
│       └── Loader.tsx
├── hooks/
│   ├── useChat.ts
│   └── useLocalStorage.ts
├── types/
│   └── index.ts
├── utils/
│   ├── api.ts
│   └── helpers.ts
├── styles/
│   └── index.css
│   └── App.css
│   └── components/
│   └── global/
│   └── themes/
│   └── utilities/
├── App.tsx
└── main.tsx
```

## 组件设计与开发

### 1. 布局组件 (Layout)
**Layout.tsx**
- 提供整体应用布局结构
- 管理侧边栏和主内容区的切换状态

**Header.tsx**
- 显示应用标题和品牌标识
- 包含主题切换按钮和新聊天按钮

**Sidebar.tsx**
- 显示聊天历史列表
- 提供新建聊天、删除聊天等功能
- 折叠/展开状态管理

### 2. 聊天组件 (Chat)
**MessageList.tsx**
- 渲染所有消息的容器
- 自动滚动至最新消息
- 虚拟滚动支持(针对大量消息)

**MessageItem.tsx**
- 单条消息展示组件
- 区分用户消息和AI消息的不同样式
- 支持消息操作(复制、重新生成等)
- Markdown格式渲染支持

**InputArea.tsx**
- 消息输入区域
- 支持多行文本输入
- 包含发送按钮和附件功能(可选)
- 输入内容验证与处理

**TypingIndicator.tsx**
- AI正在输入状态的视觉指示器
- 动画效果增强用户体验

### 3. UI组件 (UI)
**Button.tsx**
- 可定制的按钮组件
- 支持多种样式和状态

**IconButton.tsx**
- 图标按钮组件
- 工具提示功能

**Modal.tsx**
- 模态对话框组件
- 支持自定义内容

**Loader.tsx**
- 加载指示器组件
- 多种尺寸和样式

## 样式与颜色搭配

### 颜色方案
- **主色调**: DeepSeek蓝色系 (#2563EB, #1D4ED8)
- **背景色**: 浅灰(#F9FAFB)和深灰(#1F2937)双主题支持
- **消息气泡**:
  - 用户消息: 蓝色系(#2563EB)，文字白色
  - AI消息: 浅灰色(#F3F4F6)，文字深灰(#1F2937)
- **辅助色**: 绿色(#10B981)表示成功，红色(#EF4444)表示错误

### 设计原则
- 极简主义设计，减少视觉噪音
- 充足的留白和呼吸空间
- 一致的圆角设计(8px)
- 平滑的过渡动画和微交互

## 功能开发

### 核心功能
1. **消息发送与接收**
   - 实时消息渲染
   - 消息状态管理(发送中、成功、失败)
   - 自动调整文本区域高度

2. **聊天管理**
   - 创建新聊天会话
   - 保存和加载聊天历史
   - 删除聊天会话

3. **消息交互**
   - 复制消息内容
   - 重新生成AI回复
   - 编辑和重新发送消息

4. **用户体验增强**
   - 响应式设计(移动端/桌面端)
   - 键盘快捷键(Ctrl+Enter发送)
   - 消息流式接收效果
   - 主题切换(明暗模式)

### 状态管理方案
使用React Context + useReducer管理全局状态:
- 聊天会话列表
- 当前聊天消息
- 应用设置(主题、偏好)
- API连接状态

## API接口预留

### 聊天API

#### REST API接口
```typescript
// 聊天完成请求
interface ChatCompletionRequest {
  model: string;
  messages: ChatMessage[];
  temperature?: number;
  top_p?: number;
  max_tokens?: number;
  stream?: boolean;
  stop?: string | string[];
  user?: string;
}

// 聊天消息
interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string | Array<{
    type: string;
    text?: string;
  }>;
}

// 聊天完成响应
interface ChatCompletionResponse {
  id: string;
  object: string;
  created: number;
  model: string;
  choices: {
    index: number;
    message: ChatMessage;
    finish_reason: string;
  }[];
  usage: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
}

// 流式响应块
interface ChatCompletionChunk {
  id: string;
  object: string;
  created: number;
  model: string;
  choices: {
    index: number;
    delta: {
      role?: string;
      content?: string;
    };
    finish_reason: string | null;
  }[];
}

const createChatCompletion = async (
  request: ChatCompletionRequest,
  sessionId?: string
): Promise<ChatCompletionResponse> => {
  // API实现
};
```

#### WebSocket接口
```typescript
// WebSocket消息
interface WebSocketMessage {
  type: string;
  content: string;
}

// WebSocket事件
interface WebSocketEvent {
  event: string;
  data: any;
}

// 会话开始事件
interface SessionStartEvent extends WebSocketEvent {
  event: 'session_start';
  data: {
    session_id: string;
  };
}

// 内容块开始事件
interface ContentBlockStartEvent extends WebSocketEvent {
  event: 'content_block_start';
  data: {
    type: string;
    index: number;
  };
}

// 内容块增量事件
interface ContentBlockDeltaEvent extends WebSocketEvent {
  event: 'content_block_delta';
  data: {
    index: number;
    delta: {
      type: string;
      text: string;
    };
  };
}

// 内容块结束事件
interface ContentBlockStopEvent extends WebSocketEvent {
  event: 'content_block_stop';
  data: {
    index: number;
  };
}

// 消息增量事件
interface MessageDeltaEvent extends WebSocketEvent {
  event: 'message_delta';
  data: {
    delta: {
      finish_reason: string;
    };
    usage: {
      output_tokens: number;
    };
  };
}

// 消息结束事件
interface MessageStopEvent extends WebSocketEvent {
  event: 'message_stop';
  data: {};
}

// 错误事件
interface ErrorEvent extends WebSocketEvent {
  event: 'error';
  data: {
    type: string;
    message: string;
  };
}
```

### 会话管理API

```typescript
// 会话创建请求
interface SessionCreateRequest {
  title: string;
}

// 会话更新请求
interface SessionUpdateRequest {
  title: string;
}

// 会话响应
interface SessionResponse {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
}

// 消息创建请求
interface MessageCreateRequest {
  role: 'user' | 'assistant' | 'system';
  content: string;
  tokens?: number;
  metadata_info?: Record<string, any>;
}

// 消息响应
interface MessageResponse {
  id: string;
  session_id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  created_at: string;
  tokens: number;
  metadata_info: Record<string, any> | null;
}

const sessionAPI = {
  // 创建新会话
  createSession: (data: SessionCreateRequest): Promise<SessionResponse> => {
    // API实现
  },
  
  // 获取会话列表
  getSessions: (
    skip?: number,
    limit?: number,
    active_only?: boolean
  ): Promise<SessionResponse[]> => {
    // API实现
  },
  
  // 获取会话详情
  getSession: (id: string): Promise<SessionResponse> => {
    // API实现
  },
  
  // 更新会话
  updateSession: (id: string, data: SessionUpdateRequest): Promise<SessionResponse> => {
    // API实现
  },
  
  // 删除会话
  deleteSession: (id: string): Promise<void> => {
    // API实现
  },
  
  // 添加消息到会话
  addMessage: (sessionId: string, data: MessageCreateRequest): Promise<MessageResponse> => {
    // API实现
  },
  
  // 获取会话消息
  getMessages: (
    sessionId: string,
    skip?: number,
    limit?: number
  ): Promise<MessageResponse[]> => {
    // API实现
  },
  
  // 获取会话聊天历史（用于模型推理）
  getChatHistory: (sessionId: string): Promise<ChatMessage[]> => {
    // API实现
  }
};
```

### 模型管理API

```typescript
// 模型信息
interface ModelInfo {
  id: string;
  object: string;
  created: number;
  owned_by: string;
}

// 模型列表响应
interface ModelListResponse {
  object: string;
  data: ModelInfo[];
}

const modelAPI = {
  // 获取可用模型列表
  getModels: (): Promise<ModelListResponse> => {
    // API实现
  }
};
```

### 实现示例

在`services/chatService.ts`中创建API客户端:

```typescript
import { v4 as uuidv4 } from 'uuid';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

class ChatService {
  // 创建新会话
  async createSession(title: string): Promise<SessionResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/sessions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title }),
      });
      
      if (!response.ok) {
        throw new Error(`创建会话失败: ${response.statusText}`);
      }
      
      return response.json();
    } catch (error) {
      console.error('创建会话时发生错误:', error);
      throw error;
    }
  }

  // 获取会话列表
  async getSessions(skip: number = 0, limit: number = 100, active_only: boolean = true): Promise<SessionResponse[]> {
    try {
      const params = new URLSearchParams({
        skip: skip.toString(),
        limit: limit.toString(),
        active_only: active_only.toString()
      });
      
      const response = await fetch(`${API_BASE_URL}/api/sessions?${params}`);
      
      if (!response.ok) {
        throw new Error(`获取会话列表失败: ${response.statusText}`);
      }
      
      return response.json();
    } catch (error) {
      console.error('获取会话列表时发生错误:', error);
      throw error;
    }
  }

  // 获取会话详情
  async getSession(sessionId: string): Promise<SessionResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/sessions/${sessionId}`);
      
      if (!response.ok) {
        throw new Error(`获取会话详情失败: ${response.statusText}`);
      }
      
      return response.json();
    } catch (error) {
      console.error('获取会话详情时发生错误:', error);
      throw error;
    }
  }

  // 更新会话
  async updateSession(sessionId: string, title: string): Promise<SessionResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/sessions/${sessionId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title }),
      });
      
      if (!response.ok) {
        throw new Error(`更新会话失败: ${response.statusText}`);
      }
      
      return response.json();
    } catch (error) {
      console.error('更新会话时发生错误:', error);
      throw error;
    }
  }

  // 删除会话
  async deleteSession(sessionId: string): Promise<void> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/sessions/${sessionId}`, {
        method: 'DELETE',
      });
      
      if (!response.ok) {
        throw new Error(`删除会话失败: ${response.statusText}`);
      }
    } catch (error) {
      console.error('删除会话时发生错误:', error);
      throw error;
    }
  }

  // 添加消息到会话
  async addMessage(sessionId: string, message: MessageCreateRequest): Promise<MessageResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/sessions/${sessionId}/messages`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(message),
      });
      
      if (!response.ok) {
        throw new Error(`添加消息失败: ${response.statusText}`);
      }
      
      return response.json();
    } catch (error) {
      console.error('添加消息时发生错误:', error);
      throw error;
    }
  }

  // 获取会话消息
  async getMessages(sessionId: string, skip: number = 0, limit: number = 100): Promise<MessageResponse[]> {
    try {
      const params = new URLSearchParams({
        skip: skip.toString(),
        limit: limit.toString()
      });
      
      const response = await fetch(`${API_BASE_URL}/api/sessions/${sessionId}/messages?${params}`);
      
      if (!response.ok) {
        throw new Error(`获取消息失败: ${response.statusText}`);
      }
      
      return response.json();
    } catch (error) {
      console.error('获取消息时发生错误:', error);
      throw error;
    }
  }

  // 获取会话聊天历史（用于模型推理）
  async getChatHistory(sessionId: string): Promise<ChatMessage[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/sessions/${sessionId}/history`);
      
      if (!response.ok) {
        throw new Error(`获取聊天历史失败: ${response.statusText}`);
      }
      
      return response.json();
    } catch (error) {
      console.error('获取聊天历史时发生错误:', error);
      throw error;
    }
  }

  // 创建聊天完成 (REST API)
  async createChatCompletion(request: ChatCompletionRequest, sessionId?: string): Promise<ChatCompletionResponse> {
    try {
      const url = sessionId 
        ? `${API_BASE_URL}/api/chat/completions?session_id=${sessionId}`
        : `${API_BASE_URL}/api/chat/completions`;
      
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });
      
      if (!response.ok) {
        throw new Error(`聊天完成处理失败: ${response.statusText}`);
      }
      
      return response.json();
    } catch (error) {
      console.error('聊天完成处理时发生错误:', error);
      throw error;
    }
  }

  // WebSocket聊天连接
  createWebSocketConnection(sessionId?: string): WebSocket {
    const url = sessionId
      ? `${API_BASE_URL.replace('http', 'ws')}/api/ws/chat?session_id=${sessionId}`
      : `${API_BASE_URL.replace('http', 'ws')}/api/ws/chat`;
    
    return new WebSocket(url);
  }

  // 获取可用模型列表
  async getModels(): Promise<ModelListResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/models`);
      
      if (!response.ok) {
        throw new Error(`获取模型列表失败: ${response.statusText}`);
      }
      
      return response.json();
    } catch (error) {
      console.error('获取模型列表时发生错误:', error);
      throw error;
    }
  }
  
  // 生成唯一ID
  generateId(prefix: string = ''): string {
    return `${prefix}${uuidv4()}`;
  }
}

export default new ChatService();
```

### 使用示例

```typescript
// 创建会话
const session = await chatService.createSession("新的聊天会话");

// 发送消息
const response = await chatService.createChatCompletion({
  model: "stellar-byte-llm",
  messages: [
    { role: "user", content: "你好，有什么可以帮助我的吗？" }
  ],
  temperature: 0.7,
  stream: false
}, session.id);

// 获取会话消息
const messages = await chatService.getMessages(session.id);

// WebSocket连接示例
const ws = chatService.createWebSocketConnection(session.id);

ws.onopen = () => {
  console.log("WebSocket连接已建立");
  
  // 发送消息
  ws.send(JSON.stringify({
    type: "chat.message",
    content: "你好，有什么可以帮助我的吗？"
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  switch (data.event) {
    case "session_start":
      console.log("会话开始:", data.data.session_id);
      break;
    case "content_block_delta":
      console.log("收到内容块:", data.data.delta.text);
      break;
    case "message_stop":
      console.log("消息结束");
      break;
    case "error":
      console.error("错误:", data.data.message);
      break;
  }
};
```
## 注意事项
1. 使用TypeScript严格模式确保类型安全
2. 组件开发遵循单一职责原则
3. 实现适当的错误边界
4. 性能优化(useMemo, useCallback, React.memo)
5. 可访问性考虑(ARIA标签, 键盘导航)