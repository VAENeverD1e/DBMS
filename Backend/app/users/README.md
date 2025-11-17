# Users Module

## Overview

The Users module implements a comprehensive role-based access control system for the music streaming platform. It manages user roles, permissions, subscriptions, and user-specific features.

## Role-Based System

### User Roles

The system supports three distinct user roles:

#### 1. **Guest (Not Logged In)**
- **Database Record**: None
- **Capabilities**:
  - Browse/search music
  - Stream music with **30-second limit only**
  - No account features

#### 2. **Guest (Logged In)**
- **Database Role**: `'Guest'`
- **Capabilities**:
  - Stream full audio (no time limit)
  - Subscribe to plans (Listener or Artist)
  - View profile
  - **Cannot**: Create playlists, react, follow artists, release artwork

#### 3. **Listener**
- **Database Role**: `'Listener'`
- **Capabilities**:
  - All Guest capabilities
  - Create playlists containing songs/albums
  - React to artworks (songs and albums)
  - Follow artists
  - View play history (automatically recorded)
  - **Cannot**: Release artwork

#### 4. **Artist**
- **Database Role**: `'Artist'`
- **Capabilities**:
  - Stream full audio
  - Release artworks (songs/albums)
  - View follower statistics
  - **Cannot**: Create playlists, react, follow (listener features)

## Architecture

### File Structure

```
app/users/
├── __init__.py          # Module initialization and blueprint export
├── routes.py            # API endpoint definitions
├── services.py          # Business logic layer
├── schemas.py           # Request validation schemas
└── README.md           # This file
```

### Dependencies

- `app.auth.utils`: Authentication utilities (session management, decorators)
- `app.utils.decorators`: Role-based access decorators
- `pymysql`: Database connection

## API Endpoints

All endpoints are prefixed with `/api/users`

### User Statistics

#### `GET /me/stats`
Get current user's statistics based on role.

**Auth Required**: Yes (any logged-in user)

**Response**:
```json
{
  "stats": {
    "role": "Listener",
    "playlist_count": 5,
    "following_count": 12,
    "reaction_count": 45
  }
}
```

**For Artists**:
```json
{
  "stats": {
    "role": "Artist",
    "artwork_count": 8,
    "followers_count": 234
  }
}
```

---

### Listener Preferences

#### `PUT/PATCH /me/preferences`
Update listener preferences.

**Auth Required**: Listener role

**Request Body**:
```json
{
  "preference": "Prefer upbeat music",
  "favorite_genre": "Rock"
}
```

**Response**:
```json
{
  "message": "Preferences updated successfully",
  "preferences": {
    "ListenerID": 1,
    "Preference": "Prefer upbeat music",
    "FavoriteGenre": "Rock"
  }
}
```

---

### Play History

#### `GET /me/history`
Get user's play history (Listener only).

**Auth Required**: Listener role

**Query Parameters**:
- `limit` (int, optional): Number of records (1-100, default: 50)
- `offset` (int, optional): Pagination offset (default: 0)

**Response**:
```json
{
  "history": [
    {
      "HistoryID": 123,
      "SongID": 456,
      "PlayedAt": "2025-01-15T10:30:00",
      "ListenDuration": 180,
      "song_title": "Amazing Song",
      "song_duration": 200,
      "ArtworkID": 789,
      "artwork_title": "Great Album",
      "artist_username": "cool_artist"
    }
  ],
  "pagination": {
    "limit": 50,
    "offset": 0,
    "count": 1
  }
}
```

#### `POST /me/history`
Record a song play in history.

**Auth Required**: Listener role

**Request Body**:
```json
{
  "song_id": 456,
  "listen_duration": 180
}
```

**Response**:
```json
{
  "history_id": 123,
  "message": "Play history recorded"
}
```

---

### Following Artists

#### `GET /me/following`
Get list of artists the user is following.

**Auth Required**: Listener role

**Query Parameters**:
- `limit` (int, optional): Number of records (1-100, default: 50)
- `offset` (int, optional): Pagination offset (default: 0)

**Response**:
```json
{
  "artists": [
    {
      "FollowID": 1,
      "FollowedDate": "2025-01-10T12:00:00",
      "ArtistID": 5,
      "Genre": "Rock",
      "VerifiedStatus": "Verified",
      "TotalFollowers": 1234,
      "UserID": 10,
      "Username": "rockstar",
      "FirstName": "John",
      "LastName": "Doe"
    }
  ],
  "pagination": {
    "limit": 50,
    "offset": 0,
    "count": 1
  }
}
```

#### `POST /me/following/<artist_id>`
Follow an artist.

**Auth Required**: Listener role

**Response**:
```json
{
  "message": "Successfully followed artist"
}
```

