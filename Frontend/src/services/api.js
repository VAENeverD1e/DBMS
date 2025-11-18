// Central API helper for all services
// Handles base URL, auth token storage and request wrapper

const API_BASE = import.meta.env.VITE_API_BASE_URL || '';
const TOKEN_KEY = 'auth_token';

function setToken(token) {
  if (!token) return;
  localStorage.setItem(TOKEN_KEY, token);
}

function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

function removeToken() {
  localStorage.removeItem(TOKEN_KEY);
}

async function request(path, options = {}) {
  const headers = Object.assign({}, options.headers || {});
  const token = getToken();
  if (token) headers['Authorization'] = `Bearer ${token}`;

  if (!headers['Content-Type'] && !(options.body instanceof FormData)) {
    headers['Content-Type'] = 'application/json';
  }

  const res = await fetch(`${API_BASE}${path}`, Object.assign({}, options, { headers }));

  if (!res.ok) {
    const text = await res.text();
    let payload;
    try { payload = JSON.parse(text); } catch { payload = { message: text || res.statusText }; }
    const error = new Error(payload.error || payload.message || 'Request failed');
    error.status = res.status;
    error.payload = payload;
    throw error;
  }

  if (res.status === 204) return null;

  const contentType = res.headers.get('content-type') || '';
  if (contentType.includes('application/json')) return res.json();
  return res.text();
}

export default {
  API_BASE,
  request,
  setToken,
  getToken,
  removeToken,
};
