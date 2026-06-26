import { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Sparkles } from 'lucide-react';

export default function ChatInterface({ onCommandSubmit, processing }) {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'bot',
      text: "Hi! I'm your AI PDF Assistant. Upload a document and tell me what you'd like to do. For example, 'Redact all emails' or 'Add a draft watermark'."
    }
  ]);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, processing]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || processing) return;

    const userMsg = { id: Date.now(), sender: 'user', text: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    onCommandSubmit(input, setMessages);
  };

  return (
    <div className="chat-section glass-panel">
      <div className="chat-header">
        <Sparkles size={20} className="text-accent" style={{ color: 'var(--accent-color)' }} />
        AI Assistant
      </div>
      
      <div className="chat-messages">
        {messages.map((msg) => (
          <div key={msg.id} className={`message ${msg.sender} animate-fade-in`}>
            <div className="message-avatar">
              {msg.sender === 'bot' ? <Bot size={18} /> : <User size={18} />}
            </div>
            <div className="message-content">
              {msg.text}
            </div>
          </div>
        ))}
        
        {processing && (
          <div className="message bot animate-fade-in">
            <div className="message-avatar">
              <Bot size={18} />
            </div>
            <div className="message-content" style={{ display: 'flex', alignItems: 'center' }}>
              <div className="typing-indicator">
                <div className="typing-dot"></div>
                <div className="typing-dot"></div>
                <div className="typing-dot"></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form className="chat-input-container" onSubmit={handleSubmit}>
        <input 
          type="text" 
          className="chat-input"
          placeholder="Type a command..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={processing}
        />
        <button type="submit" className="send-button" disabled={processing || !input.trim()}>
          <Send size={16} />
        </button>
      </form>
    </div>
  );
}
