# Music Streaming API - Endpoint Reference

## Quick Reference Guide

### Base URL
```
http://localhost:5000
```

### Authentication
All authenticated routes require a JWT token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

---

## Plans Module - `/api/plans`

### GET /api/plans
Get all subscription plans
- **Auth:** Optional
- **Query:** `include_inactive=true/false`
- **Response:** List of plans

### GET /api/plans/:plan_id
Get specific plan details
- **Auth:** Optional
- **Response:** Plan object

### POST /api/plans
Create new plan (Admin only)
- **Auth:** Required (login_required)
- **Body:**
  ```json
  {
    "name": "Listener Monthly",
    "description": "Monthly listener subscription",
    "price": 9.99,
    "duration_days": 30,
    "role_granted": "Listener"
  }
  ```

### PUT /api/plans/:plan_id
Update plan (Admin only)
- **Auth:** Required (login_required)
- **Body:** Any of name, description, price, duration_days, is_active

### DELETE /api/plans/:plan_id
Deactivate plan (Admin only)
- **Auth:** Required (login_required)

---

## Artists Module - `/api/artists`

### GET /api/artists
Get all artists
- **Auth:** Optional
- **Query:** `genre=Rock`, `verified=Verified`, `search=name`, `limit=50`, `offset=0`
- **Response:** List of artists

### GET /api/artists/:artist_id
Get artist details
- **Auth:** Optional
- **Response:** Artist with user info

### GET /api/artists/:artist_id/artworks
Get artist's artworks
- **Auth:** Optional
- **Query:** `limit`, `offset`
- **Response:** List of artworks

### GET /api/artists/:artist_id/stats
Get artist statistics
- **Auth:** Optional
- **Response:**
  ```json
  {
    "followers": 1000,
    "artworks": 25,
    "total_likes": 5000,
    "songs": 75
  }
  ```

### PUT /api/artists/me
Update own artist profile
- **Auth:** Required (artist_required)
- **Body:**
  ```json
  {
    "genre": "Rock"
  }
  ```

### PUT /api/artists/me/social-links
Update social media links
- **Auth:** Required (artist_required)
- **Body:**
  ```json
  {
    "social_links": "instagram.com/artist twitter.com/artist"
  }
  ```

---

## Artworks Module - `/api/artworks`

### GET /api/artworks
Get all artworks
- **Auth:** Optional
- **Query:** `artist_id=1`, `genre=Rock`, `type=Album`, `search=title`, `limit=50`, `offset=0`
- **Response:** List of artworks

### GET /api/artworks/:artwork_id
Get artwork details with songs
- **Auth:** Optional
- **Response:** Artwork with song list

### GET /api/artworks/:artwork_id/songs
Get songs in artwork
- **Auth:** Optional
- **Response:** List of songs

### POST /api/artworks
Create artwork (Album or Single)
- **Auth:** Required (artist_required)
- **Body:**
  ```json
  {
    "title": "My Album",
    "type": "Album",
    "genre": "Rock",
    "release_date": "2025-01-01",
    "cover_image": "https://example.com/cover.jpg"
  }
  ```

### PUT /api/artworks/:artwork_id
Update artwork
- **Auth:** Required (artist_required, owner only)
- **Body:** Any of title, genre, cover_image

### DELETE /api/artworks/:artwork_id
Delete artwork
- **Auth:** Required (artist_required, owner only)

---

## Songs Module - `/api/songs`

### GET /api/songs
Get all songs
- **Auth:** Optional
- **Query:** `genre=Rock`, `artist_id=1`, `search=title`, `limit=50`, `offset=0`
- **Response:** List of songs

### GET /api/songs/:song_id
Get song details
- **Auth:** Optional
- **Response:** Song with artwork and artist info

### GET /api/songs/:song_id/stream
Stream song
- **Auth:** Optional
- **Access:**
  - Not logged in: 30-second preview
  - Logged in: Full audio
- **Response:**
  ```json
  {
    "song": {...},
    "stream_url": "...",
    "access_type": "preview|full",
    "duration_allowed": 30|null
  }
  ```

### POST /api/songs
Create song
- **Auth:** Required (artist_required)
- **Body:**
  ```json
  {
    "artwork_id": 1,
    "title": "Song Title",
    "track_number": 1,
    "duration": 240,
    "audio_file_url": "https://example.com/song.mp3"
  }
  ```

### PUT /api/songs/:song_id
Update song
- **Auth:** Required (artist_required, owner only)
- **Body:** Any of title, track_number, duration, audio_file_url

### DELETE /api/songs/:song_id
Delete song
- **Auth:** Required (artist_required, owner only)

---

## Playlists Module - `/api/playlists`

