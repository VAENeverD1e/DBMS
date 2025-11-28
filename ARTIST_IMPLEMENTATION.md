# Artist Implementation

## Overview
This document describes the current implementation of the **Artist** feature in both backend and frontend, and outlines how they are intended to work together.

- **Backend**: `backend/app/artists` (Flask blueprint + service layer)
- **Frontend**: `frontend/src/pages/Artist` (Artist pages for artist and listener views)

---

## Backend: `app.artists`

### Blueprint
`backend/app/artists/routes.py`

- Base URL: `/api/artists`

#### 1. `GET /api/artists/`
- **Description**: Get all artists with optional filtering and pagination.
- **Query params**:
  - `genre` (str, optional)
  - `verified` (str, optional, one of `Verified`, `Pending`, `Unverified`)
  - `search` (str, optional, matches username or name)
  - `limit` (int, default 50, 1–100)
  - `offset` (int, default 0, ≥ 0)
- **Response** (200):
  - `{ "artists": [...], "pagination": { "limit", "offset", "count" } }`

#### 2. `GET /api/artists/<int:artist_id>`
- **Description**: Get details of a single artist.
- **Response** (200):
  - `{ "artist": { ArtistID, UserID, Genre, VerifiedStatus, TotalFollowers, SMLinks, CreatedAt, Username, FirstName, LastName, Email } }`

#### 3. `GET /api/artists/<int:artist_id>/artworks`
- **Description**: Get artworks created by an artist.
- **Query params**:
  - `limit` (int, default 50, 1–100)
  - `offset` (int, default 0, ≥ 0)
- **Response** (200):
  - `{ "artworks": [ { ArtworkID, Title, Genre, ReleaseDate, Duration, TotalLike, CoverImage, Type, song_count } ], "pagination": { ... } }`

#### 4. `GET /api/artists/<int:artist_id>/stats`
- **Description**: Aggregate statistics about an artist.
- **Response** (200):
  - `{ "stats": { artist_id, followers_count, artwork_count, total_likes, song_count } }`

#### 5. `GET /api/artists/<int:artist_id>/followers`
- **Description**: Get followers of an artist, with pagination.
- **Query params**: `limit`, `offset` (same rules as above).
- **Response** (200):
  - `{ "followers": [...], "total": <int>, "pagination": { limit, offset, count } }`

#### 6. `PUT|PATCH /api/artists/me`
- **Auth**: `artist_required`.
- **Description**: Update the authenticated artist profile (currently genre).
- **Body**:
  - `{ "genre": "Rock" }` (optional field, validated in `schemas.py`).
- **Response** (200):
  - `{ "message": "Artist profile updated successfully", "artist": { ...updated artist fields... } }`

#### 7. `PUT|PATCH /api/artists/me/social-links`
- **Auth**: `artist_required`.
- **Description**: Update social media links for the current artist.
- **Body**:
  - `{ "social_links": "https://twitter.com/..., https://instagram.com/..." }`
- **Response** (200):
  - `{ "message": "Social links updated successfully", "artist": { ...updated artist fields... } }`

#### 8. `POST /api/artists/me/verify`
- **Auth**: `artist_required`.
- **Description**: Self-verification endpoint that checks whether the artist meets project prerequisites.
- **Prerequisites**:
  - Followers ≥ 670
  - Artworks ≥ 3
- **Success (200)**:
  - `{ "message": "Artist verified successfully" | "Artist already verified", ... }`
- **Failure (400)**:
  - `{ "message": "Verification prerequisites not met", "reasons": [...], "current": { followers, artworks }, "required": { followers, artworks } }`

### Service Layer
`backend/app/artists/services.py`

The `ArtistService` class encapsulates DB calls (using `pymysql` and `get_db_connection`). Important methods:

