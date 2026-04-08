import { useState } from 'react';

export default function SettingsModal({ onClose, onSave }) {
  const [name, setName] = useState(localStorage.getItem('name') || '');
  const [theme, setTheme] = useState(localStorage.getItem('theme') || 'dark');
  const [notify, setNotify] = useState(localStorage.getItem('notify') === 'true');

  function handleSave() {
    localStorage.setItem('name', name);
    localStorage.setItem('theme', theme);
    localStorage.setItem('notify', notify);
    onSave({ name, theme });
    alert('บันทึกสำเร็จ');
    onClose();
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-box" onClick={e => e.stopPropagation()}>
        <h2>⚙️ ตั้งค่า</h2>

        <label>ชื่อผู้ใช้</label>
        <input value={name} onChange={e => setName(e.target.value)} placeholder="กรอกชื่อ" />

        <label>โหมดธีม</label>
        <select value={theme} onChange={e => setTheme(e.target.value)}>
          <option value="dark">Dark (ทอง)</option>
          <option value="light">Light</option>
        </select>

        <label style={{ display: 'flex', alignItems: 'center', gap: 8, cursor: 'pointer', marginBottom: 14 }}>
          <input
            type="checkbox"
            checked={notify}
            onChange={e => setNotify(e.target.checked)}
            style={{ width: 'auto', margin: 0 }}
          />
          เปิดเสียงแจ้งเตือน
        </label>

        <button className="modal-btn" onClick={handleSave}>บันทึก</button>
        <button className="modal-btn secondary" onClick={onClose}>ปิด</button>
      </div>
    </div>
  );
}
