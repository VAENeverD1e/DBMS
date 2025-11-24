"""
Reaction service layer for reaction operations
"""
import pymysql
from flask import current_app
from app.auth.utils import get_db_connection


class ReactionService:
    """Service class for reaction operations"""

    @staticmethod
    def create_reaction(user_id, reactable_type, reactable_id, emotion='Like'):
        """
        Create a reaction to a song or artwork (for listeners only)

        Args:
            user_id (int): User's ID
            reactable_type (str): Type of reactable ('Song' or 'Artwork')
            reactable_id (int): ID of the song or artwork
            emotion (str): Reaction emotion ('Like', 'Love', 'Dislike'), default 'Like'

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

            # Verify the reactable item exists
            if reactable_type == 'Song':
                cursor.execute("SELECT SongID FROM Song WHERE SongID = %s", (reactable_id,))
                if not cursor.fetchone():
                    return False, "Song not found"
            elif reactable_type == 'Artwork':
                cursor.execute("SELECT ArtworkID FROM Artwork WHERE ArtworkID = %s", (reactable_id,))
                if not cursor.fetchone():
                    return False, "Artwork not found"

            # Check if reaction already exists
            cursor.execute(
                """
                SELECT ReactionID FROM Reaction
                WHERE ListenerID = %s AND ReactableType = %s AND ReactableID = %s
                """,
                (listener_id, reactable_type, reactable_id)
            )
            existing_reaction = cursor.fetchone()

            if existing_reaction:
                # Update existing reaction
                cursor.execute(
                    """
                    UPDATE Reaction
                    SET Emotion = %s, ReactedAt = CURRENT_TIMESTAMP
                    WHERE ReactionID = %s
                    """,
                    (emotion, existing_reaction['ReactionID'])
                )
                connection.commit()

                # Fetch updated reaction
                cursor.execute(
                    """
                    SELECT ReactionID, ListenerID, ReactableType, ReactableID, Emotion, ReactedAt
                    FROM Reaction WHERE ReactionID = %s
                    """,
                    (existing_reaction['ReactionID'],)
                )
                updated_reaction = cursor.fetchone()

                return True, {
                    'message': 'Reaction updated successfully',
                    'reaction': updated_reaction
                }
            else:
                # Create new reaction
                cursor.execute(
                    """
                    INSERT INTO Reaction (ListenerID, ReactableType, ReactableID, Emotion)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (listener_id, reactable_type, reactable_id, emotion)
                )
                reaction_id = cursor.lastrowid
                connection.commit()

                # Fetch created reaction
                cursor.execute(
                    """
                    SELECT ReactionID, ListenerID, ReactableType, ReactableID, Emotion, ReactedAt
                    FROM Reaction WHERE ReactionID = %s
                    """,
                    (reaction_id,)
                )
                new_reaction = cursor.fetchone()

                return True, {
                    'message': 'Reaction created successfully',
                    'reaction': new_reaction
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
    def delete_reaction(user_id, reaction_id):
        """
        Delete a reaction (for listeners only)

        Args:
            user_id (int): User's ID
            reaction_id (int): Reaction's ID

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

            # Check if reaction exists and belongs to this listener
            cursor.execute(
                "SELECT ReactionID FROM Reaction WHERE ReactionID = %s AND ListenerID = %s",
                (reaction_id, listener_id)
            )
            reaction = cursor.fetchone()

            if not reaction:
                return False, "Reaction not found or does not belong to this user"

            # Delete the reaction
            cursor.execute(
                "DELETE FROM Reaction WHERE ReactionID = %s",
                (reaction_id,)
            )
            connection.commit()

            return True, {'message': 'Reaction deleted successfully'}

        except pymysql.Error as e:
            if connection:
                connection.rollback()
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_reactions_for_song(song_id):
        """
        Get all reactions for a specific song

        Args:
            song_id (int): Song's ID

        Returns:
            tuple: (success: bool, result: list/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Verify song exists
            cursor.execute("SELECT SongID FROM Song WHERE SongID = %s", (song_id,))
            if not cursor.fetchone():
                return False, "Song not found"

            # Get reactions for the song
            query = """
                SELECT
                    r.ReactionID,
                    r.ListenerID,
                    r.Emotion,
                    r.ReactedAt,
                    u.UserID,
                    u.Username,
                    u.FirstName,
                    u.LastName
                FROM Reaction r
                JOIN Listener l ON r.ListenerID = l.ListenerID
                JOIN User u ON l.UserID = u.UserID
                WHERE r.ReactableType = 'Song' AND r.ReactableID = %s
                ORDER BY r.ReactedAt DESC
            """
            cursor.execute(query, (song_id,))
            reactions = cursor.fetchall()

            # Get reaction summary
            cursor.execute(
                """
                SELECT
                    Emotion,
                    COUNT(*) as count
                FROM Reaction
                WHERE ReactableType = 'Song' AND ReactableID = %s
                GROUP BY Emotion
                """,
                (song_id,)
            )
            summary = cursor.fetchall()

            return True, {
                'reactions': reactions,
                'summary': summary,
                'total': len(reactions)
            }

        except pymysql.Error as e:
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_reactions_for_artwork(artwork_id):
        """
        Get all reactions for a specific artwork (album)

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
            cursor.execute("SELECT ArtworkID FROM Artwork WHERE ArtworkID = %s", (artwork_id,))
            if not cursor.fetchone():
                return False, "Artwork not found"

            # Get reactions for the artwork
            query = """
                SELECT
                    r.ReactionID,
                    r.ListenerID,
                    r.Emotion,
                    r.ReactedAt,
                    u.UserID,
                    u.Username,
                    u.FirstName,
                    u.LastName
                FROM Reaction r
                JOIN Listener l ON r.ListenerID = l.ListenerID
                JOIN User u ON l.UserID = u.UserID
                WHERE r.ReactableType = 'Artwork' AND r.ReactableID = %s
                ORDER BY r.ReactedAt DESC
            """
            cursor.execute(query, (artwork_id,))
            reactions = cursor.fetchall()

            # Get reaction summary
            cursor.execute(
                """
                SELECT
                    Emotion,
                    COUNT(*) as count
                FROM Reaction
                WHERE ReactableType = 'Artwork' AND ReactableID = %s
                GROUP BY Emotion
                """,
                (artwork_id,)
            )
            summary = cursor.fetchall()

            return True, {
                'reactions': reactions,
                'summary': summary,
                'total': len(reactions)
            }

        except pymysql.Error as e:
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()
