from services.jamendo_service import JamendoService
from services.s3_service import S3Service
from app.auth.utils import get_db_connection
from typing import Optional, List, Dict
import pymysql


class ArtworksService:
    def __init__(self):
        self.jamendo_service = JamendoService()
        self.s3_service = S3Service()

    def _resolve_s3_url(self, maybe_key):
        """Resolve S3 key to full URL"""
        if not maybe_key:
            return None
        if maybe_key.startswith('http'):
            return maybe_key
        return self.s3_service.get_file_url(maybe_key)

    def format_db_album(self, row: Dict) -> Dict:
        """Format database album row to standard format"""
        return {
            'jamendo_id': str(row.get('AlbumID') or row.get('SingleID') or ''),
            'title': row.get('Title') or '',
            'artist': row.get('ArtistName') or 'Unknown',
            'release_date': row.get('ReleaseDate').isoformat() if row.get('ReleaseDate') else None,
            'image_url': self._resolve_s3_url(row.get('CoverImage')),
            'track_count': row.get('TotalTrack') or 1,
            'genre': row.get('Genre') or '',
            'ArtworkID': row.get('ArtworkID'),
            'ArtistID': row.get('ArtistID'),
            'AlbumID': row.get('AlbumID'),
            'SingleID': row.get('SingleID')
        }

    def search_albums_from_db(self, query: str, limit: int = 20, offset: int = 0) -> Optional[List[Dict]]:
        """Search for albums from database"""
        conn = get_db_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cur:
                sql = """
                    SELECT
                        alb.AlbumID,
                        alb.TotalTrack,
                        NULL as SingleID,
                        a.ArtworkID,
                        a.Title,
                        a.ReleaseDate,
                        a.CoverImage,
                        a.Duration,
                        a.Genre,
                        ar.ArtistID,
                        CONCAT(u.FirstName, ' ', u.LastName) AS ArtistName
                    FROM Artwork a
                    JOIN Album alb ON alb.ArtworkID = a.ArtworkID
                    JOIN ReleaseTable rt ON rt.ArtworkID = a.ArtworkID
                    JOIN Artist ar ON ar.ArtistID = rt.ArtistID
                    JOIN User u ON u.UserID = ar.UserID
                    WHERE a.Title LIKE %s OR CONCAT(u.FirstName, ' ', u.LastName) LIKE %s
                    ORDER BY a.ReleaseDate DESC
                    LIMIT %s OFFSET %s
                """
                search_term = f"%{query}%"
                cur.execute(sql, (search_term, search_term, limit, offset))
                rows = cur.fetchall()

                return [self.format_db_album(row) for row in rows]
        except Exception as e:
            print(f"Database error in search_albums_from_db: {e}")
            return []
        finally:
            conn.close()

    def get_albums_by_genre_from_db(self, genre: str, limit: int = 20) -> Optional[List[Dict]]:
        """Get albums by genre from database"""
        conn = get_db_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cur:
                sql = """
                    SELECT
                        alb.AlbumID,
                        alb.TotalTrack,
                        NULL as SingleID,
                        a.ArtworkID,
                        a.Title,
                        a.ReleaseDate,
                        a.CoverImage,
                        a.Duration,
                        a.Genre,
                        ar.ArtistID,
                        CONCAT(u.FirstName, ' ', u.LastName) AS ArtistName
                    FROM Artwork a
                    JOIN Album alb ON alb.ArtworkID = a.ArtworkID
                    JOIN ReleaseTable rt ON rt.ArtworkID = a.ArtworkID
                    JOIN Artist ar ON ar.ArtistID = rt.ArtistID
                    JOIN User u ON u.UserID = ar.UserID
                    WHERE a.Genre LIKE %s
                    ORDER BY a.ReleaseDate DESC
                    LIMIT %s
                """
                genre_term = f"%{genre}%"
                cur.execute(sql, (genre_term, limit))
                rows = cur.fetchall()

                return [self.format_db_album(row) for row in rows]
        except Exception as e:
            print(f"Database error in get_albums_by_genre_from_db: {e}")
            return []
        finally:
            conn.close()

    def get_album_by_id_from_db(self, album_id: str) -> Optional[Dict]:
        """Get album by ID from database"""
        conn = get_db_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cur:
                sql = """
                    SELECT
                        alb.AlbumID,
                        alb.TotalTrack,
                        NULL as SingleID,
                        a.ArtworkID,
                        a.Title,
                        a.ReleaseDate,
                        a.CoverImage,
                        a.Duration,
                        a.Genre,
                        ar.ArtistID,
                        CONCAT(u.FirstName, ' ', u.LastName) AS ArtistName
                    FROM Artwork a
                    JOIN Album alb ON alb.ArtworkID = a.ArtworkID
                    JOIN ReleaseTable rt ON rt.ArtworkID = a.ArtworkID
                    JOIN Artist ar ON ar.ArtistID = rt.ArtistID
                    JOIN User u ON u.UserID = ar.UserID
                    WHERE alb.AlbumID = %s
                    LIMIT 1
                """
                cur.execute(sql, (album_id,))
                row = cur.fetchone()

                if row:
                    return self.format_db_album(row)
                return None
        except Exception as e:
            print(f"Database error in get_album_by_id_from_db: {e}")
            return None
        finally:
            conn.close()

    def get_album_tracks_from_db(self, album_id: str) -> Optional[List[Dict]]:
        """Get album tracks from database"""
        conn = get_db_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cur:
                sql = """
                    SELECT
                        s.SongID,
                        s.Title,
                        s.Duration,
                        s.AudioFile,
                        s.TrackNumber,
                        a.ArtworkID,
                        a.CoverImage,
                        a.Genre,
                        ar.ArtistID,
                        CONCAT(u.FirstName, ' ', u.LastName) AS ArtistName
                    FROM Song s
                    JOIN Contain c ON c.SongID = s.SongID
                    JOIN Album alb ON alb.AlbumID = c.AlbumID
                    JOIN Artwork a ON a.ArtworkID = alb.ArtworkID
                    JOIN ReleaseTable rt ON rt.ArtworkID = a.ArtworkID
                    JOIN Artist ar ON ar.ArtistID = rt.ArtistID
                    JOIN User u ON u.UserID = ar.UserID
                    WHERE alb.AlbumID = %s
                    ORDER BY s.TrackNumber
                """
                cur.execute(sql, (album_id,))
                rows = cur.fetchall()

                tracks = []
                for row in rows:
                    tracks.append({
                        'jamendo_id': str(row.get('SongID')),
                        'title': row.get('Title') or '',
                        'artist': row.get('ArtistName') or 'Unknown',
                        'duration': row.get('Duration') or 0,
                        'audio_url': self._resolve_s3_url(row.get('AudioFile')),
                        'image_url': self._resolve_s3_url(row.get('CoverImage')),
                        'track_number': row.get('TrackNumber') or 0,
                        'ArtworkID': row.get('ArtworkID'),
                        'ArtistID': row.get('ArtistID')
                    })

                return tracks
        except Exception as e:
            print(f"Database error in get_album_tracks_from_db: {e}")
            return []
        finally:
            conn.close()

    def search_albums(self, query: str, limit: int = 20, offset: int = 0, source: str = 'jamendo') -> Optional[List[Dict]]:
        """
        Search for albums from Jamendo API, database, or both

        Args:
            query: Search term (album name, artist name, etc.)
            limit: Number of results (default: 20, max: 100)
            offset: Pagination offset (default: 0)
            source: 'jamendo', 'db', or 'both' (default: 'jamendo')

        Returns:
            List of formatted album dictionaries or None if error
        """
        albums = []

        if source == 'db':
            # Only database
            return self.search_albums_from_db(query, limit, offset)

        elif source == 'both':
            # Both sources - database first, then Jamendo
            db_albums = self.search_albums_from_db(query, limit // 2, offset)
            if db_albums:
                albums.extend(db_albums)

            # Get remaining from Jamendo
            remaining_limit = limit - len(albums)
            if remaining_limit > 0:
                response = self.jamendo_service.search_albums(query, remaining_limit, offset)
                if response:
                    for album in response.get('results', []):
                        formatted_album = self.jamendo_service.format_album_response(album)
                        albums.append(formatted_album)

            return albums if albums else []

        else:
            # Default: Jamendo only
            response = self.jamendo_service.search_albums(query, limit, offset)

            if not response:
                return None

            for album in response.get('results', []):
                formatted_album = self.jamendo_service.format_album_response(album)
                albums.append(formatted_album)

            return albums
    
    def get_albums_by_genre(self, genre: str, limit: int = 20, source: str = 'jamendo') -> Optional[List[Dict]]:
        """
        Get albums by genre/tag from Jamendo API, database, or both

        Args:
            genre: Genre or tag name
            limit: Number of results (default: 20, max: 100)
            source: 'jamendo', 'db', or 'both' (default: 'jamendo')

        Returns:
            List of formatted album dictionaries or None if error
        """
        albums = []

        if source == 'db':
            # Only database
            return self.get_albums_by_genre_from_db(genre, limit)

        elif source == 'both':
            # Both sources - database first, then Jamendo
            db_albums = self.get_albums_by_genre_from_db(genre, limit // 2)
            if db_albums:
                albums.extend(db_albums)

            # Get remaining from Jamendo
            remaining_limit = limit - len(albums)
            if remaining_limit > 0:
                response = self.jamendo_service.get_albums_by_genre(genre, remaining_limit)
                if response:
                    for album in response.get('results', []):
                        formatted_album = self.jamendo_service.format_album_response(album)
                        albums.append(formatted_album)

            return albums if albums else []

        else:
            # Default: Jamendo only
            response = self.jamendo_service.get_albums_by_genre(genre, limit)

            if not response:
                return None

            for album in response.get('results', []):
                formatted_album = self.jamendo_service.format_album_response(album)
                albums.append(formatted_album)

            return albums
    
    def get_album_by_id(self, jamendo_id: str) -> Optional[Dict]:
        """
        Get a specific album by Jamendo ID or database ID

        Args:
            jamendo_id: Jamendo album ID or database album ID

        Returns:
            Formatted album dictionary or None if not found/error
        """
        # Try database first if ID looks numeric (database IDs are integers)
        try:
            int(jamendo_id)
            # It's a valid integer, try database first
            db_album = self.get_album_by_id_from_db(jamendo_id)
            if db_album:
                return db_album
        except (ValueError, TypeError):
            # Not a valid integer, skip database check
            pass

        # Fall back to Jamendo
        album = self.jamendo_service.get_album_by_id(jamendo_id)

        if not album:
            return None

        return self.jamendo_service.format_album_response(album)
    
    def get_album_tracks(self, jamendo_id: str) -> Optional[List[Dict]]:
        """
        Get all tracks within an album from database or Jamendo

        Args:
            jamendo_id: Jamendo album ID or database album ID

        Returns:
            List of formatted track dictionaries or None if error
        """
        # Try database first if ID looks numeric (database IDs are integers)
        try:
            int(jamendo_id)
            # It's a valid integer, try database first
            db_tracks = self.get_album_tracks_from_db(jamendo_id)
            if db_tracks:
                return db_tracks
        except (ValueError, TypeError):
            # Not a valid integer, skip database check
            pass

        # Fall back to Jamendo
        response = self.jamendo_service.get_album_tracks(jamendo_id)

        if not response:
            return None

        # Format the results
        tracks = []
        for track in response.get('results', []):
            formatted_track = self.jamendo_service.format_track_response(track)
            tracks.append(formatted_track)

        return tracks

    def get_album_by_artwork_id(self, artwork_id: int):
        """
        Get album information by ArtworkID from database

        Args:
            artwork_id: Artwork ID

        Returns:
            Formatted album dictionary or None if not found
        """
        conn = get_db_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cur:
                sql = """
                    SELECT
                        alb.AlbumID,
                        alb.TotalTrack,
                        a.ArtworkID,
                        a.Title,
                        a.ReleaseDate,
                        a.CoverImage,
                        a.Duration,
                        a.Genre,
                        ar.ArtistID,
                        CONCAT(u.FirstName, ' ', u.LastName) AS ArtistName
                    FROM Artwork a
                    JOIN Album alb ON alb.ArtworkID = a.ArtworkID
                    JOIN ReleaseTable rt ON rt.ArtworkID = a.ArtworkID
                    JOIN Artist ar ON ar.ArtistID = rt.ArtistID
                    JOIN User u ON u.UserID = ar.UserID
                    WHERE a.ArtworkID = %s
                    LIMIT 1
                """
                cur.execute(sql, (artwork_id,))
                row = cur.fetchone()

                if not row:
                    return None

                # Format album using standard format method
                return {
                    'jamendo_id': str(row.get('AlbumID')),
                    'title': row.get('Title') or '',
                    'artist': row.get('ArtistName') or 'Unknown',
                    'release_date': row.get('ReleaseDate').isoformat() if row.get('ReleaseDate') else None,
                    'image_url': self._resolve_s3_url(row.get('CoverImage')),
                    'track_count': row.get('TotalTrack') or 0,
                    'genre': row.get('Genre') or '',
                    'ArtworkID': row.get('ArtworkID'),
                    'ArtistID': row.get('ArtistID'),
                    'AlbumID': row.get('AlbumID')
                }

        finally:
            conn.close()
