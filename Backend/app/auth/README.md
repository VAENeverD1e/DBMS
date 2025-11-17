# Authentication Module

This module provides comprehensive user authentication and authorization for the Music Platform API.

## Features

- User registration with email and username
- Secure password hashing (SHA-256)
- Session-based authentication
- Role-based access control (Listener/Artist)
- Profile management
- Password change functionality
- Account deletion

## API Endpoints

### 1. Register User
**POST** `/api/auth/register`

Create a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123",
  "username": "johndoe",
  "first_name": "John",       // optional
  "last_name": "Doe",         // optional
  "role": "Listener"          // optional, defaults to "Listener"
}
```

**Password Requirements:**
- At least 8 characters long
- Contains at least one uppercase letter
- Contains at least one lowercase letter
- Contains at least one number

**Username Requirements:**
- 3-100 characters
- Must start with a letter
- Alphanumeric and underscores only

**Response (201):**
```json
{
  "message": "User registered successfully",
  "user": {
    "user_id": 1,
    "email": "user@example.com",
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "role": "Listener"
  }
}
```

---

### 2. Login
**POST** `/api/auth/login`

Authenticate and create a session.

**Request Body:**
```json
{
  "email": "user@example.com",  // OR "username": "johndoe"
  "password": "SecurePass123"
}
```

**Response (200):**
```json
{
  "message": "Login successful",
  "user": {
    "user_id": 1,
    "email": "user@example.com",
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "role": "Listener"
  }
}
```

---

### 3. Logout
**POST** `/api/auth/logout`

End the current session. Requires authentication.

**Response (200):**
```json
{
  "message": "Logout successful"
}
```

---

### 4. Get Profile
**GET** `/api/auth/me`

Get current user's profile. Requires authentication.

**Response (200):**
```json
{
  "user": {
    "UserID": 1,
    "Email": "user@example.com",
    "Username": "johndoe",
    "FirstName": "John",
    "LastName": "Doe",
    "Role": "Listener",
    "listener_profile": {
      "ListenerID": 1,
      "Preference": "Pop, Rock",
      "FavoriteGenre": "Rock",
      "LikedArtwork": null
    }
  }
}
```

For artists, the response includes `artist_profile` instead of `listener_profile`:
```json
{
  "user": {
    "UserID": 2,
    "Email": "artist@example.com",
    "Username": "artistname",
    "FirstName": "Artist",
    "LastName": "Name",
    "Role": "Artist",
    "artist_profile": {
      "ArtistID": 1,
      "Genre": "Electronic",
      "VerifiedStatus": "Pending",
      "TotalFollowers": 0,
      "LabelID": null,
      "social_media_links": []
    }
  }
}
```

---

### 5. Update Profile
**PUT** or **PATCH** `/api/auth/me`

Update current user's profile. Requires authentication.

**Request Body:**
```json
{
  "email": "newemail@example.com",     // optional
  "username": "newusername",           // optional
  "first_name": "NewFirstName",        // optional
  "last_name": "NewLastName"           // optional
}
```

**Response (200):**
```json
{
  "message": "Profile updated successfully",
  "user": {
    "user_id": 1,
    "email": "newemail@example.com",
    "username": "newusername",
    "first_name": "NewFirstName",
    "last_name": "NewLastName",
    "role": "Listener"
  }
}
```

---

### 6. Change Password
**POST** `/api/auth/change-password`

Change user password. Requires authentication.

**Request Body:**
```json
{
  "current_password": "OldPass123",
  "new_password": "NewPass456",
  "confirm_password": "NewPass456"
}
```

**Response (200):**
```json
{
  "message": "Password changed successfully"
}
```

---

### 7. Delete Account
**DELETE** `/api/auth/me`

Delete current user's account. Requires authentication.

**Response (200):**
```json
{
  "message": "Account deleted successfully"
}
```

---

### 8. Check Session
**GET** `/api/auth/session`

Check if user has an active session.

**Response (200) - Authenticated:**
```json
{
  "authenticated": true,
  "user": {
    "user_id": 1,
    "email": "user@example.com",
    "username": "johndoe",
    "role": "Listener",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

**Response (200) - Not Authenticated:**
```json
{
  "authenticated": false
}
```

---

## Usage in Other Routes

### Require Authentication

```python
from app.auth import login_required

@app.route('/protected')
@login_required
def protected_route():
    return jsonify({'message': 'Access granted'})
```

### Require Specific Role

```python
from app.auth import role_required

@app.route('/artist-only')
@role_required('Artist')
def artist_route():
    return jsonify({'message': 'Artist access'})

@app.route('/multi-role')
@role_required('Artist', 'Listener')
def multi_role_route():
    return jsonify({'message': 'Access granted to Artists and Listeners'})
```

### Get Current User

```python
from app.auth import get_current_user

@app.route('/current-user')
def current_user_route():
    user = get_current_user()
    if user:
        return jsonify({'user': user})
    else:
        return jsonify({'error': 'Not authenticated'}), 401
```

---

## Module Structure

```
app/auth/
├── __init__.py       # Module exports
├── routes.py         # API endpoints
├── services.py       # Business logic
├── schemas.py        # Request validation
├── utils.py          # Helper functions and decorators
└── README.md         # This file
```

---

## Security Features

1. **Password Hashing**: All passwords are hashed using SHA-256 before storage
2. **Session Management**: Secure session-based authentication with configurable lifetime
3. **Input Validation**: Comprehensive validation for all user inputs
4. **Role-Based Access Control**: Decorators for protecting routes by user role
5. **Unique Constraints**: Email and username must be unique
6. **HTTP-Only Cookies**: Session cookies are HTTP-only to prevent XSS attacks
7. **CORS Support**: Configured for cross-origin requests with credentials

---

## Error Responses

All endpoints return consistent error responses:

```json
{
  "error": "Error message",
  "details": {
    "field": "Specific error for this field"
  }
}
```

Common HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request (validation error)
- `401` - Unauthorized (not authenticated)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found
- `409` - Conflict (duplicate email/username)
- `500` - Internal Server Error

---

## Database Schema

The authentication module works with the following database tables:

### User Table
```sql
CREATE TABLE User (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Email VARCHAR(255) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    Username VARCHAR(100) NOT NULL UNIQUE,
    FirstName VARCHAR(100),
    LastName VARCHAR(100),
    Role ENUM('Listener', 'Artist') NOT NULL DEFAULT 'Listener'
);
```

### Related Tables
- **Listener**: Extended user data for listeners
- **Artist**: Extended user data for artists
- **Artist_SMLinks**: Social media links for artists

---

## Testing

Example test with curl:

```bash
# Register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123",
    "username": "testuser",
    "first_name": "Test",
    "last_name": "User",
    "role": "Listener"
  }'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123"
  }'

# Get Profile (using saved cookies)
curl -X GET http://localhost:5000/api/auth/me \
  -b cookies.txt

# Logout
curl -X POST http://localhost:5000/api/auth/logout \
  -b cookies.txt
```

---

## Notes

- Sessions are persistent for 7 days (configurable in app.py)
- User registration automatically creates corresponding Listener or Artist records
- Deleting a user cascades to all related records (Listener/Artist data)
- Artist accounts start with 'Pending' verification status
