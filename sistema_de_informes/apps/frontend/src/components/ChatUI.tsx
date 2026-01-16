import React, { useState } from 'react';

interface ChatMessage {
  sender: 'user' | 'bot';
  text: string;
}

interface ChatUIProps {
  onSend: (message: string) => Promise<string>;
  pdfText?: string;
}

const ChatUI: React.FC<ChatUIProps> = ({ onSend, pdfText }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;
    setMessages([...messages, { sender: 'user', text: input }]);
    setLoading(true);
    const reply = await onSend(input);
    setMessages(msgs => [...msgs, { sender: 'bot', text: reply }]);
    setInput('');
    setLoading(false);
  };

  return (
    <div style={{ border: '1px solid #ccc', padding: 16, borderRadius: 8, maxWidth: 500, margin: '1em auto' }}>
      <div style={{ minHeight: 120, marginBottom: 8 }}>
        {messages.map((msg, i) => (
          <div key={i} style={{ textAlign: msg.sender === 'user' ? 'right' : 'left', margin: '4px 0' }}>
            <b>{msg.sender === 'user' ? 'Tú' : 'Bot'}:</b> {msg.text}
          </div>
        ))}
        {pdfText && (
          <div style={{ background: '#f6f6f6', padding: 8, borderRadius: 4, margin: '8px 0' }}>
            <b>Texto extraído del PDF:</b>
            <pre style={{ whiteSpace: 'pre-wrap', fontSize: 12 }}>{pdfText}</pre>
          </div>
        )}
      </div>
      <input
        type="text"
        value={input}
        onChange={e => setInput(e.target.value)}
        onKeyDown={e => e.key === 'Enter' && handleSend()}
        placeholder="Escribe tu mensaje..."
        style={{ width: '80%', marginRight: 8 }}
        disabled={loading}
      />
      <button onClick={handleSend} disabled={loading || !input.trim()}>
        {loading ? 'Enviando...' : 'Enviar'}
      </button>
    </div>
  );
};

export default ChatUI;
