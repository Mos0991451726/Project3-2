import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authAPI } from '../api';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading]   = useState(false);
  const [error, setError]       = useState('');
  const navigate = useNavigate();

  async function handleLogin() {
    if (!username || !password) { setError('กรอกข้อมูลให้ครบ'); return; }
    setLoading(true);
    setError('');
    try {
      const data = await authAPI.login(username, password);
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('username', data.username);
      localStorage.setItem('display_name', data.display_name);
      navigate('/');
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  function handleKey(e) { if (e.key === 'Enter') handleLogin(); }

  return (
    <div className="auth-body">
      <div className="login-box">
        <div className="logo">♛</div>
        <h2>เข้าสู่ระบบ</h2>
        {error && <div style={{ color:'#ff6b6b', fontSize:13, marginBottom:8 }}>{error}</div>}
        <input placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} onKeyDown={handleKey} disabled={loading} />
        <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} onKeyDown={handleKey} disabled={loading} />
        <button onClick={handleLogin} disabled={loading}>{loading ? 'กำลังเข้าสู่ระบบ...' : 'เข้าสู่ระบบ'}</button>
        <div className="login-footer">ยังไม่มีบัญชี? <Link to="/register" className="register-btn">สมัครสมาชิก</Link></div>
        <div className="login-footer">Golden AI ✦ ระบบผู้ช่วยทองคำ</div>
      </div>
    </div>
  );
}