- `get_artist_id(user_id)` → `ArtistID` or `None`.
- `get_all_artists(genre, verified, search, limit, offset)` → list of artists.
- `get_artist_by_id(artist_id)` → single artist row.
- `get_artist_artworks(artist_id, limit, offset)` → list of artworks with `song_count`.
- `get_artist_stats(artist_id)` → aggregated stats for followers, artworks, likes, and songs.
- `update_artist_profile(user_id, genre)` → update `Genre` for the current artist.
- `update_social_links(user_id, social_links)` → update `SMLinks`.
- `get_listener_id(user_id)` → helper to map user to listener.
- `get_followers(artist_id, limit, offset)` → list of followers & total count.
- `self_verify(user_id)` → core logic behind `/me/verify` endpoint.

---

## Frontend: Artist Pages

Location: `frontend/src/pages/Artist`

### 1. `ArtistHomePage.jsx`
- Role: **Artist dashboard** for logged-in artists.
- Features:
  - Displays artist profile (name, followers, reactions, avatar).
  - Sections: Popular Songs, Discography (New Release), Albums, Songs.
  - Actions:
    - Upload artwork (`UploadArtworkModal`).
    - Join record label (`JoinRecordLabelModal`).
- Current state:
  - Uses **hard-coded mock data** for all content (artist info, songs, artworks).
  - No real API calls yet to `/api/artists` or any artwork endpoints.
  - Navigation:
    - Clicking artworks/albums triggers `navigate("/artist/artwork/${itemId}")`.

### 2. `ArtistProfilePage.jsx`
- Role: **Listener view** of an artist profile.
- Uses `useParams()` to read `id` (artist ID) from the URL.
- Features:
  - Artist header with image, followers, reactions, and label link.
  - Popular Songs, Discography, Albums, Songs sections.
  - Actions:
    - Play button.
    - Follow button (`isFollowing` local state only for now).
    - Heart/like button (local `isLiked`).
  - Right sidebar (`RightSidebar`) with current/upcoming song and artist info.
  - Bottom `PlayerBar`.
- Current state:
  - All data (artist, label, songs, artworks) is mocked.
  - Does **not** call:
    - `GET /api/artists/:id`
    - `GET /api/artists/:id/stats`
    - `GET /api/artists/:id/artworks`
    - or any follow/like endpoints.

### 3. `ArtistArtworkDetailPage.jsx`
- Role: **Artist view** of a single artwork and its tracks.
- Uses `useParams()` to read `id` (artwork ID) from the URL.
- Features:
  - Artwork header (cover, title, artist, year, track count, duration).
  - Track list with play selection, likes count, and delete track.
  - Actions:
    - Play button.
    - Edit artwork via `UploadArtworkModal` in edit mode.
    - Delete artwork.
    - Delete individual track.
- Current state:
  - `albumData` and `tracks` are **hard-coded**.
  - `handleSaveEdit`, `handleDelete`, `handleDeleteTrack` only log to console.
  - No real calls to any backend artwork/track endpoints.

---

## Integration Status

✅ **COMPLETED** - Backend and frontend are now integrated!

### Backend Endpoints Added:
- `GET /api/artists/me` - Get current artist profile, stats, and recent artworks
- `POST /api/artists/<artist_id>/follow` - Follow an artist (listener only)
- `DELETE /api/artists/<artist_id>/follow` - Unfollow an artist (listener only)
- `GET /api/artists/<artist_id>/relationship` - Check follow status
- `GET /api/artists/me/artworks/<artwork_id>` - Get artwork detail with tracks
- `DELETE /api/artists/me/artworks/<artwork_id>` - Delete an artwork

### Frontend Integration:
- **`artistService.js`** - New service with all API methods
- **`ArtistHomePage`** - Fetches artist profile, stats, and artworks from API
- **`ArtistProfilePage`** - Fetches artist data, supports follow/unfollow
- **`ArtistArtworkDetailPage`** - Fetches artwork details and tracks, supports delete

---

## Proposed Integration Plan

