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

            # Get songs in playlist
            songs_query = """
                SELECT
                    ps.SongID,
                    ps.AddedAt,
                    ps.OrderIndex,
                    s.Title as song_title,
                    s.Duration,
                    s.ReleaseDate,
                    a.ArtworkID,
                    a.Title as artwork_title,
                    a.Type as artwork_type,
                    ar.ArtistID,
                    u2.Username as artist_username
                FROM PlaylistSong ps
                JOIN Song s ON ps.SongID = s.SongID
                JOIN Artwork a ON s.ArtworkID = a.ArtworkID
                JOIN Artist ar ON a.ArtistID = ar.ArtistID
                JOIN User u2 ON ar.UserID = u2.UserID
                WHERE ps.PlaylistID = %s
                ORDER BY ps.OrderIndex ASC, ps.AddedAt ASC
            """
            cursor.execute(songs_query, (playlist_id,))
            songs = cursor.fetchall()

            # Build response
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
        """
        Add song to playlist (Listener only, owner only)

        Args:
            user_id (int): User's ID
            playlist_id (int): Playlist's ID
            song_id (int): Song's ID
            order_index (int): Optional order index

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

            # Check if song exists
            cursor.execute("SELECT SongID FROM Song WHERE SongID = %s", (song_id,))
            if not cursor.fetchone():
                return False, "Song not found"

            # Check if song is already in playlist
            cursor.execute(
                "SELECT PlaylistID FROM PlaylistSong WHERE PlaylistID = %s AND SongID = %s",
                (playlist_id, song_id)
            )
            if cursor.fetchone():
                return False, "Song is already in this playlist"

            # If no order_index provided, add to end
            if order_index is None:
                cursor.execute(
                    "SELECT MAX(OrderIndex) as max_index FROM PlaylistSong WHERE PlaylistID = %s",
                    (playlist_id,)
                )
                result = cursor.fetchone()
                max_index = result['max_index'] if result['max_index'] is not None else -1
                order_index = max_index + 1

            # Add song to playlist
            cursor.execute(
                """
                INSERT INTO PlaylistSong (PlaylistID, SongID, OrderIndex)
                VALUES (%s, %s, %s)
                """,
                (playlist_id, song_id, order_index)
            )
            connection.commit()

            return True, {
                'message': 'Song added to playlist successfully',
                'playlist_id': playlist_id,
                'song_id': song_id,
                'order_index': order_index
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

            # Check if song is in playlist
            cursor.execute(
                "SELECT PlaylistID FROM PlaylistSong WHERE PlaylistID = %s AND SongID = %s",
                (playlist_id, song_id)
            )
            if not cursor.fetchone():
                return False, "Song is not in this playlist"

            # Remove song from playlist
            cursor.execute(
                "DELETE FROM PlaylistSong WHERE PlaylistID = %s AND SongID = %s",
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
