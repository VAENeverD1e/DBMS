"""
Artist service layer for artist operations
"""
import pymysql
from flask import current_app
from app.auth.utils import get_db_connection


class ArtistService:
    """Service class for artist operations"""

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
    def get_all_artists(genre=None, verified=None, search=None, limit=50, offset=0):
        """
        Get all artists with optional filters

        Args:
            genre (str): Optional genre filter
            verified (str): Optional verified status filter ('Verified', 'Pending', 'Unverified')
            search (str): Optional search term for artist username or name
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
                    a.ArtistID,
                    a.UserID,
                    a.Genre,
                    a.VerifiedStatus,
                    a.TotalFollowers,
                    a.SMLinks,
                    a.CreatedAt,
                    u.Username,
                    u.FirstName,
                    u.LastName,
                    u.Email
                FROM Artist a
                JOIN User u ON a.UserID = u.UserID
                WHERE 1=1
            """
            params = []

            # Add filters
            if genre:
                query += " AND a.Genre = %s"
                params.append(genre)

            if verified:
                query += " AND a.VerifiedStatus = %s"
                params.append(verified)

            if search:
                query += " AND (u.Username LIKE %s OR u.FirstName LIKE %s OR u.LastName LIKE %s)"
                search_pattern = f"%{search}%"
                params.extend([search_pattern, search_pattern, search_pattern])

            # Add ordering and pagination
            query += " ORDER BY a.TotalFollowers DESC, a.CreatedAt DESC LIMIT %s OFFSET %s"
            params.extend([limit, offset])

            cursor.execute(query, params)
            artists = cursor.fetchall()

            return True, artists

        except pymysql.Error as e:
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_artist_by_id(artist_id):
        """
        Get artist details by artist ID

        Args:
            artist_id (int): Artist's ID

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Get artist details with user info
            query = """
                SELECT
                    a.ArtistID,
                    a.UserID,
                    a.Genre,
                    a.VerifiedStatus,
                    a.TotalFollowers,
                    a.SMLinks,
                    a.CreatedAt,
                    u.Username,
                    u.FirstName,
                    u.LastName,
                    u.Email
                FROM Artist a
                JOIN User u ON a.UserID = u.UserID
                WHERE a.ArtistID = %s
            """
            cursor.execute(query, (artist_id,))
            artist = cursor.fetchone()

            if not artist:
                return False, "Artist not found"

            return True, artist

        except pymysql.Error as e:
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_artist_artworks(artist_id, limit=50, offset=0):
        """
        Get artworks created by an artist

        Args:
            artist_id (int): Artist's ID
            limit (int): Number of records to return
            offset (int): Offset for pagination

        Returns:
            tuple: (success: bool, result: list/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Verify artist exists
            cursor.execute("SELECT ArtistID FROM Artist WHERE ArtistID = %s", (artist_id,))
            if not cursor.fetchone():
                return False, "Artist not found"

            # Get artworks
            query = """
                SELECT
                    a.ArtworkID,
                    a.Title,
                    a.Genre,
                    a.ReleaseDate,
                    a.Duration,
                    a.TotalLike,
                    a.CoverImage,
                    a.Type,
                    COUNT(DISTINCT s.SongID) as song_count
                FROM Artwork a
                LEFT JOIN Song s ON a.ArtworkID = s.ArtworkID
                WHERE a.ArtistID = %s
                GROUP BY a.ArtworkID, a.Title, a.Genre, a.ReleaseDate, a.Duration, a.TotalLike, a.CoverImage, a.Type
                ORDER BY a.ReleaseDate DESC
                LIMIT %s OFFSET %s
            """
            cursor.execute(query, (artist_id, limit, offset))
            artworks = cursor.fetchall()

            return True, artworks

        except pymysql.Error as e:
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_artist_stats(artist_id):
        """
        Get artist statistics (followers, artworks count, total likes)

        Args:
            artist_id (int): Artist's ID

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Get artist info
            cursor.execute(
                "SELECT ArtistID, TotalFollowers FROM Artist WHERE ArtistID = %s",
                (artist_id,)
            )
            artist = cursor.fetchone()

            if not artist:
                return False, "Artist not found"

            stats = {
                'artist_id': artist['ArtistID'],
                'followers_count': artist['TotalFollowers'] if artist['TotalFollowers'] else 0
            }

            # Count artworks
            cursor.execute(
                "SELECT COUNT(*) as artwork_count FROM Artwork WHERE ArtistID = %s",
                (artist_id,)
            )
            result = cursor.fetchone()
            stats['artwork_count'] = result['artwork_count'] if result else 0

            # Get total likes across all artworks
            cursor.execute(
                "SELECT SUM(TotalLike) as total_likes FROM Artwork WHERE ArtistID = %s",
                (artist_id,)
            )
            result = cursor.fetchone()
            stats['total_likes'] = result['total_likes'] if result and result['total_likes'] else 0

            # Count total songs
            cursor.execute(
                """
                SELECT COUNT(DISTINCT s.SongID) as song_count
                FROM Song s
                JOIN Artwork a ON s.ArtworkID = a.ArtworkID
                WHERE a.ArtistID = %s
                """,
                (artist_id,)
            )
            result = cursor.fetchone()
            stats['song_count'] = result['song_count'] if result else 0

            return True, stats

        except pymysql.Error as e:
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def update_artist_profile(user_id, genre=None):
        """
        Update artist profile (genre)

        Args:
            user_id (int): User's ID
            genre (str): Genre (optional)

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Get artist ID
            artist_id = ArtistService.get_artist_id(user_id)
            if not artist_id:
                return False, "User is not an artist"

            # Build update query
            update_fields = []
            values = []

            if genre is not None:
                update_fields.append("Genre = %s")
                values.append(genre)

            if not update_fields:
                return False, "No fields to update"

            values.append(artist_id)
            update_query = f"UPDATE Artist SET {', '.join(update_fields)} WHERE ArtistID = %s"
            cursor.execute(update_query, values)
            connection.commit()

            # Fetch updated data
            query = """
                SELECT
                    a.ArtistID,
                    a.UserID,
                    a.Genre,
                    a.VerifiedStatus,
                    a.TotalFollowers,
                    a.SMLinks,
                    a.CreatedAt
                FROM Artist a
                WHERE a.ArtistID = %s
            """
            cursor.execute(query, (artist_id,))
            updated_artist = cursor.fetchone()

            return True, updated_artist

        except pymysql.Error as e:
            if connection:
                connection.rollback()
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def update_social_links(user_id, social_links):
        """
        Update artist social media links

        Args:
            user_id (int): User's ID
            social_links (str): Social media links

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Get artist ID
            artist_id = ArtistService.get_artist_id(user_id)
            if not artist_id:
                return False, "User is not an artist"

            # Update social links
            cursor.execute(
                "UPDATE Artist SET SMLinks = %s WHERE ArtistID = %s",
                (social_links, artist_id)
            )
            connection.commit()

            # Fetch updated data
            query = """
                SELECT
                    a.ArtistID,
                    a.UserID,
                    a.Genre,
                    a.VerifiedStatus,
                    a.TotalFollowers,
                    a.SMLinks,
                    a.CreatedAt
                FROM Artist a
                WHERE a.ArtistID = %s
            """
            cursor.execute(query, (artist_id,))
            updated_artist = cursor.fetchone()

            return True, updated_artist

        except pymysql.Error as e:
            if connection:
                connection.rollback()
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()
