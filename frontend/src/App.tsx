import { useState } from 'react';
import SessionManager from './components/chat/SessionManager';
import ChatInterface from './components/chat/ChatInterface';
import './App.css';

function App() {
  const [currentSessionId, setCurrentSessionId] = useState<string | null>(null);

  return (
    <div className="app">
      <header className="app-header">
        <h1>StellarChat</h1>
      </header>
      <div className="app-content">
        <SessionManager 
          onSessionSelect={setCurrentSessionId}
          currentSessionId={currentSessionId}
        />
        <div className="chat-container">
          {currentSessionId ? (
            <ChatInterface sessionId={currentSessionId} />
          ) : (
            <div className="welcome-message">
              <h2>欢迎使用 StellarChat</h2>
              <p>选择一个现有会话或创建新会话开始聊天</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