**Error Responses**:
- `404`: Artist not found
- `409`: Already following this artist

#### `DELETE /me/following/<artist_id>`
Unfollow an artist.

**Auth Required**: Listener role

**Response**:
```json
{
  "message": "Successfully unfollowed artist"
}
```

**Error Responses**:
- `404`: Not following this artist

---

### Reactions (Likes)

#### `GET /me/reactions`
Get user's reactions (liked songs/albums).

**Auth Required**: Listener role

**Query Parameters**:
- `type` (str, optional): Filter by 'Song' or 'Artwork'
- `limit` (int, optional): Number of records (1-100, default: 50)
- `offset` (int, optional): Pagination offset (default: 0)

**Response**:
```json
{
  "reactions": [
    {
      "ReactionID": 1,
      "ReactableType": "Song",
      "ReactableID": 456,
      "Emotion": "Like",
      "ReactedAt": "2025-01-15T10:30:00"
    }
  ],
  "pagination": {
    "limit": 50,
    "offset": 0,
    "count": 1
  }
}
```

---

### Role Upgrade

#### `POST /upgrade-role`
Upgrade user role after successful subscription payment.

**Auth Required**: Yes (any logged-in user)

**Note**: This endpoint is typically called automatically by the payment webhook handler.

**Request Body**:
```json
{
  "new_role": "Listener"
}
```

**Response**:
```json
{
  "message": "Role upgraded successfully",
  "user": {
    "user_id": 1,
    "email": "user@example.com",
    "username": "username",
    "first_name": "John",
    "last_name": "Doe",
    "role": "Listener"
  }
}
```

**Error Responses**:
- `400`: Invalid role or missing new_role
- `409`: Invalid role transition (e.g., already has the role)

---

## Role-Based Decorators

The module uses custom decorators from `app/utils/decorators.py`:

### `@guest_optional`
Routes accessible to both authenticated and unauthenticated users.

```python
@app.route('/music/stream/<id>')
@guest_optional
def stream_music(id):
    # Check session.get('user_id') to see if authenticated
    pass
```

### `@login_required`
Requires any logged-in user (Guest, Listener, or Artist).

```python
@app.route('/subscribe')
@login_required
def subscribe():
    pass
```

### `@listener_required`
Requires Listener role specifically.

```python
@app.route('/playlists/create')
@listener_required
def create_playlist():
    pass
```

### `@artist_required`
Requires Artist role specifically.

```python
@app.route('/artworks/create')
@artist_required
def create_artwork():
    pass
```

### `@role_required('Listener', 'Artist')`
Requires one of the specified roles.

```python
@app.route('/profile')
@role_required('Listener', 'Artist')
def profile():
    pass
```

---

## Service Layer

### `UserService` Class

#### Methods

##### `upgrade_user_role(user_id, new_role)`
Upgrade user from Guest to Listener or Artist.

**Parameters**:
- `user_id` (int): User's ID
- `new_role` (str): 'Listener' or 'Artist'

**Returns**: `(success: bool, result: dict/str)`

**Database Changes**:
- Updates `User.Role`
- Creates `Listener` or `Artist` record if doesn't exist

---

##### `get_user_stats(user_id)`
Get role-specific statistics for the user.

**Returns**: `dict` or `None`

---

##### `update_listener_preferences(user_id, preference, favorite_genre)`
Update listener's preferences.

**Returns**: `(success: bool, result: dict/str)`

---

##### `get_play_history(user_id, limit, offset)`
Get user's play history with pagination.

**Returns**: `(success: bool, result: list/str)`

---

##### `record_play_history(user_id, song_id, listen_duration)`
Record a song play in user's history.

**Returns**: `(success: bool, result: dict/str)`

---

##### `get_following_artists(user_id, limit, offset)`
Get list of artists user is following.

**Returns**: `(success: bool, result: list/str)`

---

##### `follow_artist(user_id, artist_id)`
Follow an artist. Updates artist's follower count.

**Returns**: `(success: bool, result: dict/str)`

---

##### `unfollow_artist(user_id, artist_id)`
Unfollow an artist. Updates artist's follower count.

**Returns**: `(success: bool, result: dict/str)`

---

##### `get_user_reactions(user_id, reactable_type, limit, offset)`
Get user's reactions (likes) with optional filtering.

**Returns**: `(success: bool, result: list/str)`

---

## Integration with Other Modules

### Subscriptions Module
The Users module works closely with the Subscriptions module:

1. Guest users subscribe to a plan via `/api/plans`
2. Payment is processed via `/api/payments`
3. After successful payment, subscription is created
4. Subscription service calls `UserService.upgrade_user_role()`
5. User role is upgraded to Listener or Artist
6. Session is updated with new role

