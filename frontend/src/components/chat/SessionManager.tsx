import React, { useState, useEffect } from 'react';
import type { Session } from '../../types';
import chatService from '../../services/chatService';
import './SessionManager.css';

interface SessionManagerProps {
  onSessionSelect: (sessionId: string | null) => void;
  currentSessionId: string | null;
}

const SessionManager: React.FC<SessionManagerProps> = ({ onSessionSelect, currentSessionId }) => {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [isCreating, setIsCreating] = useState(false);
  const [newSessionTitle, setNewSessionTitle] = useState('');

  // 加载会话列表
  useEffect(() => {
    const loadSessions = async () => {
      try {
        const sessionResponses = await chatService.getSessions();
        const sessionList: Session[] = sessionResponses.map(session => ({
          id: session.id,
          title: session.title,
          created_at: session.created_at,
          updated_at: session.updated_at,
          is_active: session.is_active
        }));
        setSessions(sessionList);
      } catch (error) {
        console.error('加载会话列表失败:', error);
      }
    };

    loadSessions();
  }, []);

  const handleCreateSession = async () => {
    if (!newSessionTitle.trim()) return;

    try {
      const response = await chatService.createSession(newSessionTitle);
      const newSession: Session = {
        id: response.id,
        title: response.title,
        created_at: response.created_at,
        updated_at: response.updated_at,
        is_active: response.is_active
      };
      
      setSessions(prev => [newSession, ...prev]);
      setNewSessionTitle('');
      setIsCreating(false);
      onSessionSelect(newSession.id);
    } catch (error) {
      console.error('创建会话失败:', error);
    }
  };

  const handleDeleteSession = async (sessionId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    
    try {
      await chatService.deleteSession(sessionId);
      const updatedSessions = sessions.filter(session => session.id !== sessionId);
      setSessions(updatedSessions);
      
      // 如果删除的是当前会话，选择第一个会话或null
      if (sessionId === currentSessionId) {
        const newCurrentSession = updatedSessions.length > 0 ? updatedSessions[0] : null;
        onSessionSelect(newCurrentSession ? newCurrentSession.id : null);
      }
    } catch (error) {
      console.error('删除会话失败:', error);
    }
  };

  return (
    <div className="session-manager">
      <div className="session-header">
        <h2>会话</h2>
        <button 
          onClick={() => setIsCreating(true)}
          className="create-session-button"
        >
          +
        </button>
      </div>
      
      {isCreating && (
        <div className="create-session-form">
          <input
            type="text"
            value={newSessionTitle}
            onChange={(e) => setNewSessionTitle(e.target.value)}
            placeholder="会话标题"
            autoFocus
          />
          <div className="form-actions">
            <button onClick={handleCreateSession} disabled={!newSessionTitle.trim()}>
              创建
            </button>
            <button onClick={() => setIsCreating(false)}>
              取消
            </button>
          </div>
        </div>
      )}
      
      <div className="session-list">
        {sessions.map(session => (
          <div 
            key={session.id}
            className={`session-item ${session.id === currentSessionId ? 'active' : ''}`}
            onClick={() => onSessionSelect(session.id)}
          >
            <div className="session-title">{session.title}</div>
            <div className="session-date">
              {new Date(session.updated_at).toLocaleDateString()}
            </div>
            <button 
              className="delete-session-button"
              onClick={(e) => handleDeleteSession(session.id, e)}
            >
              ×
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SessionManager;