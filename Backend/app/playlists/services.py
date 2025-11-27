"""
Playlist service layer for playlist operations
"""
import pymysql
from flask import current_app
from app.auth.utils import get_db_connection


class PlaylistService:
    """Service class for playlist operations"""

    @staticmethod
    def get_listener_id(user_id):
        """
        Get listener ID from user ID

        Args:
            user_id (int): User's ID

        Returns:
            int or None: Listener ID if found, None otherwise
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            cursor.execute(
                "SELECT ListenerID FROM Listener WHERE UserID = %s",
                (user_id,)
            )
            listener = cursor.fetchone()

            return listener['ListenerID'] if listener else None

        except pymysql.Error:
            return None

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_all_playlists(user_id=None, limit=50, offset=0):
        """
        Get all playlists (public view or user's own playlists)

        Args:
            user_id (int): Optional user ID to filter by user's playlists
            limit (int): Number of records to return
            offset (int): Offset for pagination

        Returns:
            tuple: (success: bool, result: list/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            if user_id:
                # Get user's own playlists
                listener_id = PlaylistService.get_listener_id(user_id)
                if not listener_id:
                    return True, []  # Not a listener, return empty list

                query = """
                    SELECT
                        p.PlaylistID,
                        p.ListenerID,
                        p.Name,
                        p.CreateDate,
                        u.Username as owner_username,
                        COUNT(DISTINCT ps.SongID) as song_count
                    FROM Playlist p
                    JOIN Listener l ON p.ListenerID = l.ListenerID
                    JOIN User u ON l.UserID = u.UserID
                    LEFT JOIN PlaylistSong ps ON p.PlaylistID = ps.PlaylistID
                    WHERE p.ListenerID = %s
                    GROUP BY p.PlaylistID, p.ListenerID, p.Name, p.CreateDate, u.Username
                    ORDER BY p.CreateDate DESC
                    LIMIT %s OFFSET %s
                """
                cursor.execute(query, (listener_id, limit, offset))
            else:
                # Get all playlists (public view)
                query = """
                    SELECT
                        p.PlaylistID,
                        p.ListenerID,
                        p.Name,
                        p.CreateDate,
                        u.Username as owner_username,
                        COUNT(DISTINCT ps.SongID) as song_count
                    FROM Playlist p
                    JOIN Listener l ON p.ListenerID = l.ListenerID
                    JOIN User u ON l.UserID = u.UserID
                    LEFT JOIN PlaylistSong ps ON p.PlaylistID = ps.PlaylistID
                    GROUP BY p.PlaylistID, p.ListenerID, p.Name, p.CreateDate, u.Username
                    ORDER BY p.CreateDate DESC
                    LIMIT %s OFFSET %s
                """
                cursor.execute(query, (limit, offset))

            playlists = cursor.fetchall()
            return True, playlists

        except pymysql.Error as e:
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_playlist_by_id(playlist_id, user_id=None):
        """
        Get playlist details with songs

        Args:
            playlist_id (int): Playlist's ID
            user_id (int): Optional user ID for permission checks

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Get playlist details
            query = """
                SELECT
                    p.PlaylistID,
                    p.ListenerID,
                    p.Name,
                    p.CreateDate,
                    u.UserID as owner_user_id,
                    u.Username as owner_username,
                    u.FirstName as owner_first_name,
                    u.LastName as owner_last_name
                FROM Playlist p
                JOIN Listener l ON p.ListenerID = l.ListenerID
                JOIN User u ON l.UserID = u.UserID
                WHERE p.PlaylistID = %s
            """
            cursor.execute(query, (playlist_id,))
            playlist = cursor.fetchone()

            if not playlist:
                return False, "Playlist not found"

            # Get singles in playlist (using Contain/Single/Artwork schema)
            songs_query = """
                SELECT
                    c.SingleID,
                    s.FileURL,
                    s.TrackNumber,
                    a.ArtworkID,
                    a.Title AS song_title,
                    a.ReleaseDate,
                    a.CoverImage,
                    a.Duration,
                    a.Genre
                FROM Contain c
                JOIN Single s ON c.SingleID = s.SingleID
                JOIN Artwork a ON s.ArtworkID = a.ArtworkID
                WHERE c.PlaylistID = %s
                ORDER BY c.SingleID ASC
            """
            cursor.execute(songs_query, (playlist_id,))
            songs = cursor.fetchall()

            # Build response (still expose generic "songs" for frontend compatibility)
            result = {
                'playlist_id': playlist['PlaylistID'],
                'listener_id': playlist['ListenerID'],
                'name': playlist['Name'],
                'create_date': playlist['CreateDate'],
                'owner': {
                    'user_id': playlist['owner_user_id'],
                    'username': playlist['owner_username'],
                    'first_name': playlist['owner_first_name'],
                    'last_name': playlist['owner_last_name']
                },
                'songs': songs,
                'song_count': len(songs)
            }

            return True, result

        except pymysql.Error as e:
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def create_playlist(user_id, name):
        """
        Create a new playlist (Listener only)

        Args:
            user_id (int): User's ID
            name (str): Playlist name

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Get listener ID
            listener_id = PlaylistService.get_listener_id(user_id)
            if not listener_id:
                return False, "User is not a listener"

            cursor.execute(
                "SELECT 1 FROM Playlist WHERE ListenerID = %s AND Name = %s",
                (listener_id, name)
            )
            if cursor.fetchone():
                return False, "You already have a playlist with this name"

            # Create playlist
            cursor.execute(
                "INSERT INTO Playlist (ListenerID, Name) VALUES (%s, %s)",
                (listener_id, name)
            )
            playlist_id = cursor.lastrowid
            connection.commit()

            # Fetch created playlist
            cursor.execute(
                """
                SELECT
                    p.PlaylistID,
                    p.ListenerID,
                    p.Name,
                    p.CreateDate,
                    u.Username as owner_username
                FROM Playlist p
                JOIN Listener l ON p.ListenerID = l.ListenerID
                JOIN User u ON l.UserID = u.UserID
                WHERE p.PlaylistID = %s
                """,
                (playlist_id,)
            )
            playlist = cursor.fetchone()

            return True, playlist

        except pymysql.Error as e:
            if connection:
                connection.rollback()
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def update_playlist(user_id, playlist_id, name):
        """
        Update playlist name (Listener only, owner only)

        Args:
            user_id (int): User's ID
            playlist_id (int): Playlist's ID
            name (str): New playlist name

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Get listener ID
            listener_id = PlaylistService.get_listener_id(user_id)
            if not listener_id:
                return False, "User is not a listener"

            # Check if playlist exists and user is owner
            cursor.execute(
                "SELECT ListenerID FROM Playlist WHERE PlaylistID = %s",
                (playlist_id,)
            )
            playlist = cursor.fetchone()

            if not playlist:
                return False, "Playlist not found"

            if playlist['ListenerID'] != listener_id:
                return False, "You are not the owner of this playlist"

            cursor.execute(
                "SELECT 1 FROM Playlist WHERE ListenerID = %s AND Name = %s AND PlaylistID <> %s",
                (listener_id, name, playlist_id)
            )
            if cursor.fetchone():
                return False, "You already have a playlist with this name"

            # Update playlist
            cursor.execute(
                "UPDATE Playlist SET Name = %s WHERE PlaylistID = %s",
                (name, playlist_id)
            )
            connection.commit()

            # Fetch updated playlist
            cursor.execute(
                """
                SELECT
                    p.PlaylistID,
                    p.ListenerID,
                    p.Name,
                    p.CreateDate,
                    u.Username as owner_username
                FROM Playlist p
                JOIN Listener l ON p.ListenerID = l.ListenerID
                JOIN User u ON l.UserID = u.UserID
                WHERE p.PlaylistID = %s
                """,
                (playlist_id,)
            )
            updated_playlist = cursor.fetchone()

            return True, updated_playlist

        except pymysql.Error as e:
            if connection:
                connection.rollback()
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def delete_playlist(user_id, playlist_id):
        """
        Delete playlist (Listener only, owner only)

        Args:
            user_id (int): User's ID
            playlist_id (int): Playlist's ID

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Get listener ID
            listener_id = PlaylistService.get_listener_id(user_id)
            if not listener_id:
                return False, "User is not a listener"

            # Check if playlist exists and user is owner
            cursor.execute(
                "SELECT ListenerID FROM Playlist WHERE PlaylistID = %s",
                (playlist_id,)
            )
            playlist = cursor.fetchone()

            if not playlist:
                return False, "Playlist not found"

            if playlist['ListenerID'] != listener_id:
                return False, "You are not the owner of this playlist"

            # Delete playlist (CASCADE will delete PlaylistSong entries)
            cursor.execute(
                "DELETE FROM Playlist WHERE PlaylistID = %s",
                (playlist_id,)
            )
            connection.commit()

            return True, {'message': 'Playlist deleted successfully'}

        except pymysql.Error as e:
            if connection:
                connection.rollback()
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def add_song_to_playlist(user_id, playlist_id, song_id, order_index=None):
        """Add a *single* to playlist using Contain/Single tables (Listener only, owner only).

        Args:
            user_id (int): User's ID
            playlist_id (int): Playlist's ID
            song_id (int): Single's ID (kept as song_id for frontend compatibility)
            order_index (int): Optional order index (currently unused but kept for API compatibility)

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Get listener ID
            listener_id = PlaylistService.get_listener_id(user_id)
            if not listener_id:
                return False, "User is not a listener"

            # Check if playlist exists and user is owner
            cursor.execute(
                "SELECT ListenerID FROM Playlist WHERE PlaylistID = %s",
                (playlist_id,)
            )
            playlist = cursor.fetchone()

            if not playlist:
                return False, "Playlist not found"

            if playlist['ListenerID'] != listener_id:
                return False, "You are not the owner of this playlist"

            # Check if single exists
            cursor.execute("SELECT SingleID FROM Single WHERE SingleID = %s", (song_id,))
            if not cursor.fetchone():
                return False, "Song not found"

            # Check if single is already in playlist
            cursor.execute(
                "SELECT PlaylistID FROM Contain WHERE PlaylistID = %s AND SingleID = %s",
                (playlist_id, song_id)
            )
            if cursor.fetchone():
                return False, "Song is already in this playlist"

            cursor.execute(
                "SELECT COUNT(*) AS song_count FROM Contain WHERE PlaylistID = %s",
                (playlist_id,)
            )
            count_row = cursor.fetchone()
            if count_row and count_row['song_count'] >= 360:
                return False, "Playlist has reached the maximum limit of 360 songs"

            # NOTE: Contain schema has no ordering column; ignore order_index for now

            # Add single to playlist
            cursor.execute(
                """
                INSERT INTO Contain (PlaylistID, SingleID)
                VALUES (%s, %s)
                """,
                (playlist_id, song_id)
            )
            connection.commit()

            return True, {
                'message': 'Song added to playlist successfully',
                'playlist_id': playlist_id,
                'song_id': song_id
            }

        except pymysql.Error as e:
            if connection:
                connection.rollback()
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def remove_song_from_playlist(user_id, playlist_id, song_id):
        """
        Remove song from playlist (Listener only, owner only)

        Args:
            user_id (int): User's ID
            playlist_id (int): Playlist's ID
            song_id (int): Song's ID

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Get listener ID
            listener_id = PlaylistService.get_listener_id(user_id)
            if not listener_id:
                return False, "User is not a listener"

            # Check if playlist exists and user is owner
            cursor.execute(
                "SELECT ListenerID FROM Playlist WHERE PlaylistID = %s",
                (playlist_id,)
            )
            playlist = cursor.fetchone()

            if not playlist:
                return False, "Playlist not found"

            if playlist['ListenerID'] != listener_id:
                return False, "You are not the owner of this playlist"

            # Check if song (single) is in playlist
            cursor.execute(
                "SELECT PlaylistID FROM Contain WHERE PlaylistID = %s AND SingleID = %s",
                (playlist_id, song_id)
            )
            if not cursor.fetchone():
                return False, "Song is not in this playlist"

            # Remove song (single) from playlist
            cursor.execute(
                "DELETE FROM Contain WHERE PlaylistID = %s AND SingleID = %s",
                (playlist_id, song_id)
            )
            connection.commit()

            return True, {'message': 'Song removed from playlist successfully'}

        except pymysql.Error as e:
            if connection:
                connection.rollback()
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()
