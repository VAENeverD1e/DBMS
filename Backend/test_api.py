import requests

BASE = 'http://127.0.0.1:5000'
s = requests.Session()

# Register
r = s.post(f'{BASE}/api/auth/register', json={
    'email': 'testuser@example.com',
    'password': 'Pass1234!',
    'username': 'testuser'
})
print('register', r.status_code, r.json())

# Login
r = s.post(f'{BASE}/api/auth/login', json={'email': 'testuser@example.com', 'password': 'Pass1234!'})
print('login', r.status_code, r.json())

# Get profile
r = s.get(f'{BASE}/api/auth/me')
print('me', r.status_code, r.json())

# Change password (if implemented)
r = s.post(f'{BASE}/api/auth/change-password', json={
    'current_password': 'Pass1234!',
    'new_password': 'NewPass456!',
    'confirm_password': 'NewPass456!'
})
print('change-password', r.status_code, r.json())

# Logout
r = s.post(f'{BASE}/api/auth/logout')
print('logout', r.status_code, r.json())