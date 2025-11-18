import requests
import json

BASE = 'http://127.0.0.1:5000'

def print_response(label, response):
    """Pretty print API response"""
    print(f'\n{"="*60}')
    print(f'{label}')
    print(f'{"="*60}')
    print(f'Status Code: {response.status_code}')
    try:
        print(f'Response: {json.dumps(response.json(), indent=2)}')
    except:
        print(f'Response: {response.text}')

# Test 1: Register a new user with all fields
print('\n' + '='*60)
print('TEST 1: Register New User (with first_name and last_name)')
print('='*60)
r = requests.post(f'{BASE}/api/auth/register', json={
    'email': 'testuser@example.com',
    'password': 'TestPass123',
    'username': 'testuser',
    'first_name': 'Test',
    'last_name': 'User',
    'role': 'Listener'
})
print_response('Register', r)

# Test 2: Try to register with same email (should fail)
print('\n' + '='*60)
print('TEST 2: Register Duplicate User (should fail)')
print('='*60)
r = requests.post(f'{BASE}/api/auth/register', json={
    'email': 'testuser@example.com',
    'password': 'TestPass123',
    'username': 'testuser2',
})
print_response('Register Duplicate', r)

# Test 3: Register a Guest user
print('\n' + '='*60)
print('TEST 3: Register Guest User')
print('='*60)
r = requests.post(f'{BASE}/api/auth/register', json={
    'email': 'guestuser@example.com',
    'password': 'GuestPass123',
    'username': 'guestuser',
    'role': 'Guest'
})
print_response('Register Guest', r)

# Test 4: Register an Artist user
print('\n' + '='*60)
print('TEST 4: Register Artist User')
print('='*60)
r = requests.post(f'{BASE}/api/auth/register', json={
    'email': 'artist@example.com',
    'password': 'ArtistPass123',
    'username': 'artistuser',
    'first_name': 'Artist',
    'last_name': 'Name',
    'role': 'Artist'
})
print_response('Register Artist', r)

# Test 5: Login with email
print('\n' + '='*60)
print('TEST 5: Login with Email')
print('='*60)
r = requests.post(f'{BASE}/api/auth/login', json={
    'email': 'testuser@example.com',
    'password': 'TestPass123'
})
print_response('Login', r)

# Store token for authenticated requests
token = None
if r.status_code == 200:
    try:
        token = r.json().get('token')
    except:
        pass

# Test 6: Get user profile (requires authentication)
if token:
    print('\n' + '='*60)
    print('TEST 6: Get User Profile')
    print('='*60)
    headers = {'Authorization': f'Bearer {token}'}
    r = requests.get(f'{BASE}/api/auth/me', headers=headers)
    print_response('Get Profile', r)

# Test 7: Login with wrong password (should fail)
print('\n' + '='*60)
print('TEST 7: Login with Wrong Password (should fail)')
print('='*60)
r = requests.post(f'{BASE}/api/auth/login', json={
    'email': 'testuser@example.com',
    'password': 'WrongPassword123'
})
print_response('Login Failed', r)

# Test 8: Invalid password format during registration (should fail)
print('\n' + '='*60)
print('TEST 8: Register with Weak Password (should fail)')
print('='*60)
r = requests.post(f'{BASE}/api/auth/register', json={
    'email': 'weakpass@example.com',
    'password': 'weak',
    'username': 'weakuser',
})
print_response('Weak Password', r)

# Test 9: Invalid email format (should fail)
print('\n' + '='*60)
print('TEST 9: Register with Invalid Email (should fail)')
print('='*60)
r = requests.post(f'{BASE}/api/auth/register', json={
    'email': 'notanemail',
    'password': 'ValidPass123',
    'username': 'invalidemail',
})
print_response('Invalid Email', r)

# Test 10: Access protected route without token (should fail)
print('\n' + '='*60)
print('TEST 10: Access Protected Route Without Token (should fail)')
print('='*60)
r = requests.get(f'{BASE}/api/auth/me')
print_response('No Token', r)

print('\n' + '='*60)
print('ALL TESTS COMPLETED')
print('='*60)