### Backend Additions

To fully support the current UI design, we recommend adding these endpoints (if not already implemented elsewhere):

1. **Current artist profile**
   - `GET /api/artists/me`
   - Returns combined:
     - `artist` → from `get_artist_by_id(get_artist_id(user_id))`
     - `stats` → from `get_artist_stats(artist_id)`.

2. **Artwork detail + tracks**
   - `GET /api/artworks/<int:artwork_id>` (or scoped under artist routes).
   - Returns:
     - `artwork`: fields like `ArtworkID, Title, Genre, ReleaseDate, Duration, TotalLike, CoverImage, Type`.
     - `tracks`: associated songs (id, title, duration, likes, etc.).

3. **Artwork & track mutation endpoints**
   - `PUT /api/artworks/<int:artwork_id>` → update metadata and (optionally) track list.
   - `DELETE /api/artworks/<int:artwork_id>` → delete artwork.
   - `DELETE /api/songs/<int:song_id>` → delete track.

4. **Follow / unfollow**
   - Uses `Follow` table and `get_listener_id(user_id)`.
   - `POST /api/artists/<int:artist_id>/follow`
   - `DELETE /api/artists/<int:artist_id>/follow`
   - Optional: `GET /api/artists/<int:artist_id>/relationship` → `{ is_following: bool }`.

5. **(Optional) Like / unlike**
   - For artwork and/or songs to back the like UI.
   - `POST /api/artworks/<int:artwork_id>/like`
   - `DELETE /api/artworks/<int:artwork_id>/like`

6. **Upload single (artist-owned local content)**
   - `POST /api/artists/me/singles`
   - **Auth**: `artist_required`.
   - **Body (example)**:
     - `{ "title", "genre", "release_date", "duration", "cover_image", "file_url", "track_number"? }`
   - **Behavior**:
     - Insert into `Artwork` (core metadata for the release).
     - Insert into `Single` (track-level details, including `FileURL` and optional `TrackNumber`).
     - Insert into `ReleaseTable` linking the current `ArtistID` to the new `ArtworkID`.
   - This endpoint backs the "Upload single" flow in the artist dashboard.

### Frontend Changes

#### ArtistHomePage

- On mount:
  - Call `GET /api/artists/me` and populate `artistData` from response.
  - Call `GET /api/artists/<artist_id>/artworks` for discography and albums.
- Replace all mock lists (`popularSongs`, `discography`, `albums`, `songs`) with data transformed from backend responses.
- Hook `UploadArtworkModal.onUpload` to a real artwork creation endpoint (e.g. `POST /api/artists/me/singles` for standalone tracks), then refresh lists.

#### ArtistProfilePage

- On mount (using `id` from URL):
  - Call `GET /api/artists/:id` → basic artist info.
  - Call `GET /api/artists/:id/stats` → followers and reactions.
  - Call `GET /api/artists/:id/artworks` → discography and albums.
- Replace mock `popularSongs`, `discography`, `albums`, `songs` with API-driven data.
- Wire Follow button:
  - `POST /api/artists/:id/follow` and `DELETE /api/artists/:id/follow`.
  - Sync `isFollowing` and optionally followers count.

#### ArtistArtworkDetailPage

- On mount (using `id` from URL):
  - Call `GET /api/artworks/:id` (or equivalent) to load `albumData` and `tracks`.
- Edit flow:
  - `UploadArtworkModal.onUpload` → `PUT /api/artworks/:id` then refetch.
- Delete flow:
  - `DELETE /api/artworks/:id` then `navigate("/artist/home")`.
- Delete track:
  - `DELETE /api/songs/:trackId` then update `tracks` or refetch.

---

## Notes

- This document focuses on the **Artist** feature only and is intended to mirror the style of `PLAYLIST_IMPLEMENTATION.md`.
- Exact payload shapes can be refined while wiring up the actual API client (e.g., axios hooks) in the frontend.
