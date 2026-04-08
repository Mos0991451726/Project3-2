export default function ShareModal({ messages, onClose }) {
  const chatText = messages.map(m => `${m.role === 'bot' ? 'แชทบอท' : 'คุณ'}: ${m.text.replace(/<[^>]+>/g, '')}`).join('\n\n');

  function copyShare() {
    navigator.clipboard.writeText(chatText);
    alert('คัดลอกแล้ว ✦');
  }

  function shareTo(platform) {
    const text = encodeURIComponent(chatText);
    const urls = {
      x: `https://twitter.com/intent/tweet?text=${text}`,
      linkedin: `https://www.linkedin.com/sharing/share-offsite/?url=${window.location.href}`,
      reddit: `https://www.reddit.com/submit?title=Chat&text=${text}`,
    };
    window.open(urls[platform], '_blank');
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="share-box" onClick={e => e.stopPropagation()}>
        <div className="share-header">
          <h3>แชร์บทสนทนา</h3>
          <span className="share-close" onClick={onClose}>✕</span>
        </div>
        <div className="share-content">
          <p>บทสนทนานี้อาจมีข้อมูลส่วนบุคคล</p>
          <textarea readOnly value={chatText} />
        </div>
        <div className="share-actions">
          <button onClick={copyShare}>🔗<br />คัดลอกลิงก์</button>
          <button onClick={() => shareTo('x')}>✖️<br />X</button>
          <button onClick={() => shareTo('linkedin')}>💼<br />LinkedIn</button>
          <button onClick={() => shareTo('reddit')}>👽<br />Reddit</button>
        </div>
      </div>
    </div>
  );
}
