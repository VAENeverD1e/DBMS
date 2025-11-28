"""
Artist service layer for artist operations
"""

import pymysql
import uuid
import os
import tempfile
from datetime import date
from flask import current_app
from app.auth.utils import get_db_connection
from services.s3_service import s3_service

# Try to import mutagen for audio duration calculation
try:
    from mutagen.mp3 import MP3
    from mutagen import File as MutagenFile
    MUTAGEN_AVAILABLE = True
except ImportError:
    MUTAGEN_AVAILABLE = False
    print("Warning: mutagen not installed. Audio duration will default to 0.")


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

            cursor.execute("SELECT ArtistID FROM Artist WHERE UserID = %s", (user_id,))
            artist = cursor.fetchone()

            return artist["ArtistID"] if artist else None

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

            query = """
                SELECT
                    a.ArtistID,
                    a.UserID,
                    a.LabelID,
                    a.Genre,
                    a.VerifiedStatus,
                    a.TotalFollowers,
                    asl.SMLinks,
                    u.Username,
                    u.FirstName,
                    u.LastName,
                    u.Email
                FROM Artist a
                JOIN User u ON a.UserID = u.UserID
                LEFT JOIN Artist_SMLinks asl ON asl.ArtistID = a.ArtistID
                WHERE 1=1
            """
            params = []

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

            query += " ORDER BY a.TotalFollowers DESC, a.ArtistID DESC LIMIT %s OFFSET %s"
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

            query = """
                SELECT
                    a.ArtistID,
                    a.UserID,
                    a.LabelID,
                    a.Genre,
                    a.VerifiedStatus,
                    a.TotalFollowers,
                    asl.SMLinks,
                    u.Username,
                    u.FirstName,
                    u.LastName,
                    u.Email
                FROM Artist a
                JOIN User u ON a.UserID = u.UserID
                LEFT JOIN Artist_SMLinks asl ON asl.ArtistID = a.ArtistID
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

            cursor.execute(
                "SELECT ArtistID FROM Artist WHERE ArtistID = %s", (artist_id,)
            )
            if not cursor.fetchone():
                return False, "Artist not found"

            query = """
                SELECT
                    aw.ArtworkID,
                    aw.Title,
                    aw.Genre,
                    aw.ReleaseDate,
                    aw.Duration,
                    aw.CoverImage,
                    COALESCE(COUNT(DISTINCT re.ListenerID), 0) AS TotalLike,
                    CASE
                        WHEN al.AlbumID IS NOT NULL THEN 'Album'
                        ELSE 'Single'
                    END AS Type,
                    COUNT(DISTINCT s.SingleID) AS song_count
                FROM ReleaseTable rel
                JOIN Artwork aw ON rel.ArtworkID = aw.ArtworkID
                LEFT JOIN Album al ON al.ArtworkID = aw.ArtworkID
                LEFT JOIN Single s ON s.ArtworkID = aw.ArtworkID
                LEFT JOIN React re ON re.ArtworkID = aw.ArtworkID
                WHERE rel.ArtistID = %s
                GROUP BY aw.ArtworkID, aw.Title, aw.Genre, aw.ReleaseDate, aw.Duration, aw.CoverImage, al.AlbumID
                ORDER BY aw.ReleaseDate DESC
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

            cursor.execute(
                "SELECT ArtistID, TotalFollowers FROM Artist WHERE ArtistID = %s",
                (artist_id,),
            )
            artist = cursor.fetchone()

            if not artist:
                return False, "Artist not found"

            stats = {
                "artist_id": artist["ArtistID"],
                "followers_count": artist["TotalFollowers"] if artist["TotalFollowers"] else 0,
            }

            cursor.execute(
                "SELECT COUNT(DISTINCT ArtworkID) as artwork_count FROM ReleaseTable WHERE ArtistID = %s",
                (artist_id,),
            )
            result = cursor.fetchone()
            stats["artwork_count"] = result["artwork_count"] if result else 0

            cursor.execute(
                """
                SELECT COUNT(*) as total_likes
                FROM React r
                JOIN ReleaseTable rel ON r.ArtworkID = rel.ArtworkID
                WHERE rel.ArtistID = %s
                """,
                (artist_id,),
            )
            result = cursor.fetchone()
            stats["total_likes"] = result["total_likes"] if result and result["total_likes"] else 0

            cursor.execute(
                """
                SELECT COUNT(DISTINCT s.SingleID) as song_count
                FROM Single s
                JOIN ReleaseTable rel ON s.ArtworkID = rel.ArtworkID
                WHERE rel.ArtistID = %s
                """,
                (artist_id,),
            )
            result = cursor.fetchone()
            stats["song_count"] = result["song_count"] if result else 0

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

            artist_id = ArtistService.get_artist_id(user_id)
            if not artist_id:
                return False, "User is not an artist"

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

            query = """
                SELECT
                    a.ArtistID,
                    a.UserID,
                    a.Genre,
                    a.VerifiedStatus,
                    a.TotalFollowers
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

            artist_id = ArtistService.get_artist_id(user_id)
            if not artist_id:
                return False, "User is not an artist"

            cursor.execute(
                """
                INSERT INTO Artist_SMLinks (ArtistID, SMLinks)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE SMLinks = VALUES(SMLinks)
                """,
                (artist_id, social_links),
            )
            connection.commit()

            query = """
                SELECT
                    a.ArtistID,
                    a.UserID,
                    a.Genre,
                    a.VerifiedStatus,
                    a.TotalFollowers,
                    asl.SMLinks
                FROM Artist a
                LEFT JOIN Artist_SMLinks asl ON asl.ArtistID = a.ArtistID
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
    def update_artist_label(user_id, label_id=None):
        """
        Update artist's record label

        Args:
            user_id (int): User's ID
            label_id (int or None): Label ID to join, or None to leave label

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            artist_id = ArtistService.get_artist_id(user_id)
            if not artist_id:
                return False, "User is not an artist"

            # If label_id is provided, validate it exists
            if label_id is not None:
                cursor.execute("SELECT LabelID FROM Label WHERE LabelID = %s", (label_id,))
                if not cursor.fetchone():
                    return False, "Label not found"

            # Update artist's label
            cursor.execute(
                "UPDATE Artist SET LabelID = %s WHERE ArtistID = %s",
                (label_id, artist_id)
            )
            connection.commit()

            # Get updated artist
            query = """
                SELECT
                    a.ArtistID,
                    a.UserID,
                    a.LabelID,
                    a.Genre,
                    a.VerifiedStatus,
                    a.TotalFollowers,
                    l.Name as LabelName
                FROM Artist a
                LEFT JOIN Label l ON a.LabelID = l.LabelID
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
    def get_listener_id(user_id):
        """
        Helper: Get ListenerID from UserID
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            cursor.execute("SELECT ListenerID FROM Listener WHERE UserID = %s", (user_id,))
            listener = cursor.fetchone()

            return listener["ListenerID"] if listener else None
        except pymysql.Error:
            return None
        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_followers(artist_id, limit=50, offset=0):
        """
        Get followers of an artist
        Returns: (success: bool, result: dict with 'followers' list and 'total')
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            cursor.execute("SELECT ArtistID FROM Artist WHERE ArtistID = %s", (artist_id,))
            if not cursor.fetchone():
                return False, "Artist not found"

            cursor.execute(
                "SELECT COUNT(*) as total FROM Follow WHERE ArtistID = %s", (artist_id,)
            )
            total = cursor.fetchone()["total"]

            query = """
                SELECT 
                    f.ListenerID,
                    f.ArtistID,
                    l.UserID,
                    u.Username,
                    u.FirstName,
                    u.LastName
                FROM Follow f
                JOIN Listener l ON l.ListenerID = f.ListenerID
                JOIN User u ON u.UserID = l.UserID
                WHERE f.ArtistID = %s
                ORDER BY f.ListenerID DESC
                LIMIT %s OFFSET %s
            """
            cursor.execute(query, (artist_id, limit, offset))
            followers = cursor.fetchall()

            return True, {"followers": followers, "total": total}

        except pymysql.Error as e:
            return False, f"Database error: {str(e)}"
        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def self_verify(user_id):
        """
        Self-verify artist if prerequisites met:
        - followers >= 670
        - artworks >= 3
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            artist_id = ArtistService.get_artist_id(user_id)
            if not artist_id:
                return False, "User is not an artist"

            cursor.execute(
                "SELECT VerifiedStatus FROM Artist WHERE ArtistID = %s", (artist_id,)
            )
            row = cursor.fetchone()
            if not row:
                return False, "Artist not found"

            if row["VerifiedStatus"] == "Verified":
                return True, {"message": "Artist already verified", "status": "Verified"}

            cursor.execute(
                "SELECT COUNT(*) as count FROM Follow WHERE ArtistID = %s", (artist_id,)
            )
            followers = cursor.fetchone()["count"]

            cursor.execute(
                "SELECT COUNT(DISTINCT ArtworkID) as count FROM ReleaseTable WHERE ArtistID = %s",
                (artist_id,),
            )
            artworks = cursor.fetchone()["count"]

            if followers >= 670 and artworks >= 3:
                cursor.execute(
                    "UPDATE Artist SET VerifiedStatus = 'Verified' WHERE ArtistID = %s",
                    (artist_id,),
                )
                connection.commit()
                return True, {
                    "message": "Artist verified successfully",
                    "status": "Verified",
                    "followers": followers,
                    "artworks": artworks,
                }
            else:
                reasons = []
                if followers < 670:
                    reasons.append(f"Need {670 - followers} more followers (current: {followers})")
                if artworks < 3:
                    reasons.append(f"Need {3 - artworks} more artworks (current: {artworks})")

                return False, {
                    "message": "Verification prerequisites not met",
                    "reasons": reasons,
                    "current": {"followers": followers, "artworks": artworks},
                    "required": {"followers": 670, "artworks": 3},
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
    def follow_artist(user_id, artist_id):
        """
        Follow an artist (for listeners)

        Args:
            user_id (int): User's ID (listener)
            artist_id (int): Artist's ID to follow

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            cursor.execute("SELECT ArtistID FROM Artist WHERE ArtistID = %s", (artist_id,))
            if not cursor.fetchone():
                return False, "Artist not found"

            listener_id = ArtistService.get_listener_id(user_id)
            if not listener_id:
                return False, "User is not a listener"

            cursor.execute(
                "SELECT * FROM Follow WHERE ListenerID = %s AND ArtistID = %s",
                (listener_id, artist_id)
            )
            if cursor.fetchone():
                return False, "Already following this artist"

            cursor.execute(
                "INSERT INTO Follow (ListenerID, ArtistID) VALUES (%s, %s)",
                (listener_id, artist_id)
            )

            cursor.execute(
                "UPDATE Artist SET TotalFollowers = TotalFollowers + 1 WHERE ArtistID = %s",
                (artist_id,)
            )

            connection.commit()

            return True, {"artist_id": artist_id, "listener_id": listener_id}

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
        Unfollow an artist (for listeners)

        Args:
            user_id (int): User's ID (listener)
            artist_id (int): Artist's ID to unfollow

        Returns:
            tuple: (success: bool, result: str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            cursor.execute("SELECT ArtistID FROM Artist WHERE ArtistID = %s", (artist_id,))
            if not cursor.fetchone():
                return False, "Artist not found"

            listener_id = ArtistService.get_listener_id(user_id)
            if not listener_id:
                return False, "User is not a listener"

            cursor.execute(
                "SELECT * FROM Follow WHERE ListenerID = %s AND ArtistID = %s",
                (listener_id, artist_id)
            )
            if not cursor.fetchone():
                return False, "Not following this artist"

            cursor.execute(
                "DELETE FROM Follow WHERE ListenerID = %s AND ArtistID = %s",
                (listener_id, artist_id)
            )

            cursor.execute(
                "UPDATE Artist SET TotalFollowers = GREATEST(TotalFollowers - 1, 0) WHERE ArtistID = %s",
                (artist_id,)
            )

            connection.commit()

            return True, "Unfollowed successfully"

        except pymysql.Error as e:
            if connection:
                connection.rollback()
            return False, f"Database error: {str(e)}"
        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_follow_relationship(user_id, artist_id):
        """
        Check if a user is following an artist

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

            cursor.execute("SELECT ArtistID FROM Artist WHERE ArtistID = %s", (artist_id,))
            if not cursor.fetchone():
                return False, "Artist not found"

            listener_id = ArtistService.get_listener_id(user_id)
            if not listener_id:
                return True, {"is_following": False, "artist_id": artist_id}

            cursor.execute(
                "SELECT * FROM Follow WHERE ListenerID = %s AND ArtistID = %s",
                (listener_id, artist_id)
            )
            is_following = cursor.fetchone() is not None

            return True, {"is_following": is_following, "artist_id": artist_id}

        except pymysql.Error as e:
            return False, f"Database error: {str(e)}"
        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_artwork_detail(user_id, artwork_id):
        """
        Get detailed information about an artwork owned by the artist

        Args:
            user_id (int): User's ID (artist)
            artwork_id (int): Artwork's ID

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Get artist ID from user ID
            artist_id = ArtistService.get_artist_id(user_id)
            if not artist_id:
                return False, "User is not an artist"

            # Get artwork details
            cursor.execute(
                """
                SELECT 
                    aw.ArtworkID,
                    aw.Title,
                    aw.Genre,
                    aw.ReleaseDate,
                    aw.Duration,
                    aw.CoverImage,
                    rel.ArtistID,
                    u.Username as ArtistName
                FROM Artwork aw
                JOIN ReleaseTable rel ON rel.ArtworkID = aw.ArtworkID
                JOIN Artist art ON rel.ArtistID = art.ArtistID
                JOIN User u ON art.UserID = u.UserID
                WHERE aw.ArtworkID = %s
                """,
                (artwork_id,),
            )
            artwork = cursor.fetchone()

            if not artwork:
                return False, "Artwork not found"

            # Check if artwork belongs to this artist
            if artwork["ArtistID"] != artist_id:
                return False, "Artwork not owned by this artist"

            # Get total likes for this artwork
            cursor.execute(
                "SELECT COUNT(*) as total_likes FROM React WHERE ArtworkID = %s",
                (artwork_id,),
            )
            likes_row = cursor.fetchone() or {"total_likes": 0}
            total_likes = likes_row["total_likes"] or 0

            # Determine artwork type (Album or Single)
            cursor.execute(
                "SELECT AlbumID, TotalTrack FROM Album WHERE ArtworkID = %s",
                (artwork_id,),
            )
            album_row = cursor.fetchone()
            artwork_type = "Album" if album_row else "Single"

            # Get tracks (Singles) for this artwork
            if album_row:
                # For albums, fetch tracks by AlbumID and join with their Artwork records for titles
                cursor.execute(
                    """
                    SELECT 
                        s.SingleID,
                        s.TrackNumber,
                        s.FileURL,
                        aw.Title as TrackTitle,
                        aw.Duration as TrackDuration
                    FROM Single s
                    JOIN Artwork aw ON s.ArtworkID = aw.ArtworkID
                    WHERE s.AlbumID = %s
                    ORDER BY COALESCE(s.TrackNumber, s.SingleID)
                    """,
                    (album_row["AlbumID"],),
                )
            else:
                # For singles, fetch by ArtworkID
                cursor.execute(
                    """
                    SELECT 
                        s.SingleID,
                        s.TrackNumber,
                        s.FileURL,
                        aw.Title as TrackTitle,
                        aw.Duration as TrackDuration
                    FROM Single s
                    JOIN Artwork aw ON s.ArtworkID = aw.ArtworkID
                    WHERE s.ArtworkID = %s
                    ORDER BY COALESCE(s.TrackNumber, s.SingleID)
                    """,
                    (artwork_id,),
                )
            tracks = cursor.fetchall()

            # Format tracks with number and proper title
            formatted_tracks = []
            for idx, track in enumerate(tracks, 1):
                number = track["TrackNumber"] if track["TrackNumber"] is not None else idx
                # Use track title from Artwork, fallback to FileURL or generic name
                title = track["TrackTitle"] or track["FileURL"] or f"Track {number}"
                # Format duration from seconds to mm:ss
                duration_secs = track["TrackDuration"] or 0
                duration_str = f"{duration_secs // 60}:{duration_secs % 60:02d}" if duration_secs else "0:00"
                formatted_tracks.append({
                    "id": track["SingleID"],
                    "number": number,
                    "title": title,
                    "duration": duration_str,
                    "likes": 0,
                    "audioFile": track["FileURL"],
                })

            return True, {
                "artwork": {
                    "id": artwork["ArtworkID"],
                    "title": artwork["Title"],
                    "artist": artwork["ArtistName"],
                    "genre": artwork["Genre"],
                    "releaseDate": str(artwork["ReleaseDate"]) if artwork["ReleaseDate"] else None,
                    "duration": artwork["Duration"],
                    "totalLikes": total_likes,
                    "coverImage": artwork["CoverImage"],
                    "type": artwork_type,
                    "trackCount": len(formatted_tracks),
                },
                "tracks": formatted_tracks,
            }

        except pymysql.Error as e:
            return False, f"Database error: {str(e)}"
        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def delete_artwork(user_id, artwork_id):
        """
        Delete an artwork owned by the artist

        Args:
            user_id (int): User's ID (artist)
            artwork_id (int): Artwork's ID

        Returns:
            tuple: (success: bool, result: str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Get artist ID from user ID
            artist_id = ArtistService.get_artist_id(user_id)
            if not artist_id:
                return False, "User is not an artist"

            # Check if artwork exists and belongs to this artist via ReleaseTable
            cursor.execute(
                "SELECT ArtworkID, ArtistID FROM ReleaseTable WHERE ArtworkID = %s AND ArtistID = %s",
                (artwork_id, artist_id),
            )
            rel = cursor.fetchone()

            if not rel:
                # Determine if artwork does not exist at all or just not owned
                cursor.execute("SELECT ArtworkID FROM Artwork WHERE ArtworkID = %s", (artwork_id,))
                if not cursor.fetchone():
                    return False, "Artwork not found"
                return False, "Artwork not owned by this artist"

            # Deleting the artwork will cascade to related tables (Album, Single, React, etc.)
            cursor.execute("DELETE FROM Artwork WHERE ArtworkID = %s", (artwork_id,))

            connection.commit()

            return True, "Artwork deleted successfully"

        except pymysql.Error as e:
            if connection:
                connection.rollback()
            return False, f"Database error: {str(e)}"
        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def _get_audio_duration(file_obj):
        """
        Calculate audio duration in seconds using mutagen
        
        Args:
            file_obj: File object from request.files
            
        Returns:
            int: Duration in seconds, or 0 if unable to determine
        """
        if not MUTAGEN_AVAILABLE:
            return 0
            
        try:
            # Save file temporarily to read with mutagen
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp:
                file_obj.seek(0)
                tmp.write(file_obj.read())
                tmp_path = tmp.name
            
            # Reset file position for subsequent reads
            file_obj.seek(0)
            
            # Try to get duration
            try:
                audio = MutagenFile(tmp_path)
                if audio and audio.info:
                    duration = int(audio.info.length)
                else:
                    duration = 0
            finally:
                # Clean up temp file
                os.unlink(tmp_path)
            
            return duration
        except Exception as e:
            print(f"Warning: Could not determine audio duration: {e}")
            return 0

    @staticmethod
    def _get_artist_id_by_username(cursor, username):
        """
        Get artist ID from username
        
        Args:
            cursor: Database cursor
            username: Username to look up
            
        Returns:
            int or None: Artist ID if found
        """
        cursor.execute(
            """
            SELECT a.ArtistID 
            FROM Artist a 
            JOIN User u ON a.UserID = u.UserID 
            WHERE u.Username = %s
            """,
            (username,)
        )
        result = cursor.fetchone()
        return result["ArtistID"] if result else None

    @staticmethod
    def create_artwork(user_id, mode, title, genre, cover_image, track_files, 
                       track_titles, track_numbers=None, collaborations=None):
        """
        Create a new artwork (Single or Album) with S3 uploads
        
        Args:
            user_id (int): User's ID (artist)
            mode (str): 'single' or 'album'
            title (str): Artwork title
            genre (str): Genre name
            cover_image: Cover image file object
            track_files (list): List of audio file objects
            track_titles (list): List of track title strings
            track_numbers (list): Optional list of track numbers
            collaborations (list): Optional list of collaborator usernames
            
        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        uploaded_files = []  # Track uploaded S3 files for cleanup on error
        
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            
            # Get artist ID from user ID
            artist_id = ArtistService.get_artist_id(user_id)
            if not artist_id:
                return False, "User is not an artist"
            
            # Generate unique IDs for file paths
            artwork_uuid = str(uuid.uuid4())
            
            # Get file extension for cover image
            cover_ext = cover_image.filename.rsplit('.', 1)[-1] if '.' in cover_image.filename else 'jpg'
            
            # Upload cover image to S3
            cover_s3_path = f"artworks/covers/{artist_id}/{artwork_uuid}.{cover_ext}"
            cover_result = s3_service.upload_file(cover_image, f"artworks/covers/{artist_id}", f"{artwork_uuid}.{cover_ext}")
            
            if not cover_result.get('success'):
                return False, f"Failed to upload cover image: {cover_result.get('error')}"
            
            cover_url = cover_result['url']
            uploaded_files.append(cover_result.get('key'))
            
            # Process tracks and calculate durations
            track_data = []
            total_duration = 0
            
            for i, track_file in enumerate(track_files):
                track_num = track_numbers[i] if track_numbers and i < len(track_numbers) else i + 1
                track_title = track_titles[i] if i < len(track_titles) else f"Track {track_num}"
                
                # Calculate duration
                duration = ArtistService._get_audio_duration(track_file)
                total_duration += duration
                
                # Generate S3 path for track
                track_uuid = str(uuid.uuid4())
                if mode == "single":
                    s3_folder = f"artworks/singles/{artist_id}"
                else:
                    s3_folder = f"artworks/albums/{artist_id}/{artwork_uuid}"
                
                track_filename = f"{track_num:02d}-{track_uuid}.mp3"
                
                # Upload track to S3
                track_result = s3_service.upload_file(track_file, s3_folder, track_filename)
                
                if not track_result.get('success'):
                    # Cleanup already uploaded files
                    for key in uploaded_files:
                        s3_service.delete_file(key)
                    return False, f"Failed to upload track {track_num}: {track_result.get('error')}"
                
                uploaded_files.append(track_result.get('key'))
                
                track_data.append({
                    'number': track_num,
                    'title': track_title,
                    'duration': duration,
                    'url': track_result['url']
                })
            
            # Start database transaction
            today = date.today()
            
            if mode == "single":
                # Create single artwork
                cursor.execute(
                    """
                    INSERT INTO Artwork (Title, ReleaseDate, CoverImage, Duration, Genre)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (title, today, cover_url, track_data[0]['duration'], genre)
                )
                artwork_id = cursor.lastrowid
                
                # Create Single record
                cursor.execute(
                    """
                    INSERT INTO Single (ArtworkID, AlbumID, TrackNumber, FileURL)
                    VALUES (%s, NULL, 1, %s)
                    """,
                    (artwork_id, track_data[0]['url'])
                )
                single_id = cursor.lastrowid
                
                # Create ReleaseTable entry
                cursor.execute(
                    """
                    INSERT INTO ReleaseTable (ArtistID, ArtworkID)
                    VALUES (%s, %s)
                    """,
                    (artist_id, artwork_id)
                )
                
                # Handle collaborations for single
                if collaborations:
                    for collab_username in collaborations:
                        collab_artist_id = ArtistService._get_artist_id_by_username(cursor, collab_username)
                        if collab_artist_id and collab_artist_id != artist_id:
                            cursor.execute(
                                """
                                INSERT INTO Collaboration (ArtistID_1, ArtistID_2, SingleID)
                                VALUES (%s, %s, %s)
                                """,
                                (artist_id, collab_artist_id, single_id)
                            )
                        else:
                            print(f"Warning: Collaborator '{collab_username}' not found or is the main artist")
                
                connection.commit()
                
                return True, {
                    'id': artwork_id,
                    'type': 'Single',
                    'title': title,
                    'coverImage': cover_url,
                    'genre': genre,
                    'duration': track_data[0]['duration'],
                    'trackCount': 1,
                    'tracks': [{
                        'id': single_id,
                        'number': 1,
                        'title': track_data[0]['title'],
                        'url': track_data[0]['url'],
                        'duration': track_data[0]['duration']
                    }]
                }
            
            else:  # Album mode
                # Create album-level Artwork
                cursor.execute(
                    """
                    INSERT INTO Artwork (Title, ReleaseDate, CoverImage, Duration, Genre)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (title, today, cover_url, total_duration, genre)
                )
                album_artwork_id = cursor.lastrowid
                
                # Create Album record
                cursor.execute(
                    """
                    INSERT INTO Album (ArtworkID, TotalTrack)
                    VALUES (%s, %s)
                    """,
                    (album_artwork_id, len(track_data))
                )
                album_id = cursor.lastrowid
                
                # Create ReleaseTable entry for album
                cursor.execute(
                    """
                    INSERT INTO ReleaseTable (ArtistID, ArtworkID)
                    VALUES (%s, %s)
                    """,
                    (artist_id, album_artwork_id)
                )
                
                # Create each track
                result_tracks = []
                for track in track_data:
                    # Create track-level Artwork
                    cursor.execute(
                        """
                        INSERT INTO Artwork (Title, ReleaseDate, CoverImage, Duration, Genre)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (track['title'], today, cover_url, track['duration'], genre)
                    )
                    track_artwork_id = cursor.lastrowid
                    
                    # Create Single record linked to album
                    cursor.execute(
                        """
                        INSERT INTO Single (ArtworkID, AlbumID, TrackNumber, FileURL)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (track_artwork_id, album_id, track['number'], track['url'])
                    )
                    single_id = cursor.lastrowid
                    
                    # Create ReleaseTable entry for track
                    cursor.execute(
                        """
                        INSERT INTO ReleaseTable (ArtistID, ArtworkID)
                        VALUES (%s, %s)
                        """,
                        (artist_id, track_artwork_id)
                    )
                    
                    # Handle collaborations for each track
                    if collaborations:
                        for collab_username in collaborations:
                            collab_artist_id = ArtistService._get_artist_id_by_username(cursor, collab_username)
                            if collab_artist_id and collab_artist_id != artist_id:
                                cursor.execute(
                                    """
                                    INSERT INTO Collaboration (ArtistID_1, ArtistID_2, SingleID)
                                    VALUES (%s, %s, %s)
                                    """,
                                    (artist_id, collab_artist_id, single_id)
                                )
                    
                    result_tracks.append({
                        'id': single_id,
                        'number': track['number'],
                        'title': track['title'],
                        'url': track['url'],
                        'duration': track['duration']
                    })
                
                connection.commit()
                
                return True, {
                    'id': album_artwork_id,
                    'type': 'Album',
                    'title': title,
                    'coverImage': cover_url,
                    'genre': genre,
                    'duration': total_duration,
                    'trackCount': len(result_tracks),
                    'tracks': result_tracks
                }
        
        except pymysql.Error as e:
            if connection:
                connection.rollback()
            # Attempt to clean up S3 files on database error
            for key in uploaded_files:
                try:
                    s3_service.delete_file(key)
                except Exception:
                    pass
            return False, f"Database error: {str(e)}"
        
        except Exception as e:
            if connection:
                connection.rollback()
            # Attempt to clean up S3 files on any error
            for key in uploaded_files:
                try:
                    s3_service.delete_file(key)
                except Exception:
                    pass
            return False, f"Error creating artwork: {str(e)}"
        
        finally:
            if connection:
                cursor.close()
                connection.close()
