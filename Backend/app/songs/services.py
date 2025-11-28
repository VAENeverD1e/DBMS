from services.jamendo_service import JamendoService
from services.s3_service import s3_service
from app.auth.utils import get_db_connection
import pymysql
from typing import Optional, List, Dict

class SongsService:
    def __init__(self):
        self.jamendo_service = JamendoService()
        
    def _resolve_s3_url(self, maybe_key: str) -> Optional[str]:
        if not maybe_key:
            return None
        if maybe_key.startswith('http'):
            return maybe_key
        return s3_service.get_file_url(maybe_key)

    def format_db_song(self, row: Dict) -> Dict:
        """Format a DB song row to frontend song schema"""
        return {
            'jamendo_id': str(row.get('SingleID')),
            'title': row.get('Title') or '',
            'artist': row.get('ArtistName') or 'Unknown',
            'album': row.get('AlbumID'),
            'duration': row.get('Duration'),
            'image_url': self._resolve_s3_url(row.get('CoverImage')),
            'audio_url': self._resolve_s3_url(row.get('FileURL')),
            'license': 'proprietary',
            'license_url': '',
            'release_date': row.get('ReleaseDate').isoformat() if row.get('ReleaseDate') else None,
            'genre': [row.get('Genre')] if row.get('Genre') else [],
            'ArtworkID': row.get('ArtworkID'),  # Include ArtworkID for play history
            'SongID': row.get('SingleID')  # Include SongID alias
        }
    
    def search_songs(self, query: str, limit: int = 20, offset: int = 0, source: str = 'jamendo') -> Optional[List[Dict]]:
        """
        Search for songs from Jamendo API
        
        Args:
            query: Search term (song title, artist name, etc.)
            limit: Number of results (default: 20, max: 100)
            offset: Pagination offset (default: 0)
        
        Returns:
            List of formatted song dictionaries or None if error
        """
        source = (source or 'jamendo').lower()
        # Database-only
        if source == 'database':
            return self.search_songs_from_db(query, limit, offset)

        # Jamendo-only
        if source == 'jamendo':
            response = self.jamendo_service.search_tracks(query, limit, offset)
            if not response:
                return None
            songs = [self.jamendo_service.format_track_response(track) for track in response.get('results', [])]
            return songs

        # both
        if source == 'both':
            # Fetch both sources and merge/dedup by audio_url
            jam_resp = self.jamendo_service.search_tracks(query, limit, offset)
            jam_songs = []
            if jam_resp:
                jam_songs = [self.jamendo_service.format_track_response(t) for t in jam_resp.get('results', [])]

            db_songs = self.search_songs_from_db(query, limit, offset) or []

            # merge, prefer DB songs first then Jamendo, dedupe by audio_url
            seen = set()
            merged = []
            for s in db_songs + jam_songs:
                key = s.get('audio_url') or f"id:{s.get('jamendo_id')}"
                if key in seen:
                    continue
                seen.add(key)
                merged.append(s)
                if len(merged) >= limit:
                    break
            return merged
        # unknown source
        return None
    
    def get_songs_by_genre(self, genre: str, limit: int = 20, source: str = 'jamendo') -> Optional[List[Dict]]:
        """
        Get songs by genre/tag from Jamendo API
        
        Args:
            genre: Genre or tag name
            limit: Number of results (default: 20, max: 100)
        
        Returns:
            List of formatted song dictionaries or None if error
        """
        source = (source or 'jamendo').lower()
        if source == 'database':
            return self.get_songs_by_genre_from_db(genre, limit)
        if source == 'jamendo':
            response = self.jamendo_service.get_tracks_by_genre(genre, limit)
            if not response:
                return None
            return [self.jamendo_service.format_track_response(track) for track in response.get('results', [])]
        if source == 'both':
            jam_resp = self.jamendo_service.get_tracks_by_genre(genre, limit) or {}
            jam_songs = [self.jamendo_service.format_track_response(t) for t in jam_resp.get('results', [])]
            db_songs = self.get_songs_by_genre_from_db(genre, limit) or []
            seen = set(); merged = []
            for s in db_songs + jam_songs:
                key = s.get('audio_url') or f"id:{s.get('jamendo_id')}"
                if key in seen: continue
                seen.add(key); merged.append(s)
                if len(merged) >= limit: break
            return merged
        return None
    
    def get_song_by_id(self, jamendo_id: str, source: str = 'jamendo') -> Optional[Dict]:
        """
        Get a specific song by Jamendo ID
        
        Args:
            jamendo_id: Jamendo track ID
        
        Returns:
            Formatted song dictionary or None if not found/error
        """
        source = (source or 'jamendo').lower()
        if source == 'database':
            return self.get_song_by_id_from_db(jamendo_id)
        if source == 'jamendo':
            track = self.jamendo_service.get_track_by_id(jamendo_id)
            if not track:
                return None
            return self.jamendo_service.format_track_response(track)
        if source == 'both':
            # try DB first
            db = self.get_song_by_id_from_db(jamendo_id)
            if db:
                return db
            return self.get_song_by_id(jamendo_id, source='jamendo')
        return None

    # ---- Database-backed methods ----
    def search_songs_from_db(self, query: str, limit: int = 20, offset: int = 0) -> Optional[List[Dict]]:
        conn = get_db_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cur:
                q = f"%{query}%"
                sql = """
                SELECT s.SingleID, s.ArtworkID, a.Title, a.ReleaseDate, a.CoverImage, a.Duration, a.Genre,
                       s.AlbumID, s.TrackNumber, s.FileURL,
                       CONCAT(u.FirstName, ' ', u.LastName) AS ArtistName
                FROM Single s
                JOIN Artwork a ON a.ArtworkID = s.ArtworkID
                JOIN ReleaseTable rt ON rt.ArtworkID = a.ArtworkID
                JOIN Artist ar ON ar.ArtistID = rt.ArtistID
                JOIN User u ON u.UserID = ar.UserID
                WHERE a.Title LIKE %s OR s.FileURL LIKE %s
                ORDER BY a.ReleaseDate DESC
                LIMIT %s OFFSET %s
                """
                cur.execute(sql, (q, q, limit, offset))
                rows = cur.fetchall()
                return [self.format_db_song(r) for r in rows]
        finally:
            conn.close()

    def get_songs_by_genre_from_db(self, genre: str, limit: int = 20) -> Optional[List[Dict]]:
        conn = get_db_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cur:
                sql = """
                SELECT s.SingleID, s.ArtworkID, a.Title, a.ReleaseDate, a.CoverImage, a.Duration, a.Genre,
                       s.AlbumID, s.TrackNumber, s.FileURL,
                       CONCAT(u.FirstName, ' ', u.LastName) AS ArtistName
                FROM Single s
                JOIN Artwork a ON a.ArtworkID = s.ArtworkID
                JOIN ReleaseTable rt ON rt.ArtworkID = a.ArtworkID
                JOIN Artist ar ON ar.ArtistID = rt.ArtistID
                JOIN User u ON u.UserID = ar.UserID
                WHERE a.Genre = %s
                ORDER BY a.ReleaseDate DESC
                LIMIT %s
                """
                cur.execute(sql, (genre, limit))
                rows = cur.fetchall()
                return [self.format_db_song(r) for r in rows]
        finally:
            conn.close()

    def get_song_by_id_from_db(self, single_id: str) -> Optional[Dict]:
        conn = get_db_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cur:
                sql = """
                SELECT s.SingleID, s.ArtworkID, a.Title, a.ReleaseDate, a.CoverImage, a.Duration, a.Genre,
                       s.AlbumID, s.TrackNumber, s.FileURL,
                       CONCAT(u.FirstName, ' ', u.LastName) AS ArtistName
                FROM Single s
                JOIN Artwork a ON a.ArtworkID = s.ArtworkID
                JOIN ReleaseTable rt ON rt.ArtworkID = a.ArtworkID
                JOIN Artist ar ON ar.ArtistID = rt.ArtistID
                JOIN User u ON u.UserID = ar.UserID
                WHERE s.SingleID = %s
                LIMIT 1
                """
                cur.execute(sql, (single_id,))
                row = cur.fetchone()
                if not row:
                    return None
                return self.format_db_song(row)
        finally:
            conn.close()
