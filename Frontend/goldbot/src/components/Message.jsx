const username = localStorage.getItem('username') || 'ผู้ใช้';

export default function Message({ role, text, time }) {
  const isBot = role === 'bot';

  function copyText() {
    navigator.clipboard.writeText(text.replace(/<[^>]+>/g, ''));
  }

  return (
    <div className="message-group">
      <div className={`message ${isBot ? 'bot' : 'user'}`}>
        <div className={`msg-avatar ${isBot ? 'bot' : 'user-av'}`}>
          {isBot ? '♛' : username.charAt(0).toUpperCase()}
        </div>
        <div className="msg-content">
          <div className="msg-meta">
            <span className="msg-name">{isBot ? 'แชทบอททองคำ' : 'คุณ'}</span>
            <span className="msg-time">{time}</span>
          </div>
          <div
            className="msg-bubble"
            dangerouslySetInnerHTML={{ __html: text }}
          />
          {isBot && (
            <div className="msg-actions">
              <button className="msg-action-btn" onClick={copyText}>
                <svg viewBox="0 0 24 24" strokeWidth="2">
                  <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
                  <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
                </svg>
                คัดลอก
              </button>
              <button className="msg-action-btn">
                <svg viewBox="0 0 24 24" strokeWidth="2">
                  <path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"/>
                </svg>
                ถูกใจ
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
