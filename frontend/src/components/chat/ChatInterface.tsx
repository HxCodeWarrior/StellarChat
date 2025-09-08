import React, { useState, useEffect, useRef } from 'react';
import type { ChatMessage } from '../../types';
import chatService from '../../services/chatService';
import ChatMessageComponent from './ChatMessage';
import './ChatInterface.css';

interface ChatInterfaceProps {
  sessionId: string | null;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({ sessionId }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // 加载会话消息
  useEffect(() => {
    const loadMessages = async () => {
      if (!sessionId) {
        setMessages([]);
        return;
      }
      
      try {
        const messageResponses = await chatService.getMessages(sessionId);
        const chatMessages: ChatMessage[] = messageResponses.map(msg => ({
          role: msg.role as 'user' | 'assistant' | 'system',
          content: msg.content
        }));
        setMessages(chatMessages);
      } catch (error) {
        console.error('加载消息失败:', error);
        setMessages([]);
      }
    };

    loadMessages();
  }, [sessionId]);

  // 滚动到最新消息
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading || !sessionId) return;

    try {
      // 添加用户消息到UI
      const userMessage: ChatMessage = {
        role: 'user',
        content: inputValue
      };
      
      const newMessages = [...messages, userMessage];
      setMessages(newMessages);
      setInputValue('');
      setIsLoading(true);

      // 保存用户消息到数据库
      await chatService.addMessage(sessionId, {
        role: 'user',
        content: inputValue,
        tokens: inputValue.length,
        metadata: null
      });

      // 发送请求到聊天API
      const request = {
        model: 'stellar-byte-llm',
        messages: newMessages,
        stream: false
      };

      const response = await chatService.createChatCompletion(request, sessionId);
      
      // 添加AI回复到UI
      const aiMessage: ChatMessage = response.choices[0].message;
      setMessages(prev => [...prev, aiMessage]);
      
      // 保存AI回复到数据库
      await chatService.addMessage(sessionId, {
        role: 'assistant',
        content: aiMessage.content,
        tokens: aiMessage.content.length,
        metadata: null
      });
    } catch (error) {
      console.error('发送消息失败:', error);
      // 添加错误消息到UI
      const errorMessage: ChatMessage = {
        role: 'assistant',
        content: '抱歉，发送消息时出现错误。请稍后再试。'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="chat-interface">
      <div className="messages-container">
        {messages.map((message, index) => (
          <ChatMessageComponent key={index} message={message} />
        ))}
        {isLoading && (
          <div className="message assistant">
            <div className="message-content">
              <div className="message-role">StellarChat</div>
              <div className="message-text typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <div className="input-container">
        <textarea
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="输入消息..."
          disabled={isLoading || !sessionId}
          rows={3}
        />
        <button 
          onClick={handleSendMessage} 
          disabled={isLoading || !inputValue.trim() || !sessionId}
          className="send-button"
        >
          发送
        </button>
      </div>
    </div>
  );
};

export default ChatInterface;