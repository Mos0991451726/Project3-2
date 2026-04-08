const BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function getToken() {
  return localStorage.getItem('token');
}

async function request(path, options = {}) {
  const token = getToken();
  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  };

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 300000); // 5 นาที

  try {
    const res = await fetch(`${BASE_URL}${path}`, {
      ...options,
      headers,
      signal: controller.signal,
    });
    clearTimeout(timeoutId);

    if (res.status === 401) {
      localStorage.clear();
      window.location.href = '/login';
      return;
    }

    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'เกิดข้อผิดพลาด');
    return data;
  } catch (e) {
    clearTimeout(timeoutId);
    if (e.name === 'AbortError') throw new Error('หมดเวลา กรุณาลองใหม่');
    throw e;
  }
}

// ─── Auth ───
export const authAPI = {
  register: (username, password, display_name) =>
    request('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ username, password, display_name }),
    }),

  login: (username, password) =>
    request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    }),

  logout: () => {
    const token = getToken();
    localStorage.clear();
    return request('/auth/logout', {
      method: 'POST',
      body: JSON.stringify(token),
    });
  },
};

// ─── Chat Rooms ───
export const roomAPI = {
  list: () => request('/chat/rooms'),

  create: (title = 'การสนทนาใหม่') =>
    request('/chat/rooms', {
      method: 'POST',
      body: JSON.stringify({ title }),
    }),

  delete: (roomId) =>
    request(`/chat/rooms/${roomId}`, { method: 'DELETE' }),

  getMessages: (roomId) => request(`/chat/rooms/${roomId}/messages`),

  sendMessage: (roomId, content) =>
    request(`/chat/rooms/${roomId}/messages`, {
      method: 'POST',
      body: JSON.stringify({ content }),
    }),

  quickChat: (content) =>
    request('/chat/quick', {
      method: 'POST',
      body: JSON.stringify({ content }),
    }),
};