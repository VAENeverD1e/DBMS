// Auth service for the frontend
// Uses the central `api` helper for requests and token management

import api from './api';

const { request, setToken: apiSetToken, getToken: apiGetToken, removeToken: apiRemoveToken, API_BASE } = api;

async function login({ email, password }) {
  const data = await request('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  });
  if (data && data.token) apiSetToken(data.token);
  return data;
}

async function signup(payload) {
    console.log("Signup payload:", payload);
  const data = await request('/auth/register', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
  if (data && data.token) apiSetToken(data.token);
  return data;
}

function logout() {
  apiRemoveToken();
}

function getToken() {
  return apiGetToken();
}

async function getCurrentUser() {
  return request('/auth/me');
}

export default {
  API_BASE,
  setToken: apiSetToken,
  getToken,
  removeToken: apiRemoveToken,
  request,
  login,
  signup,
  logout,
  getCurrentUser,
};
