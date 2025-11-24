"""
Artwork service layer for artwork operations
"""
import pymysql
from flask import current_app
from app.auth.utils import get_db_connection


class ArtworkService:
    """Service class for artwork operations"""

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
    def get_all_artworks(artist_id=None, genre=None, artwork_type=None, search=None, limit=50, offset=0):
        """
        Get all artworks with optional filters

        Args:
            artist_id (int): Optional artist ID to filter by
            genre (str): Optional genre to filter by
            artwork_type (str): Optional type ('Album' or 'Single')
            search (str): Optional search term for title
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
                    a.ArtworkID,
                    a.ArtistID,
                    a.Title,
                    a.Genre,
                    a.Duration,
                    a.TotalLike,
                    a.ReleaseDate,
                    a.CoverImage,
                    a.Type,
                    a.CreatedAt,
                    ar.ArtistID,
                    u.UserID,
                    u.Username as artist_username,
                    u.FirstName as artist_first_name,
                    u.LastName as artist_last_name,
                    al.Total_track,
                    (SELECT COUNT(*) FROM Song s WHERE s.ArtworkID = a.ArtworkID) as song_count
                FROM Artwork a
                JOIN Artist ar ON a.ArtistID = ar.ArtistID
                JOIN User u ON ar.UserID = u.UserID
                LEFT JOIN Album al ON a.ArtworkID = al.AlbumID
                WHERE 1=1
            """
            params = []

            if artist_id:
                query += " AND a.ArtistID = %s"
                params.append(artist_id)

            if genre:
                query += " AND a.Genre = %s"
                params.append(genre)

            if artwork_type:
                query += " AND a.Type = %s"
                params.append(artwork_type)

            if search:
                query += " AND a.Title LIKE %s"
                params.append(f"%{search}%")

            query += " ORDER BY a.CreatedAt DESC LIMIT %s OFFSET %s"
            params.extend([limit, offset])

            cursor.execute(query, params)
            artworks = cursor.fetchall()

            return True, artworks

        except pymysql.Error as e:
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_artwork_by_id(artwork_id):
        """
        Get artwork details by ID

        Args:
            artwork_id (int): Artwork's ID

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Get artwork details
            query = """
                SELECT
                    a.ArtworkID,
                    a.ArtistID,
                    a.Title,
                    a.Genre,
                    a.Duration,
                    a.TotalLike,
                    a.ReleaseDate,
                    a.CoverImage,
                    a.Type,
                    a.CreatedAt,
                    ar.ArtistID,
                    u.UserID as artist_user_id,
                    u.Username as artist_username,
                    u.FirstName as artist_first_name,
                    u.LastName as artist_last_name,
                    al.Total_track,
                    s.SingleID
                FROM Artwork a
                JOIN Artist ar ON a.ArtistID = ar.ArtistID
                JOIN User u ON ar.UserID = u.UserID
                LEFT JOIN Album al ON a.ArtworkID = al.AlbumID
                LEFT JOIN Single s ON a.ArtworkID = s.SingleID
                WHERE a.ArtworkID = %s
            """
            cursor.execute(query, (artwork_id,))
            artwork = cursor.fetchone()

            if not artwork:
                return False, "Artwork not found"

            # Get songs in artwork
            songs_query = """
                SELECT
                    s.SongID,
                    s.Title,
                    s.Duration,
                    s.ReleaseDate,
                    s.TrackNumber,
                    s.AudioFile,
                    s.CreatedAt
                FROM Song s
                WHERE s.ArtworkID = %s
                ORDER BY s.TrackNumber ASC
            """
            cursor.execute(songs_query, (artwork_id,))
            songs = cursor.fetchall()

            # Build response
            result = {
                'artwork_id': artwork['ArtworkID'],
                'artist_id': artwork['ArtistID'],
                'title': artwork['Title'],
                'genre': artwork['Genre'],
                'duration': artwork['Duration'],
                'total_like': artwork['TotalLike'],
                'release_date': artwork['ReleaseDate'],
                'cover_image': artwork['CoverImage'],
                'type': artwork['Type'],
                'created_at': artwork['CreatedAt'],
                'artist': {
                    'artist_id': artwork['ArtistID'],
                    'user_id': artwork['artist_user_id'],
                    'username': artwork['artist_username'],
                    'first_name': artwork['artist_first_name'],
                    'last_name': artwork['artist_last_name']
                },
                'songs': songs,
                'song_count': len(songs)
            }

            if artwork['Type'] == 'Album':
                result['total_track'] = artwork['Total_track']

            return True, result

        except pymysql.Error as e:
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_artwork_songs(artwork_id):
        """
        Get all songs in an artwork

        Args:
            artwork_id (int): Artwork's ID

        Returns:
            tuple: (success: bool, result: list/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Verify artwork exists
            cursor.execute("SELECT ArtworkID, Title, Type FROM Artwork WHERE ArtworkID = %s", (artwork_id,))
            artwork = cursor.fetchone()

            if not artwork:
                return False, "Artwork not found"

            # Get songs
            query = """
                SELECT
                    s.SongID,
                    s.ArtworkID,
                    s.Title,
                    s.Duration,
                    s.ReleaseDate,
                    s.TrackNumber,
                    s.AudioFile,
                    s.CreatedAt
                FROM Song s
                WHERE s.ArtworkID = %s
                ORDER BY s.TrackNumber ASC
            """
            cursor.execute(query, (artwork_id,))
            songs = cursor.fetchall()

            return True, {
                'artwork_id': artwork['ArtworkID'],
                'artwork_title': artwork['Title'],
                'artwork_type': artwork['Type'],
                'songs': songs,
                'song_count': len(songs)
            }

        except pymysql.Error as e:
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def create_artwork(user_id, title, artwork_type, genre=None, release_date=None, cover_image=None):
        """
        Create a new artwork (album or single) - Artist only

        Args:
            user_id (int): User's ID
            title (str): Artwork title
            artwork_type (str): 'Album' or 'Single'
            genre (str): Optional genre
            release_date (str): Optional release date
            cover_image (str): Optional cover image URL

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Get artist ID
            artist_id = ArtworkService.get_artist_id(user_id)
            if not artist_id:
                return False, "User is not an artist"

            # Create Artwork record first
            cursor.execute(
                """
                INSERT INTO Artwork (ArtistID, Title, Genre, ReleaseDate, CoverImage, Type)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (artist_id, title, genre, release_date, cover_image, artwork_type)
            )
            artwork_id = cursor.lastrowid

            # Create Album or Single record
            if artwork_type == 'Album':
                cursor.execute(
                    "INSERT INTO Album (AlbumID, Total_track) VALUES (%s, %s)",
                    (artwork_id, 0)  # Initially 0 tracks, will be updated when songs are added
                )
            elif artwork_type == 'Single':
                cursor.execute(
                    "INSERT INTO Single (SingleID) VALUES (%s)",
                    (artwork_id,)
                )

            connection.commit()

            # Fetch created artwork
            cursor.execute(
                """
                SELECT
                    a.ArtworkID,
                    a.ArtistID,
                    a.Title,
                    a.Genre,
                    a.Duration,
                    a.TotalLike,
                    a.ReleaseDate,
                    a.CoverImage,
                    a.Type,
                    a.CreatedAt,
                    u.Username as artist_username,
                    al.Total_track
                FROM Artwork a
                JOIN Artist ar ON a.ArtistID = ar.ArtistID
                JOIN User u ON ar.UserID = u.UserID
                LEFT JOIN Album al ON a.ArtworkID = al.AlbumID
                WHERE a.ArtworkID = %s
                """,
                (artwork_id,)
            )
            artwork = cursor.fetchone()

            return True, artwork

        except pymysql.Error as e:
            if connection:
                connection.rollback()
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def update_artwork(user_id, artwork_id, title=None, genre=None, cover_image=None, release_date=None):
        """
        Update artwork - Artist only, owner only

        Args:
            user_id (int): User's ID
            artwork_id (int): Artwork's ID
            title (str): Optional new title
            genre (str): Optional new genre
            cover_image (str): Optional new cover image
            release_date (str): Optional new release date

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Get artist ID
            artist_id = ArtworkService.get_artist_id(user_id)
            if not artist_id:
                return False, "User is not an artist"

            # Check if artwork exists and user is owner
            cursor.execute(
                "SELECT ArtistID FROM Artwork WHERE ArtworkID = %s",
                (artwork_id,)
            )
            artwork = cursor.fetchone()

            if not artwork:
                return False, "Artwork not found"

            if artwork['ArtistID'] != artist_id:
                return False, "You are not the owner of this artwork"

            # Build update query
            update_fields = []
            params = []

            if title is not None:
                update_fields.append("Title = %s")
                params.append(title)

            if genre is not None:
                update_fields.append("Genre = %s")
                params.append(genre)

            if cover_image is not None:
                update_fields.append("CoverImage = %s")
                params.append(cover_image)

            if release_date is not None:
                update_fields.append("ReleaseDate = %s")
                params.append(release_date)

            if not update_fields:
                return False, "No fields to update"

            params.append(artwork_id)
            query = f"UPDATE Artwork SET {', '.join(update_fields)} WHERE ArtworkID = %s"
            cursor.execute(query, params)
            connection.commit()

            # Fetch updated artwork
            cursor.execute(
                """
                SELECT
                    a.ArtworkID,
                    a.ArtistID,
                    a.Title,
                    a.Genre,
                    a.Duration,
                    a.TotalLike,
                    a.ReleaseDate,
                    a.CoverImage,
                    a.Type,
                    a.CreatedAt,
                    u.Username as artist_username,
                    al.Total_track
                FROM Artwork a
                JOIN Artist ar ON a.ArtistID = ar.ArtistID
                JOIN User u ON ar.UserID = u.UserID
                LEFT JOIN Album al ON a.ArtworkID = al.AlbumID
                WHERE a.ArtworkID = %s
                """,
                (artwork_id,)
            )
            updated_artwork = cursor.fetchone()

            return True, updated_artwork

        except pymysql.Error as e:
            if connection:
                connection.rollback()
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def delete_artwork(user_id, artwork_id):
        """
        Delete artwork - Artist only, owner only

        Args:
            user_id (int): User's ID
            artwork_id (int): Artwork's ID

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Get artist ID
            artist_id = ArtworkService.get_artist_id(user_id)
            if not artist_id:
                return False, "User is not an artist"

            # Check if artwork exists and user is owner
            cursor.execute(
                "SELECT ArtistID, Type FROM Artwork WHERE ArtworkID = %s",
                (artwork_id,)
            )
            artwork = cursor.fetchone()

            if not artwork:
                return False, "Artwork not found"

            if artwork['ArtistID'] != artist_id:
                return False, "You are not the owner of this artwork"

            # Delete Album or Single record first (due to foreign key constraints)
            if artwork['Type'] == 'Album':
                cursor.execute("DELETE FROM Album WHERE AlbumID = %s", (artwork_id,))
            elif artwork['Type'] == 'Single':
                cursor.execute("DELETE FROM Single WHERE SingleID = %s", (artwork_id,))

            # Delete Artwork (CASCADE will delete related songs, reactions, etc.)
            cursor.execute("DELETE FROM Artwork WHERE ArtworkID = %s", (artwork_id,))
            connection.commit()

            return True, {'message': 'Artwork deleted successfully'}

        except pymysql.Error as e:
            if connection:
                connection.rollback()
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def update_total_track(artwork_id):
        """
        Update Total_track for an album based on the number of songs

        Args:
            artwork_id (int): Artwork's ID

        Returns:
            tuple: (success: bool, result: str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Count songs in the artwork
            cursor.execute(
                "SELECT COUNT(*) as count FROM Song WHERE ArtworkID = %s",
                (artwork_id,)
            )
            result = cursor.fetchone()
            song_count = result['count']

            # Update Total_track in Album table
            cursor.execute(
                "UPDATE Album SET Total_track = %s WHERE AlbumID = %s",
                (song_count, artwork_id)
            )
            connection.commit()

            return True, f"Total track updated to {song_count}"

        except pymysql.Error as e:
            if connection:
                connection.rollback()
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def update_total_duration(artwork_id):
        """
        Update total duration for an artwork based on the sum of song durations

        Args:
            artwork_id (int): Artwork's ID

        Returns:
            tuple: (success: bool, result: str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Calculate total duration
            cursor.execute(
                "SELECT SUM(Duration) as total_duration FROM Song WHERE ArtworkID = %s",
                (artwork_id,)
            )
            result = cursor.fetchone()
            total_duration = result['total_duration'] if result['total_duration'] else 0

            # Update Duration in Artwork table
            cursor.execute(
                "UPDATE Artwork SET Duration = %s WHERE ArtworkID = %s",
                (total_duration, artwork_id)
            )
            connection.commit()

            return True, f"Total duration updated to {total_duration}"

        except pymysql.Error as e:
            if connection:
                connection.rollback()
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()
