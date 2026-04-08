import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authAPI } from '../api';

export default function Register() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirm, setConfirm]   = useState('');
  const [loading, setLoading]   = useState(false);
  const [error, setError]       = useState('');
  const navigate = useNavigate();

  async function handleRegister() {
    if (!username || !password) { setError('กรอกข้อมูลให้ครบ'); return; }
    if (password !== confirm) { setError('รหัสผ่านไม่ตรงกัน'); return; }
    if (password.length < 6) { setError('รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร'); return; }
    setLoading(true); setError('');
    try {
      await authAPI.register(username, password, username);
      alert('สมัครสมาชิกสำเร็จ');
      navigate('/login');
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-body">
      <div className="login-box">
        <div className="logo">♛</div>
        <h2>สมัครสมาชิก</h2>
        {error && <div style={{ color:'#ff6b6b', fontSize:13, marginBottom:8 }}>{error}</div>}
        <input placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} disabled={loading} />
        <input type="password" placeholder="Password (อย่างน้อย 6 ตัว)" value={password} onChange={e => setPassword(e.target.value)} disabled={loading} />
        <input type="password" placeholder="Confirm Password" value={confirm} onChange={e => setConfirm(e.target.value)} disabled={loading} />
        <button onClick={handleRegister} disabled={loading}>{loading ? 'กำลังสมัคร...' : 'สมัครสมาชิก'}</button>
        <div className="login-footer">มีบัญชีแล้ว? <Link to="/login" className="register-btn">เข้าสู่ระบบ</Link></div>
      </div>
    </div>
  );
}
