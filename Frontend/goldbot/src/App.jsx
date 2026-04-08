import { useState, useRef, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Message from './components/Message';
import SettingsModal from './components/SettingsModal';
import ShareModal from './components/ShareModal';
import { roomAPI, authAPI } from './api';

const SUGGESTIONS = [
  { icon: '📈', title: 'ราคาทองวันนี้',       desc: 'ติดตามราคาทองคำล่าสุด',     text: 'ราคาทองคำวันนี้เป็นเท่าไหร่' },
  { icon: '⚖️', title: 'เปรียบเทียบการลงทุน', desc: 'ทองคำ vs สินทรัพย์อื่น',   text: 'ควรลงทุนทองคำหรือหุ้นดีกว่า' },
  { icon: '🏆', title: 'มือใหม่เริ่มยังไง',   desc: 'คำแนะนำสำหรับผู้เริ่มต้น', text: 'วิธีเริ่มต้นลงทุนทองคำสำหรับมือใหม่' },
  { icon: '🔮', title: 'แนวโน้มราคาทอง',      desc: 'วิเคราะห์อนาคตตลาดทอง',    text: 'แนวโน้มราคาทองในอีก 6 เดือนข้างหน้า' },
];

function getTime() {
  const n = new Date();
  return n.getHours().toString().padStart(2,'0') + ':' + n.getMinutes().toString().padStart(2,'0');
}

export default function App() {
  const navigate = useNavigate();
  const [rooms, setRooms]               = useState([]);
  const [activeRoom, setActiveRoom]     = useState(null);
  const [messages, setMessages]         = useState([]);
  const [input, setInput]               = useState('');
  const [isTyping, setIsTyping]         = useState(false);
  const [showWelcome, setShowWelcome]   = useState(true);
  const [showSettings, setShowSettings] = useState(false);
  const [showShare, setShowShare]       = useState(false);
  const [loadingMsgs, setLoadingMsgs]   = useState(false);
  const chatAreaRef = useRef(null);
  const textareaRef = useRef(null);

  useEffect(() => {
    if (!localStorage.getItem('token')) navigate('/login');
    else loadRooms();
  }, []);

  useEffect(() => {
    if (chatAreaRef.current)
      chatAreaRef.current.scrollTop = chatAreaRef.current.scrollHeight;
  }, [messages, isTyping]);

  async function loadRooms() {
    try { setRooms(await roomAPI.list()); } catch (e) { console.error(e); }
  }

  async function openRoom(room) {
    setActiveRoom(room);
    setShowWelcome(false);
    setLoadingMsgs(true);
    try {
      const msgs = await roomAPI.getMessages(room.id);
      setMessages(msgs.map(m => ({
        role: m.role === 'assistant' ? 'bot' : 'user',
        text: m.content,
        time: new Date(m.created_at).toLocaleTimeString('th-TH', { hour:'2-digit', minute:'2-digit' }),
      })));
    } catch (e) { console.error(e); }
    finally { setLoadingMsgs(false); }
  }

  function newChat() {
    setActiveRoom(null);
    setMessages([]);
    setShowWelcome(true);
    setInput('');
  }

  async function deleteRoom(roomId) {
    try {
      await roomAPI.delete(roomId);
      setRooms(prev => prev.filter(r => r.id !== roomId));
      if (activeRoom?.id === roomId) newChat();
    } catch (e) { console.error(e); }
  }

  const sendMessage = useCallback(async (textOverride) => {
    const msg = (textOverride || input).trim();
    if (!msg || isTyping) return;

    const time = getTime();
    setInput('');
    if (textareaRef.current) textareaRef.current.style.height = 'auto';
    setIsTyping(true);
    setShowWelcome(false);
    setMessages(prev => [...prev, { role:'user', text:msg, time }]);

    try {
      let data;
      if (activeRoom) {
        data = await roomAPI.sendMessage(activeRoom.id, msg);
      } else {
        data = await roomAPI.quickChat(msg);
        setActiveRoom({ id: data.room_id, title: msg.substring(0, 40) });
        await loadRooms();
      }

      const botTime = new Date(data.bot_message.created_at)
        .toLocaleTimeString('th-TH', { hour:'2-digit', minute:'2-digit' });

      setMessages(prev => [...prev, { role:'bot', text:data.bot_message.content, time:botTime }]);

      setRooms(prev => prev.map(r =>
        r.id === data.room_id ? { ...r, title: msg.substring(0,40) } : r
      ));
    } catch (e) {
      setMessages(prev => [...prev, { role:'bot', text:`⚠️ เกิดข้อผิดพลาด: ${e.message}`, time:getTime() }]);
    } finally {
      setIsTyping(false);
    }
  }, [input, isTyping, activeRoom]);

  function handleKey(e) {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
  }

  function autoResize(el) {
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 200) + 'px';
  }

  function handleLogout() {
    authAPI.logout();
    navigate('/login');
  }

  const canSend = input.trim().length > 0 && !isTyping;

  return (
    <div className="app-layout">
      <div className="ornament ornament-tl" />
      <div className="ornament ornament-br" />

      <Sidebar
        rooms={rooms}
        activeRoomId={activeRoom?.id}
        onNewChat={newChat}
        onSelectRoom={openRoom}
        onDeleteRoom={deleteRoom}
        onLogout={handleLogout}
      />

      <div className="main">
        <div className="topbar">
          <div className="model-selector">
            <div className="model-dot" />
            GoldBot Ultra 2.0
            <svg viewBox="0 0 24 24" strokeWidth="2" style={{ width:12,height:12,stroke:'currentColor',fill:'none' }}>
              <polyline points="6 9 12 15 18 9" />
            </svg>
          </div>
          <div className="topbar-actions">
            <button className="icon-btn" title="แชร์" onClick={() => setShowShare(true)}>
              <svg viewBox="0 0 24 24" strokeWidth="2">
                <circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/>
                <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/>
                <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/>
              </svg>
            </button>
            <button className="icon-btn" title="ตั้งค่า" onClick={() => setShowSettings(true)}>
              <svg viewBox="0 0 24 24" strokeWidth="2">
                <circle cx="12" cy="12" r="3"/>
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>
              </svg>
            </button>
          </div>
        </div>

        <div className="chat-area" ref={chatAreaRef}>
          <div className="chat-container">
            {showWelcome && (
              <div className="welcome">
                <div className="welcome-icon">♛</div>
                <h1>แชทบอททองคำ</h1>
                <p>ผู้ช่วยอัจฉริยะด้านการลงทุนทองคำ<br />พร้อมตอบทุกคำถามด้วยความแม่นยำระดับทองคำ</p>
                <div className="gold-divider"><span>เริ่มต้นด้วย</span></div>
                <div className="suggestion-grid">
                  {SUGGESTIONS.map((s, i) => (
                    <div key={i} className="suggestion-card" onClick={() => sendMessage(s.text)}>
                      <div className="suggestion-icon">{s.icon}</div>
                      <div className="suggestion-title">{s.title}</div>
                      <div className="suggestion-desc">{s.desc}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {loadingMsgs && (
              <div style={{ textAlign:'center', color:'var(--text-muted)', padding:40, fontSize:14 }}>
                กำลังโหลดบทสนทนา...
              </div>
            )}

            {!loadingMsgs && messages.map((m, i) => (
              <Message key={i} role={m.role} text={m.text} time={m.time} />
            ))}

            {isTyping && (
              <div className="typing-indicator">
                <div className="msg-avatar bot">♛</div>
                <div className="typing-dots">
                  <div className="typing-dot" /><div className="typing-dot" /><div className="typing-dot" />
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="input-area">
          <div className="input-wrapper">
            <div className="input-box">
              <div className="input-tools">
                <button className="tool-btn" title="แนบไฟล์">
                  <svg viewBox="0 0 24 24" strokeWidth="2"><path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"/></svg>
                </button>
                <button className="tool-btn" title="ค้นหาเว็บ">
                  <svg viewBox="0 0 24 24" strokeWidth="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
                </button>
              </div>
              <textarea
                ref={textareaRef}
                className="msg-input"
                rows="1"
                placeholder="ถามเรื่องทองคำได้เลย..."
                value={input}
                onChange={e => { setInput(e.target.value); autoResize(e.target); }}
                onKeyDown={handleKey}
                disabled={isTyping}
              />
              <button className="send-btn" disabled={!canSend} onClick={() => sendMessage()}>
                <svg viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round">
                  <line x1="22" y1="2" x2="11" y2="13"/>
                  <polygon points="22 2 15 22 11 13 2 9 22 2"/>
                </svg>
              </button>
            </div>
            <div className="input-footer">แชทบอททองคำ อาจเกิดข้อผิดพลาดได้ โปรดตรวจสอบข้อมูลสำคัญ ✦</div>
          </div>
        </div>
      </div>

      {showSettings && <SettingsModal onClose={() => setShowSettings(false)} onSave={() => {}} />}
      {showShare && <ShareModal messages={messages} onClose={() => setShowShare(false)} />}
    </div>
  );
}