### GET /api/playlists
Get all playlists
- **Auth:** Optional
- **Query:** `own=true` (requires auth), `limit=50`, `offset=0`
- **Response:** List of playlists

### GET /api/playlists/:playlist_id
Get playlist with songs
- **Auth:** Optional
- **Response:** Playlist with ordered song list

### POST /api/playlists
Create playlist
- **Auth:** Required (listener_required)
- **Body:**
  ```json
  {
    "name": "My Favorites"
  }
  ```

### PUT /api/playlists/:playlist_id
Update playlist name
- **Auth:** Required (listener_required, owner only)
- **Body:**
  ```json
  {
    "name": "New Name"
  }
  ```

### DELETE /api/playlists/:playlist_id
Delete playlist
- **Auth:** Required (listener_required, owner only)

### POST /api/playlists/:playlist_id/songs
Add song to playlist
- **Auth:** Required (listener_required, owner only)
- **Body:**
  ```json
  {
    "song_id": 123,
    "order_index": 5
  }
  ```
  (order_index is optional, auto-calculated if omitted)

### DELETE /api/playlists/:playlist_id/songs/:song_id
Remove song from playlist
- **Auth:** Required (listener_required, owner only)

---

## Reactions Module - `/api/reactions`

### POST /api/reactions
Create or update reaction
- **Auth:** Required (listener_required)
- **Body:**
  ```json
  {
    "reactable_type": "Song",
    "reactable_id": 123,
    "emotion": "Like"
  }
  ```
  - `reactable_type`: "Song" or "Artwork"
  - `emotion`: "Like", "Love", or "Dislike" (default: "Like")

### DELETE /api/reactions/:reaction_id
Delete reaction
- **Auth:** Required (listener_required, owner only)

### GET /api/reactions/song/:song_id
Get all reactions for a song
- **Auth:** Optional
- **Response:**
  ```json
  {
    "reactions": [...],
    "summary": {
      "Like": 100,
      "Love": 50,
      "Dislike": 5
    }
  }
  ```

### GET /api/reactions/artwork/:artwork_id
Get all reactions for an artwork
- **Auth:** Optional
- **Response:** Same as song reactions

---

## User Flows

### Guest User (Not Logged In)
1. Browse artists: `GET /api/artists`
2. View artworks: `GET /api/artworks`
3. View songs: `GET /api/songs`
4. Preview song (30s): `GET /api/songs/:song_id/stream`
5. View plans: `GET /api/plans`

### Guest User (Logged In)
All of the above, plus:
- Full audio streaming: `GET /api/songs/:song_id/stream`
- View public playlists: `GET /api/playlists`

### Listener
All of the above, plus:
- Create playlists: `POST /api/playlists`
- Add songs to playlists: `POST /api/playlists/:id/songs`
- React to songs: `POST /api/reactions`
- View own playlists: `GET /api/playlists?own=true`

### Artist
Can view everything, plus:
- Create artworks: `POST /api/artworks`
- Create songs: `POST /api/songs`
- Update own profile: `PUT /api/artists/me`
- Manage own artworks and songs

---

## Response Codes

- **200** OK - Success
- **201** Created - Resource created successfully
- **400** Bad Request - Validation error
- **401** Unauthorized - Authentication required
- **403** Forbidden - Insufficient permissions
- **404** Not Found - Resource not found
- **409** Conflict - Resource already exists
- **500** Internal Server Error - Server error

---

## Error Response Format

```json
{
  "error": "Error message",
  "details": "Additional details (optional)"
}
```

---

## Example Requests

### Create Listener Playlist
```bash
curl -X POST http://localhost:5000/api/playlists \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Workout Mix"
  }'
```

### Add Song to Playlist
```bash
curl -X POST http://localhost:5000/api/playlists/1/songs \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "song_id": 42
  }'
```

### React to Song
```bash
curl -X POST http://localhost:5000/api/reactions \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "reactable_type": "Song",
    "reactable_id": 42,
    "emotion": "Love"
  }'
```

### Create Album (Artist)
```bash
curl -X POST http://localhost:5000/api/artworks \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Greatest Hits",
    "type": "Album",
    "genre": "Rock",
    "release_date": "2025-01-15",
    "cover_image": "https://example.com/cover.jpg"
  }'
```

### Add Song to Album (Artist)
```bash
curl -X POST http://localhost:5000/api/songs \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "artwork_id": 1,
    "title": "Hit Single",
    "track_number": 1,
    "duration": 240,
    "audio_file_url": "https://example.com/song.mp3"
  }'
```

---

## Notes

- All timestamps are in UTC
- Pagination defaults: limit=50, offset=0
- Maximum limit: 100 per request
- Search is case-insensitive with LIKE pattern
- Owner verification is enforced for all modifications
- Soft deletes are used where applicable (Plans)

---

**Last Updated:** 2025-01-19
