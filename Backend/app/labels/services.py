"""
Label service layer for label operations
"""

import pymysql
from app.auth.utils import get_db_connection


class LabelService:
    """Service class for label operations"""

    @staticmethod
    def get_all_labels():
        """
        Get all record labels

        Returns:
            tuple: (success: bool, result: list/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            cursor.execute(
                """
                SELECT 
                    LabelID,
                    Name,
                    ContactEmail,
                    Country,
                    FoundedYear
                FROM Label
                ORDER BY Name ASC
                """
            )
            labels = cursor.fetchall()

            return True, labels

        except pymysql.Error as e:
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_label_by_id(label_id):
        """
        Get label details by label ID

        Args:
            label_id (int): Label's ID

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            cursor.execute(
                """
                SELECT 
                    LabelID,
                    Name,
                    ContactEmail,
                    Country,
                    FoundedYear
                FROM Label
                WHERE LabelID = %s
                """,
                (label_id,),
            )
            label = cursor.fetchone()

            if not label:
                return False, "Label not found"

            return True, label

        except pymysql.Error as e:
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_label_artists(label_id):
        """
        Get all artists belonging to a label

        Args:
            label_id (int): Label's ID

        Returns:
            tuple: (success: bool, result: list/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Check if label exists
            cursor.execute("SELECT LabelID FROM Label WHERE LabelID = %s", (label_id,))
            if not cursor.fetchone():
                return False, "Label not found"

            cursor.execute(
                """
                SELECT 
                    a.ArtistID,
                    a.UserID,
                    u.Username,
                    u.FirstName,
                    u.LastName
                FROM Artist a
                JOIN User u ON a.UserID = u.UserID
                WHERE a.LabelID = %s
                ORDER BY u.Username ASC
                """,
                (label_id,),
            )
            artists = cursor.fetchall()

            # Format artists for frontend
            formatted_artists = []
            for artist in artists:
                name = artist["Username"] or f"{artist['FirstName']} {artist['LastName']}".strip() or "Unknown Artist"
                formatted_artists.append({
                    "id": artist["ArtistID"],
                    "name": name,
                    "image": "/ProfilePicArtist.png",  # Default image
                })

            return True, formatted_artists

        except pymysql.Error as e:
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

