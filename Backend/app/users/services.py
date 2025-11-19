"""
User service layer for user-specific operations
"""
import pymysql
from flask import current_app
from app.auth.utils import get_db_connection


class UserService:
    """Service class for user operations"""

    @staticmethod
    def upgrade_user_role(user_id, new_role):
        """
        Upgrade user role from Guest to Listener or Artist
        This is called after successful subscription payment

        Args:
            user_id (int): User's ID
            new_role (str): New role ('Listener' or 'Artist')

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Get current user role
            cursor.execute("SELECT Role FROM User WHERE UserID = %s", (user_id,))
            user = cursor.fetchone()

            if not user:
                return False, "User not found"

            current_role = user['Role']

            # Validate role transition
            if current_role == new_role:
                return False, f"User already has {new_role} role"

            if current_role not in ['Guest', 'Listener', 'Artist']:
                return False, "Invalid current role"

            if new_role not in ['Listener', 'Artist']:
                return False, "Invalid new role. Must be 'Listener' or 'Artist'"

            # Update user role
            cursor.execute(
                "UPDATE User SET Role = %s WHERE UserID = %s",
                (new_role, user_id)
            )

            # Create corresponding role-specific record
            if new_role == 'Listener':
                # Check if Listener record already exists
                cursor.execute("SELECT ListenerID FROM Listener WHERE UserID = %s", (user_id,))
                if not cursor.fetchone():
                    cursor.execute("INSERT INTO Listener (UserID) VALUES (%s)", (user_id,))
            elif new_role == 'Artist':
                # Check if Artist record already exists
                cursor.execute("SELECT ArtistID FROM Artist WHERE UserID = %s", (user_id,))
                if not cursor.fetchone():
                    cursor.execute(
                        "INSERT INTO Artist (UserID, VerifiedStatus) VALUES (%s, 'Pending')",
                        (user_id,)
                    )

            connection.commit()

            # Fetch updated user info
            cursor.execute(
                "SELECT UserID, Email, Username, FirstName, LastName, Role FROM User WHERE UserID = %s",
                (user_id,)
            )
            updated_user = cursor.fetchone()

            return True, updated_user

        except pymysql.Error as e:
            if connection:
                connection.rollback()
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_user_stats(user_id):
        """
        Get user statistics (playlists count, followers, following, etc.)

        Args:
            user_id (int): User's ID

        Returns:
            dict: User statistics or None
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Get user role
            cursor.execute("SELECT Role FROM User WHERE UserID = %s", (user_id,))
            user = cursor.fetchone()

            if not user:
                return None

            stats = {'role': user['Role']}

            # Role-specific statistics
            if user['Role'] == 'Listener':
                cursor.execute("SELECT ListenerID FROM Listener WHERE UserID = %s", (user_id,))
                listener = cursor.fetchone()

                if listener:
                    listener_id = listener['ListenerID']

                    # Count playlists
                    cursor.execute(
                        "SELECT COUNT(*) as playlist_count FROM Playlist WHERE ListenerID = %s",
                        (listener_id,)
                    )
                    stats['playlist_count'] = cursor.fetchone()['playlist_count']

                    # Count following artists
                    cursor.execute(
                        "SELECT COUNT(*) as following_count FROM Follow WHERE ListenerID = %s",
                        (listener_id,)
                    )
                    stats['following_count'] = cursor.fetchone()['following_count']

                    # Count reactions
                    cursor.execute(
                        "SELECT COUNT(*) as reaction_count FROM Reaction WHERE ListenerID = %s",
                        (listener_id,)
                    )
                    stats['reaction_count'] = cursor.fetchone()['reaction_count']

            elif user['Role'] == 'Artist':
                cursor.execute("SELECT ArtistID FROM Artist WHERE UserID = %s", (user_id,))
                artist = cursor.fetchone()

                if artist:
                    artist_id = artist['ArtistID']

                    # Count artworks
                    cursor.execute(
                        "SELECT COUNT(*) as artwork_count FROM Artwork WHERE ArtistID = %s",
                        (artist_id,)
                    )
                    stats['artwork_count'] = cursor.fetchone()['artwork_count']

                    # Get followers count
                    cursor.execute(
                        "SELECT TotalFollowers FROM Artist WHERE ArtistID = %s",
                        (artist_id,)
                    )
                    result = cursor.fetchone()
                    stats['followers_count'] = result['TotalFollowers'] if result else 0

            return stats

        except pymysql.Error:
            return None

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def update_listener_preferences(user_id, preference=None, favorite_genre=None):
        """
        Update listener preferences

        Args:
            user_id (int): User's ID
            preference (str): User preference (optional)
            favorite_genre (str): Favorite genre (optional)

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Get listener ID
            cursor.execute(
                "SELECT ListenerID FROM Listener WHERE UserID = %s",
                (user_id,)
            )
            listener = cursor.fetchone()

            if not listener:
                return False, "User is not a listener"

            listener_id = listener['ListenerID']

            # Build update query
            update_fields = []
            values = []

            if preference is not None:
                update_fields.append("Preference = %s")
                values.append(preference)

            if favorite_genre is not None:
                update_fields.append("FavoriteGenre = %s")
                values.append(favorite_genre)

            if not update_fields:
                return False, "No fields to update"

            values.append(listener_id)
            update_query = f"UPDATE Listener SET {', '.join(update_fields)} WHERE ListenerID = %s"
            cursor.execute(update_query, values)
            connection.commit()

            # Fetch updated data
            cursor.execute(
                "SELECT ListenerID, Preference, FavoriteGenre FROM Listener WHERE ListenerID = %s",
                (listener_id,)
            )
            updated_listener = cursor.fetchone()

            return True, updated_listener

        except pymysql.Error as e:
            if connection:
                connection.rollback()
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_play_history(user_id, limit=50, offset=0):
        """
        Get user's play history (for listeners only)

        Args:
            user_id (int): User's ID
            limit (int): Number of records to return
            offset (int): Offset for pagination

        Returns:
            tuple: (success: bool, result: list/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Get listener ID
            cursor.execute(
                "SELECT ListenerID FROM Listener WHERE UserID = %s",
                (user_id,)
            )
            listener = cursor.fetchone()

            if not listener:
                return False, "User is not a listener"

            listener_id = listener['ListenerID']

            # Get play history
            query = """
                SELECT
                    ph.HistoryID,
                    ph.SongID,
                    ph.PlayedAt,
                    ph.ListenDuration,
                    s.Title as song_title,
                    s.Duration as song_duration,
                    a.ArtworkID,
                    a.Title as artwork_title,
                    u.Username as artist_username
                FROM PlayHistory ph
                JOIN Song s ON ph.SongID = s.SongID
                JOIN Artwork a ON s.ArtworkID = a.ArtworkID
                JOIN Artist ar ON a.ArtistID = ar.ArtistID
                JOIN User u ON ar.UserID = u.UserID
                WHERE ph.ListenerID = %s
                ORDER BY ph.PlayedAt DESC
                LIMIT %s OFFSET %s
            """
            cursor.execute(query, (listener_id, limit, offset))
            history = cursor.fetchall()

            return True, history

        except pymysql.Error as e:
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def record_play_history(user_id, song_id, listen_duration):
        """
        Record a song play in user's history (for listeners only)

        Args:
            user_id (int): User's ID
            song_id (int): Song's ID
            listen_duration (int): Duration listened in seconds

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Get listener ID
            cursor.execute(
                "SELECT ListenerID FROM Listener WHERE UserID = %s",
                (user_id,)
            )
            listener = cursor.fetchone()

            if not listener:
                return False, "User is not a listener"

            listener_id = listener['ListenerID']

            # Insert play history record
            cursor.execute(
                """
                INSERT INTO PlayHistory (ListenerID, SongID, ListenDuration)
                VALUES (%s, %s, %s)
                """,
                (listener_id, song_id, listen_duration)
            )
            history_id = cursor.lastrowid
            connection.commit()

            return True, {'history_id': history_id, 'message': 'Play history recorded'}

        except pymysql.Error as e:
            if connection:
                connection.rollback()
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_following_artists(user_id, limit=50, offset=0):
        """
        Get list of artists the user is following (for listeners only)

        Args:
            user_id (int): User's ID
            limit (int): Number of records to return
            offset (int): Offset for pagination

        Returns:
            tuple: (success: bool, result: list/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Get listener ID
            cursor.execute(
                "SELECT ListenerID FROM Listener WHERE UserID = %s",
                (user_id,)
            )
            listener = cursor.fetchone()

            if not listener:
                return False, "User is not a listener"

            listener_id = listener['ListenerID']

            # Get following artists
            query = """
                SELECT
                    f.FollowID,
                    f.FollowedDate,
                    a.ArtistID,
                    a.Genre,
                    a.VerifiedStatus,
                    a.TotalFollowers,
                    u.UserID,
                    u.Username,
                    u.FirstName,
                    u.LastName
                FROM Follow f
                JOIN Artist a ON f.ArtistID = a.ArtistID
                JOIN User u ON a.UserID = u.UserID
                WHERE f.ListenerID = %s
                ORDER BY f.FollowedDate DESC
                LIMIT %s OFFSET %s
            """
            cursor.execute(query, (listener_id, limit, offset))
            artists = cursor.fetchall()

            return True, artists

        except pymysql.Error as e:
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def follow_artist(user_id, artist_id):
        """
        Follow an artist (for listeners only)

        Args:
            user_id (int): User's ID
            artist_id (int): Artist's ID

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Get listener ID
            cursor.execute(
                "SELECT ListenerID FROM Listener WHERE UserID = %s",
                (user_id,)
            )
            listener = cursor.fetchone()

            if not listener:
                return False, "User is not a listener"

            listener_id = listener['ListenerID']

            # Check if artist exists
            cursor.execute("SELECT ArtistID FROM Artist WHERE ArtistID = %s", (artist_id,))
            if not cursor.fetchone():
                return False, "Artist not found"

            # Check if already following
            cursor.execute(
                "SELECT FollowID FROM Follow WHERE ListenerID = %s AND ArtistID = %s",
                (listener_id, artist_id)
            )
            if cursor.fetchone():
                return False, "Already following this artist"

            # Create follow record
            cursor.execute(
                "INSERT INTO Follow (ListenerID, ArtistID) VALUES (%s, %s)",
                (listener_id, artist_id)
            )

            # Update artist's follower count
            cursor.execute(
                """
                UPDATE Artist
                SET TotalFollowers = COALESCE(TotalFollowers, 0) + 1
                WHERE ArtistID = %s
                """,
                (artist_id,)
            )

            connection.commit()

            return True, {'message': 'Successfully followed artist'}

        except pymysql.Error as e:
            if connection:
                connection.rollback()
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def unfollow_artist(user_id, artist_id):
        """
        Unfollow an artist (for listeners only)

        Args:
            user_id (int): User's ID
            artist_id (int): Artist's ID

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Get listener ID
            cursor.execute(
                "SELECT ListenerID FROM Listener WHERE UserID = %s",
                (user_id,)
            )
            listener = cursor.fetchone()

            if not listener:
                return False, "User is not a listener"

            listener_id = listener['ListenerID']

            # Check if following
            cursor.execute(
                "SELECT FollowID FROM Follow WHERE ListenerID = %s AND ArtistID = %s",
                (listener_id, artist_id)
            )
            if not cursor.fetchone():
                return False, "Not following this artist"

            # Delete follow record
            cursor.execute(
                "DELETE FROM Follow WHERE ListenerID = %s AND ArtistID = %s",
                (listener_id, artist_id)
            )

            # Update artist's follower count
            cursor.execute(
                """
                UPDATE Artist
                SET TotalFollowers = GREATEST(COALESCE(TotalFollowers, 0) - 1, 0)
                WHERE ArtistID = %s
                """,
                (artist_id,)
            )

            connection.commit()

            return True, {'message': 'Successfully unfollowed artist'}

        except pymysql.Error as e:
            if connection:
                connection.rollback()
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_user_reactions(user_id, reactable_type=None, limit=50, offset=0):
        """
        Get user's reactions (liked songs/albums) - for listeners only

        Args:
            user_id (int): User's ID
            reactable_type (str): Filter by type ('Song' or 'Artwork'), optional
            limit (int): Number of records to return
            offset (int): Offset for pagination

        Returns:
            tuple: (success: bool, result: list/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Get listener ID
            cursor.execute(
                "SELECT ListenerID FROM Listener WHERE UserID = %s",
                (user_id,)
            )
            listener = cursor.fetchone()

            if not listener:
                return False, "User is not a listener"

            listener_id = listener['ListenerID']

            # Build query based on reactable_type
            if reactable_type:
                query = """
                    SELECT
                        ReactionID,
                        ReactableType,
                        ReactableID,
                        Emotion,
                        ReactedAt
                    FROM Reaction
                    WHERE ListenerID = %s AND ReactableType = %s
                    ORDER BY ReactedAt DESC
                    LIMIT %s OFFSET %s
                """
                cursor.execute(query, (listener_id, reactable_type, limit, offset))
            else:
                query = """
                    SELECT
                        ReactionID,
                        ReactableType,
                        ReactableID,
                        Emotion,
                        ReactedAt
                    FROM Reaction
                    WHERE ListenerID = %s
                    ORDER BY ReactedAt DESC
                    LIMIT %s OFFSET %s
                """
                cursor.execute(query, (listener_id, limit, offset))

            reactions = cursor.fetchall()

            return True, reactions

        except pymysql.Error as e:
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()
