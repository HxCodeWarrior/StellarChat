export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export interface Message {
  id: string;
  session_id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  created_at: string;
  tokens: number;
  metadata: Record<string, any> | null;
}

export interface Session {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
}

export interface Message {
  id: string;
  session_id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  created_at: string;
  tokens: number;
  metadata: Record<string, any> | null;
}