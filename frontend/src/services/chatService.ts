import { v4 as uuidv4 } from 'uuid';
import type { ChatMessage } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export interface ChatCompletionRequest {
  model: string;
  messages: ChatMessage[];
  temperature?: number;
  top_p?: number;
  max_tokens?: number;
  stream?: boolean;
}

export interface ChatCompletionResponse {
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

export interface SessionResponse {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
}

export interface MessageResponse {
  id: string;
  session_id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  created_at: string;
  tokens: number;
  metadata: Record<string, any> | null;
}

class ChatService {
  // 创建新会话
  async createSession(title: string): Promise<SessionResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/sessions`, {
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
  async getSessions(): Promise<SessionResponse[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/sessions`);
      
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
      const response = await fetch(`${API_BASE_URL}/sessions/${sessionId}`);
      
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
      const response = await fetch(`${API_BASE_URL}/sessions/${sessionId}`, {
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
      const response = await fetch(`${API_BASE_URL}/sessions/${sessionId}`, {
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
  async addMessage(sessionId: string, message: Omit<MessageResponse, 'id' | 'session_id' | 'created_at'>): Promise<MessageResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/sessions/${sessionId}/messages`, {
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
  async getMessages(sessionId: string): Promise<MessageResponse[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/sessions/${sessionId}/messages`);
      
      if (!response.ok) {
        throw new Error(`获取消息失败: ${response.statusText}`);
      }
      
      return response.json();
    } catch (error) {
      console.error('获取消息时发生错误:', error);
      throw error;
    }
  }

  // 创建聊天完成
  async createChatCompletion(request: ChatCompletionRequest, sessionId?: string): Promise<ChatCompletionResponse> {
    try {
      const url = sessionId 
        ? `${API_BASE_URL}/chat/completions?session_id=${sessionId}`
        : `${API_BASE_URL}/chat/completions`;
      
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
  
  // 生成唯一ID
  generateId(prefix: string = ''): string {
    return `${prefix}${uuidv4()}`;
  }
}

export default new ChatService();