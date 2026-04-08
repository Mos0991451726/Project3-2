import { useState } from 'react';

export default function Sidebar({ rooms, activeRoomId, onNewChat, onSelectRoom, onDeleteRoom, onLogout }) {
  const [showMenu, setShowMenu] = useState(false);
  const [hoveredRoom, setHoveredRoom] = useState(null);

  const username    = localStorage.getItem('username') || 'ผู้ใช้';
  const displayName = localStorage.getItem('display_name') || username;

  // แบ่ง rooms เป็น วันนี้ / เก่ากว่า
  const now = new Date();
  const todayRooms = rooms.filter(r => {
    const d = new Date(r.last_activity_at || r.created_at);
    return d.toDateString() === now.toDateString();
  });
  const olderRooms = rooms.filter(r => {
    const d = new Date(r.last_activity_at || r.created_at);
    return d.toDateString() !== now.toDateString();
  });

  function RoomItem({ room }) {
    const isActive = room.id === activeRoomId;
    return (
      <div
        className={`chat-item ${isActive ? 'active' : ''}`}
        style={{ display:'flex', alignItems:'center', justifyContent:'space-between', gap:4 }}
        onMouseEnter={() => setHoveredRoom(room.id)}
        onMouseLeave={() => setHoveredRoom(null)}
        onClick={() => onSelectRoom(room)}
      >
        <span style={{ overflow:'hidden', textOverflow:'ellipsis', whiteSpace:'nowrap', flex:1 }}>
          {room.title || 'การสนทนาใหม่'}
        </span>
        {hoveredRoom === room.id && (
          <button
            onClick={e => { e.stopPropagation(); onDeleteRoom(room.id); }}
            style={{
              background:'transparent', border:'none', cursor:'pointer',
              color:'var(--text-muted)', fontSize:14, padding:'0 2px', flexShrink:0,
              lineHeight:1,
            }}
            title="ลบ"
          >✕</button>
        )}
      </div>
    );
  }

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <div className="logo-area">
          <div className="logo-icon">♛</div>
          <div className="logo-text">
            แชทบอท<br />ทองคำ
            <span>Golden AI · v2.0</span>
          </div>
        </div>
        <button className="new-chat-btn" onClick={onNewChat}>
          <svg viewBox="0 0 24 24" strokeWidth="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
          สนทนาใหม่
        </button>
      </div>

      <div className="chat-list">
        {/* วันนี้ */}
        {todayRooms.length > 0 && (
          <>
            <div className="sidebar-section"><div className="sidebar-section-label">วันนี้</div></div>
            {todayRooms.map(r => <RoomItem key={r.id} room={r} />)}
          </>
        )}

        {/* เก่ากว่า */}
        {olderRooms.length > 0 && (
          <>
            <div className="sidebar-section" style={{ paddingTop:20 }}>
              <div className="sidebar-section-label">ก่อนหน้านี้</div>
            </div>
            {olderRooms.map(r => <RoomItem key={r.id} room={r} />)}
          </>
        )}

        {/* ว่าง */}
        {rooms.length === 0 && (
          <div style={{ padding:'20px 12px', color:'var(--text-muted)', fontSize:12, textAlign:'center' }}>
            ยังไม่มีบทสนทนา<br />กด "สนทนาใหม่" เพื่อเริ่ม
          </div>
        )}
      </div>

      <div className="sidebar-footer">
        <div className="user-profile" onClick={() => setShowMenu(v => !v)}>
          <div className="avatar">{displayName.charAt(0).toUpperCase()}</div>
          <div className="user-info">
            <div className="user-name">{displayName}</div>
            <div className="user-plan">Gold Member ✦</div>
          </div>
          {showMenu && (
            <div className="user-menu">
              <div onClick={e => { e.stopPropagation(); setShowMenu(false); onLogout(); }}>
                ออกจากระบบ
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
