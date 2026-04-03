
  const responses = [
    "ทองคำในปัจจุบันถือเป็นสินทรัพย์ที่ได้รับความนิยมมากในฐานะ <strong>สินทรัพย์ปลอดภัย (Safe Haven)</strong> โดยเฉพาะในช่วงที่เศรษฐกิจโลกมีความผันผวน นักลงทุนมักหันมาถือครองทองคำเพื่อป้องกันความเสี่ยงจากเงินเฟ้อและค่าเงินอ่อนตัว ✦",
    "การลงทุนในทองคำมีหลายรูปแบบ ได้แก่ <strong>ทองคำแท่ง, ทองรูปพรรณ, กองทุน Gold ETF</strong> และฟิวเจอร์สทองคำ แต่ละแบบมีข้อดีข้อเสียต่างกัน ขึ้นอยู่กับวัตถุประสงค์การลงทุนของคุณ ♛",
    "ราคาทองคำมีความสัมพันธ์กับหลายปัจจัย ทั้ง <strong>อัตราดอกเบี้ย, ค่าเงินดอลลาร์, อุปสงค์ทั่วโลก</strong> และสถานการณ์ทางภูมิรัฐศาสตร์ การติดตามปัจจัยเหล่านี้จะช่วยให้คาดการณ์แนวโน้มได้แม่นยำยิ่งขึ้น 📊",
    "สำหรับมือใหม่ที่ต้องการเริ่มลงทุนทองคำ แนะนำให้เริ่มจาก <strong>กองทุน Gold ETF</strong> เพราะง่ายต่อการซื้อขาย ไม่ต้องกังวลเรื่องการเก็บรักษา และสามารถเริ่มต้นด้วยเงินน้อยได้ 🥇",
  ];

  let msgCount = 0;
  let isTyping = false;
  let welcomeVisible = true;

  function autoResize(el) {
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 200) + 'px';
  }

  function toggleSendBtn() {
    const btn = document.getElementById('sendBtn');
    const val = document.getElementById('messageInput').value.trim();
    btn.disabled = !val || isTyping;
  }

  function handleKey(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (!document.getElementById('sendBtn').disabled) sendMessage();
    }
  }

  function sendSuggestion(text) {
    document.getElementById('messageInput').value = text;
    sendMessage();
  }

  function sendMessage() {
    const input = document.getElementById('messageInput');
    const text = input.value.trim();
    if (!text || isTyping) return;

    if (welcomeVisible) {
      document.getElementById('welcomeScreen').style.display = 'none';
      welcomeVisible = false;
    }

    addMessage(text, 'user');
    input.value = '';
    input.style.height = 'auto';
    toggleSendBtn();

    isTyping = true;
    setTimeout(() => showTyping(), 200);
    const delay = 1400 + Math.random() * 800;
    setTimeout(() => {
      removeTyping();
      const r = responses[msgCount % responses.length];
      msgCount++;
      addMessage(r, 'bot');
      isTyping = false;
      toggleSendBtn();
    }, delay);
  }

  function addMessage(text, role) {
    const container = document.querySelector('.chat-container');
    const now = new Date();
    const time = now.getHours().toString().padStart(2,'0') + ':' + now.getMinutes().toString().padStart(2,'0');

    const isBot = role === 'bot';
    const div = document.createElement('div');
    div.className = 'message-group';
    div.innerHTML = `
      <div class="message ${isBot ? 'bot' : 'user'}">
        <div class="msg-avatar ${isBot ? 'bot' : 'user-av'}">${isBot ? '♛' : 'ก'}</div>
        <div class="msg-content">
          <div class="msg-meta">
            <span class="msg-name">${isBot ? 'แชทบอททองคำ' : 'คุณ'}</span>
            <span class="msg-time">${time}</span>
          </div>
          <div class="msg-bubble">${text}</div>
          ${isBot ? `<div class="msg-actions">
            <button class="msg-action-btn"><svg viewBox="0 0 24 24" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>คัดลอก</button>
            <button class="msg-action-btn"><svg viewBox="0 0 24 24" stroke-width="2"><path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"/></svg>ถูกใจ</button>
          </div>` : ''}
        </div>
      </div>`;
    container.appendChild(div);
    scrollToBottom();
  }

  function showTyping() {
    const container = document.querySelector('.chat-container');
    const div = document.createElement('div');
    div.id = 'typingIndicator';
    div.className = 'typing-indicator';
    div.innerHTML = `
      <div class="msg-avatar bot">♛</div>
      <div class="typing-dots">
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
      </div>`;
    container.appendChild(div);
    scrollToBottom();
  }

  function removeTyping() {
    const el = document.getElementById('typingIndicator');
    if (el) el.remove();
  }

  function scrollToBottom() {
    const area = document.getElementById('chatArea');
    area.scrollTop = area.scrollHeight;
  }

  function newChat() {
    const container = document.querySelector('.chat-container');
    container.innerHTML = `<div class="welcome" id="welcomeScreen">
      <div class="welcome-icon">♛</div>
      <h1>แชทบอททองคำ</h1>
      <p>ผู้ช่วยอัจฉริยะด้านการลงทุนทองคำ<br>พร้อมตอบทุกคำถามด้วยความแม่นยำระดับทองคำ</p>
      <div class="gold-divider"><span>เริ่มต้นด้วย</span></div>
      <div class="suggestion-grid">
        <div class="suggestion-card" onclick="sendSuggestion('ราคาทองคำวันนี้เป็นเท่าไหร่')"><div class="suggestion-icon">📈</div><div class="suggestion-title">ราคาทองวันนี้</div><div class="suggestion-desc">ติดตามราคาทองคำล่าสุด</div></div>
        <div class="suggestion-card" onclick="sendSuggestion('ควรลงทุนทองคำหรือหุ้นดีกว่า')"><div class="suggestion-icon">⚖️</div><div class="suggestion-title">เปรียบเทียบการลงทุน</div><div class="suggestion-desc">ทองคำ vs สินทรัพย์อื่น</div></div>
        <div class="suggestion-card" onclick="sendSuggestion('วิธีเริ่มต้นลงทุนทองคำสำหรับมือใหม่')"><div class="suggestion-icon">🏆</div><div class="suggestion-title">มือใหม่เริ่มยังไง</div><div class="suggestion-desc">คำแนะนำสำหรับผู้เริ่มต้น</div></div>
        <div class="suggestion-card" onclick="sendSuggestion('แนวโน้มราคาทองในอีก 6 เดือนข้างหน้า')"><div class="suggestion-icon">🔮</div><div class="suggestion-title">แนวโน้มราคาทอง</div><div class="suggestion-desc">วิเคราะห์อนาคตตลาดทอง</div></div>
      </div>
    </div>`;
    welcomeVisible = true;
    isTyping = false;
    toggleSendBtn();
    document.querySelectorAll('.chat-item').forEach(i => i.classList.remove('active'));
  }
