"""
Song service layer for song operations
"""
import pymysql
from flask import current_app
from app.auth.utils import get_db_connection


class SongService:
    """Service class for song operations"""

    @staticmethod
    def get_artist_id(user_id):
        """
        Get artist ID from user ID

        Args:
            user_id (int): User's ID

        Returns:
            int or None: Artist ID if found, None otherwise
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            cursor.execute(
                "SELECT ArtistID FROM Artist WHERE UserID = %s",
                (user_id,)
            )
            artist = cursor.fetchone()

            return artist['ArtistID'] if artist else None

        except pymysql.Error:
            return None

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_all_songs(genre=None, artist_id=None, search=None, limit=50, offset=0):
        """
        Get all songs with optional filters

        Args:
            genre (str): Optional genre filter
            artist_id (int): Optional artist ID filter
            search (str): Optional search query (searches title, artwork title, artist username)
            limit (int): Number of records to return
            offset (int): Offset for pagination

        Returns:
            tuple: (success: bool, result: list/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Build query with filters
            query = """
                SELECT
                    s.SongID,
                    s.ArtworkID,
                    s.TrackNumber,
                    s.Title,
                    s.Duration,
                    s.AudioFileURL,
                    s.ReleaseDate,
                    a.Title as artwork_title,
                    a.Type as artwork_type,
                    a.Genre,
                    a.CoverImage,
                    ar.ArtistID,
                    u.UserID as artist_user_id,
                    u.Username as artist_username,
                    u.FirstName as artist_first_name,
                    u.LastName as artist_last_name
                FROM Song s
                JOIN Artwork a ON s.ArtworkID = a.ArtworkID
                JOIN Artist ar ON a.ArtistID = ar.ArtistID
                JOIN User u ON ar.UserID = u.UserID
                WHERE 1=1
            """
            params = []

            if genre:
                query += " AND a.Genre = %s"
                params.append(genre)

            if artist_id:
                query += " AND ar.ArtistID = %s"
                params.append(artist_id)

            if search:
                query += """ AND (
                    s.Title LIKE %s OR
                    a.Title LIKE %s OR
                    u.Username LIKE %s OR
                    CONCAT(u.FirstName, ' ', u.LastName) LIKE %s
                )"""
                search_pattern = f"%{search}%"
                params.extend([search_pattern, search_pattern, search_pattern, search_pattern])

            query += " ORDER BY s.ReleaseDate DESC, s.SongID DESC LIMIT %s OFFSET %s"
            params.extend([limit, offset])

            cursor.execute(query, tuple(params))
            songs = cursor.fetchall()

            return True, songs

        except pymysql.Error as e:
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_song_by_id(song_id):
        """
        Get song details by ID

        Args:
            song_id (int): Song's ID

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            query = """
                SELECT
                    s.SongID,
                    s.ArtworkID,
                    s.TrackNumber,
                    s.Title,
                    s.Duration,
                    s.AudioFileURL,
                    s.ReleaseDate,
                    a.Title as artwork_title,
                    a.Type as artwork_type,
                    a.Genre,
                    a.CoverImage,
                    a.ReleaseDate as artwork_release_date,
                    ar.ArtistID,
                    u.UserID as artist_user_id,
                    u.Username as artist_username,
                    u.FirstName as artist_first_name,
                    u.LastName as artist_last_name
                FROM Song s
                JOIN Artwork a ON s.ArtworkID = a.ArtworkID
                JOIN Artist ar ON a.ArtistID = ar.ArtistID
                JOIN User u ON ar.UserID = u.UserID
                WHERE s.SongID = %s
            """
            cursor.execute(query, (song_id,))
            song = cursor.fetchone()

            if not song:
                return False, "Song not found"

            return True, song

        except pymysql.Error as e:
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def create_song(user_id, artwork_id, title, track_number, duration, audio_file_url, release_date=None):
        """
        Create a new song (Artist only)

        Args:
            user_id (int): User's ID
            artwork_id (int): Artwork's ID
            title (str): Song title
            track_number (int): Track number
            duration (float): Duration in seconds
            audio_file_url (str): URL to audio file
            release_date (str): Optional release date (YYYY-MM-DD)

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Get artist ID
            artist_id = SongService.get_artist_id(user_id)
            if not artist_id:
                return False, "User is not an artist"

            # Verify artwork exists and belongs to this artist
            cursor.execute(
                "SELECT ArtistID FROM Artwork WHERE ArtworkID = %s",
                (artwork_id,)
            )
            artwork = cursor.fetchone()

            if not artwork:
                return False, "Artwork not found"

            if artwork['ArtistID'] != artist_id:
                return False, "You are not the owner of this artwork"

            # Check if track number already exists for this artwork
            cursor.execute(
                "SELECT SongID FROM Song WHERE ArtworkID = %s AND TrackNumber = %s",
                (artwork_id, track_number)
            )
            if cursor.fetchone():
                return False, f"Track number {track_number} already exists for this artwork"

            # Create song
            if release_date:
                cursor.execute(
                    """
                    INSERT INTO Song (ArtworkID, TrackNumber, Title, Duration, AudioFileURL, ReleaseDate)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (artwork_id, track_number, title, duration, audio_file_url, release_date)
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO Song (ArtworkID, TrackNumber, Title, Duration, AudioFileURL)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (artwork_id, track_number, title, duration, audio_file_url)
                )

            song_id = cursor.lastrowid
            connection.commit()

            # Fetch created song
            success, song = SongService.get_song_by_id(song_id)
            if not success:
                return False, "Song created but failed to retrieve details"

            return True, song

        except pymysql.Error as e:
            if connection:
                connection.rollback()
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def update_song(user_id, song_id, **updates):
        """
        Update song (Artist only, owner only)

        Args:
            user_id (int): User's ID
            song_id (int): Song's ID
            **updates: Fields to update (title, track_number, duration, audio_file_url, release_date)

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Get artist ID
            artist_id = SongService.get_artist_id(user_id)
            if not artist_id:
                return False, "User is not an artist"

            # Check if song exists and user is the owner (via artwork)
            cursor.execute(
                """
                SELECT s.ArtworkID, a.ArtistID
                FROM Song s
                JOIN Artwork a ON s.ArtworkID = a.ArtworkID
                WHERE s.SongID = %s
                """,
                (song_id,)
            )
            song = cursor.fetchone()

            if not song:
                return False, "Song not found"

            if song['ArtistID'] != artist_id:
                return False, "You are not the owner of this song"

            # Build update query dynamically
            update_fields = []
            params = []

            if 'title' in updates:
                update_fields.append("Title = %s")
                params.append(updates['title'])

            if 'track_number' in updates:
                # Check if new track number already exists for this artwork
                cursor.execute(
                    "SELECT SongID FROM Song WHERE ArtworkID = %s AND TrackNumber = %s AND SongID != %s",
                    (song['ArtworkID'], updates['track_number'], song_id)
                )
                if cursor.fetchone():
                    return False, f"Track number {updates['track_number']} already exists for this artwork"

                update_fields.append("TrackNumber = %s")
                params.append(updates['track_number'])

            if 'duration' in updates:
                update_fields.append("Duration = %s")
                params.append(updates['duration'])

            if 'audio_file_url' in updates:
                update_fields.append("AudioFileURL = %s")
                params.append(updates['audio_file_url'])

            if 'release_date' in updates:
                update_fields.append("ReleaseDate = %s")
                params.append(updates['release_date'])

            if not update_fields:
                return False, "No valid fields to update"

            # Execute update
            query = f"UPDATE Song SET {', '.join(update_fields)} WHERE SongID = %s"
            params.append(song_id)
            cursor.execute(query, tuple(params))
            connection.commit()

            # Fetch updated song
            success, updated_song = SongService.get_song_by_id(song_id)
            if not success:
                return False, "Song updated but failed to retrieve details"

            return True, updated_song

        except pymysql.Error as e:
            if connection:
                connection.rollback()
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def delete_song(user_id, song_id):
        """
        Delete song (Artist only, owner only)

        Args:
            user_id (int): User's ID
            song_id (int): Song's ID

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Get artist ID
            artist_id = SongService.get_artist_id(user_id)
            if not artist_id:
                return False, "User is not an artist"

            # Check if song exists and user is the owner (via artwork)
            cursor.execute(
                """
                SELECT s.SongID, a.ArtistID
                FROM Song s
                JOIN Artwork a ON s.ArtworkID = a.ArtworkID
                WHERE s.SongID = %s
                """,
                (song_id,)
            )
            song = cursor.fetchone()

            if not song:
                return False, "Song not found"

            if song['ArtistID'] != artist_id:
                return False, "You are not the owner of this song"

            # Delete song (CASCADE will delete related records)
            cursor.execute("DELETE FROM Song WHERE SongID = %s", (song_id,))
            connection.commit()

            return True, {'message': 'Song deleted successfully'}

        except pymysql.Error as e:
            if connection:
                connection.rollback()
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()
