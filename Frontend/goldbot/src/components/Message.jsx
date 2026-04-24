const username = localStorage.getItem('username') || 'ผู้ใช้';

function formatText(text) {
  // ลบ Markdown ที่ model ส่งมา
  const cleaned = text
    .replace(/#{1,6}\s?/g, '')           // ลบ ## หัวข้อ
    .replace(/\*\*(.*?)\*\*/g, '$1')     // ลบ **bold**
    .replace(/\*(.*?)\*/g, '$1')         // ลบ *italic*
    .replace(/\|\|/g, '')                // ลบ ||
    .replace(/---+/g, '')                // ลบ ---
    .replace(/^\s*[-•]\s/gm, '• ')      // จัด bullet
    .replace(/\n{3,}/g, '\n\n')         // ลด newline ซ้อนกัน

  const lines = cleaned.split('\n').filter(l => l.trim() !== '')

  return lines.map((line, i) => {
    const trimmed = line.trim()

    // บรรทัดที่เป็น bullet
    if (trimmed.startsWith('•') || trimmed.startsWith('-')) {
      return (
        <div key={i} style={{ display:'flex', gap:8, margin:'3px 0', lineHeight:1.7 }}>
          <span style={{ color:'var(--gold-mid)', flexShrink:0 }}>•</span>
          <span>{trimmed.replace(/^[•\-]\s*/, '')}</span>
        </div>
      )
    }

    // บรรทัดที่เป็น numbered list เช่น 1. 2. 3.
    if (/^\d+\./.test(trimmed)) {
      const num   = trimmed.match(/^(\d+)\./)[1]
      const rest  = trimmed.replace(/^\d+\.\s*/, '')
      return (
        <div key={i} style={{ display:'flex', gap:8, margin:'3px 0', lineHeight:1.7 }}>
          <span style={{ color:'var(--gold-mid)', flexShrink:0, minWidth:18 }}>{num}.</span>
          <span>{rest}</span>
        </div>
      )
    }

    // บรรทัดปกติ
    return (
      <p key={i} style={{ margin:'4px 0', lineHeight:1.75 }}>
        {trimmed}
      </p>
    )
  })
}

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
          <div className="msg-bubble">
            {isBot ? formatText(text) : text}
          </div>
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