### Example Flow:

```
Guest User → Subscribe to Listener Plan → Payment Success
→ Subscription Created → Role Upgraded to Listener
→ Can now create playlists, follow artists, etc.
```

---

## Database Schema

### Related Tables

#### `User` Table
- `UserID` (PK)
- `Email`
- `Password`
- `Username`
- `FirstName`
- `LastName`
- **`Role`** ('Guest', 'Listener', 'Artist')

#### `Listener` Table
- `ListenerID` (PK)
- `UserID` (FK → User)
- `Preference`
- `FavoriteGenre`

#### `Artist` Table
- `ArtistID` (PK)
- `UserID` (FK → User)
- `Genre`
- `VerifiedStatus`
- `TotalFollowers`
- `LabelID` (FK)

#### `Follow` Table
- `FollowID` (PK)
- `ListenerID` (FK → Listener)
- `ArtistID` (FK → Artist)
- `FollowedDate`

#### `PlayHistory` Table
- `HistoryID` (PK)
- `ListenerID` (FK → Listener)
- `SongID` (FK → Song)
- `PlayedAt`
- `ListenDuration`

#### `Reaction` Table
- `ReactionID` (PK)
- `ListenerID` (FK → Listener)
- `ReactableType` ('Song' or 'Artwork')
- `ReactableID`
- `Emotion`
- `ReactedAt`

---

## Error Handling

### Common HTTP Status Codes

- **200 OK**: Successful request
- **201 Created**: Resource created successfully
- **400 Bad Request**: Validation error or missing required fields
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Insufficient permissions (wrong role)
- **404 Not Found**: Resource not found
- **409 Conflict**: Resource already exists or invalid state transition
- **500 Internal Server Error**: Database or server error

### Error Response Format

```json
{
  "error": "Error message",
  "details": "Additional error details"
}
```

---

## Usage Examples

### Example 1: Register as Guest and Upgrade to Listener

```bash
# 1. Register as Guest (default)
POST /api/auth/register
{
  "email": "user@example.com",
  "password": "SecurePass123",
  "username": "musiclover"
}

# 2. Login (if not auto-logged in)
POST /api/auth/login
{
  "email": "user@example.com",
  "password": "SecurePass123"
}

# 3. Subscribe to Listener plan
POST /api/plans/subscribe
{
  "plan_id": 1
}

# 4. Make payment (handled by payment module)
POST /api/payments/create-checkout-session
{
  "plan_id": 1
}

# 5. After payment success, role is automatically upgraded
# Check new role
GET /api/auth/me

# 6. Now can follow artists
POST /api/users/me/following/5

# 7. Create playlist (now available as Listener)
POST /api/playlists
{
  "name": "My Favorites"
}
```

### Example 2: Listener Views Play History

```bash
# Record some plays
POST /api/users/me/history
{
  "song_id": 123,
  "listen_duration": 180
}

# View history
GET /api/users/me/history?limit=20&offset=0
```

### Example 3: Follow/Unfollow Artists

```bash
# Follow an artist
POST /api/users/me/following/5

# Get following list
GET /api/users/me/following

# Unfollow an artist
DELETE /api/users/me/following/5
```

---

## Testing

### Manual Testing with curl

```bash
# Get user stats
curl -X GET http://localhost:5000/api/users/me/stats \
  -H "Cookie: session=YOUR_SESSION_COOKIE"

# Follow an artist
curl -X POST http://localhost:5000/api/users/me/following/5 \
  -H "Cookie: session=YOUR_SESSION_COOKIE"

# Update preferences
curl -X PUT http://localhost:5000/api/users/me/preferences \
  -H "Content-Type: application/json" \
  -H "Cookie: session=YOUR_SESSION_COOKIE" \
  -d '{"favorite_genre": "Rock"}'
```

---

## Security Considerations

1. **Role Verification**: All role-specific endpoints use decorators to verify user roles
2. **Session Management**: User roles are stored in Flask sessions and verified on each request
3. **Input Validation**: All user inputs are validated using schemas
4. **SQL Injection Prevention**: Parameterized queries are used throughout
5. **Authorization**: Users can only access their own data (user_id from session)

---

## Future Enhancements

- [ ] Add email verification for new users
- [ ] Implement role-specific permissions for more granular access control
- [ ] Add user badges and achievements system
- [ ] Implement collaborative playlists (multiple listeners)
- [ ] Add artist verification workflow
- [ ] Implement user blocking/reporting features
- [ ] Add privacy settings for user profiles

---

## Support

For issues or questions about the Users module, please check:

1. This README
2. API endpoint documentation above
3. Source code comments in `services.py` and `routes.py`

---

**Last Updated**: January 2025
**Version**: 1.0.0
