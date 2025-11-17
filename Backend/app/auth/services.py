"""
Authentication service layer for business logic
"""
import pymysql
from flask import current_app
from .utils import hash_password, verify_password, get_db_connection


class AuthService:
    """Service class for authentication operations"""

    @staticmethod
    def register_user(email, password, username, first_name=None, last_name=None, role='Guest'):
        """
        Register a new user

        Args:
            email (str): User's email
            password (str): User's plain text password
            username (str): User's username
            first_name (str): User's first name (optional)
            last_name (str): User's last name (optional)
            role (str): User's role ('Guest', 'Listener' or 'Artist'), defaults to 'Guest'

        Returns:
            tuple: (success: bool, result: dict/str)
                - On success: (True, user_dict)
                - On failure: (False, error_message)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Check if email already exists
            cursor.execute("SELECT UserID FROM User WHERE Email = %s", (email,))
            if cursor.fetchone():
                return False, "Email already registered"

            # Check if username already exists
            cursor.execute("SELECT UserID FROM User WHERE Username = %s", (username,))
            if cursor.fetchone():
                return False, "Username already taken"

            # Hash the password
            hashed_password = hash_password(password)

            # Insert new user
            insert_query = """
                INSERT INTO User (Email, Password, Username, FirstName, LastName, Role)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (email, hashed_password, username, first_name, last_name, role))
            user_id = cursor.lastrowid

            # Create corresponding Listener or Artist record (not for Guest role)
            if role == 'Listener':
                cursor.execute(
                    "INSERT INTO Listener (UserID) VALUES (%s)",
                    (user_id,)
                )
            elif role == 'Artist':
                cursor.execute(
                    "INSERT INTO Artist (UserID, VerifiedStatus) VALUES (%s, 'Pending')",
                    (user_id,)
                )
            # Guest role doesn't need a separate table entry

            connection.commit()

            # Fetch and return the created user
            cursor.execute(
                "SELECT UserID, Email, Username, FirstName, LastName, Role FROM User WHERE UserID = %s",
                (user_id,)
            )
            user = cursor.fetchone()

            return True, user

        except pymysql.Error as e:
            if connection:
                connection.rollback()
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def login_user(login_identifier, password):
        """
        Authenticate a user by email/username and password

        Args:
            login_identifier (str): User's email or username
            password (str): User's plain text password

        Returns:
            tuple: (success: bool, result: dict/str)
                - On success: (True, user_dict)
                - On failure: (False, error_message)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Find user by email or username
            query = """
                SELECT UserID, Email, Password, Username, FirstName, LastName, Role
                FROM User
                WHERE Email = %s OR Username = %s
            """
            cursor.execute(query, (login_identifier, login_identifier))
            user = cursor.fetchone()

            if not user:
                return False, "Invalid email/username or password"

            # Verify password
            if not verify_password(password, user['Password']):
                return False, "Invalid email/username or password"

            # Remove password from returned data
            del user['Password']

            return True, user

        except pymysql.Error as e:
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_user_by_id(user_id):
        """
        Get user information by user ID

        Args:
            user_id (int): User's ID

        Returns:
            dict or None: User data or None if not found
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            query = """
                SELECT UserID, Email, Username, FirstName, LastName, Role
                FROM User
                WHERE UserID = %s
            """
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()

            return user

        except pymysql.Error:
            return None

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_user_profile(user_id):
        """
        Get detailed user profile including role-specific information

        Args:
            user_id (int): User's ID

        Returns:
            dict or None: User profile data or None if not found
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Get basic user info
            cursor.execute(
                "SELECT UserID, Email, Username, FirstName, LastName, Role FROM User WHERE UserID = %s",
                (user_id,)
            )
            user = cursor.fetchone()

            if not user:
                return None

            # Get role-specific information
            if user['Role'] == 'Listener':
                cursor.execute(
                    """
                    SELECT ListenerID, Preference, FavoriteGenre
                    FROM Listener
                    WHERE UserID = %s
                    """,
                    (user_id,)
                )
                listener_data = cursor.fetchone()
                if listener_data:
                    user['listener_profile'] = listener_data

            elif user['Role'] == 'Artist':
                cursor.execute(
                    """
                    SELECT ArtistID, Genre, VerifiedStatus, TotalFollowers, LabelID
                    FROM Artist
                    WHERE UserID = %s
                    """,
                    (user_id,)
                )
                artist_data = cursor.fetchone()
                if artist_data:
                    user['artist_profile'] = artist_data

                    # Get social media links if available
                    cursor.execute(
                        "SELECT SMLinks FROM Artist_SMLinks WHERE ArtistID = %s",
                        (artist_data['ArtistID'],)
                    )
                    sm_links = cursor.fetchone()
                    if sm_links:
                        user['artist_profile']['social_media_links'] = sm_links['SMLinks']

            return user

        except pymysql.Error:
            return None

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def update_user_profile(user_id, email=None, username=None, first_name=None, last_name=None):
        """
        Update user profile information

        Args:
            user_id (int): User's ID
            email (str): New email (optional)
            username (str): New username (optional)
            first_name (str): New first name (optional)
            last_name (str): New last name (optional)

        Returns:
            tuple: (success: bool, result: dict/str)
                - On success: (True, updated_user_dict)
                - On failure: (False, error_message)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Check if user exists
            cursor.execute("SELECT UserID FROM User WHERE UserID = %s", (user_id,))
            if not cursor.fetchone():
                return False, "User not found"

            # Check if new email is already taken by another user
            if email:
                cursor.execute(
                    "SELECT UserID FROM User WHERE Email = %s AND UserID != %s",
                    (email, user_id)
                )
                if cursor.fetchone():
                    return False, "Email already in use by another account"

            # Check if new username is already taken by another user
            if username:
                cursor.execute(
                    "SELECT UserID FROM User WHERE Username = %s AND UserID != %s",
                    (username, user_id)
                )
                if cursor.fetchone():
                    return False, "Username already taken by another account"

            # Build update query dynamically
            update_fields = []
            values = []

            if email is not None:
                update_fields.append("Email = %s")
                values.append(email)

            if username is not None:
                update_fields.append("Username = %s")
                values.append(username)

            if first_name is not None:
                update_fields.append("FirstName = %s")
                values.append(first_name)

            if last_name is not None:
                update_fields.append("LastName = %s")
                values.append(last_name)

            if not update_fields:
                return False, "No fields to update"

            # Execute update
            values.append(user_id)
            update_query = f"UPDATE User SET {', '.join(update_fields)} WHERE UserID = %s"
            cursor.execute(update_query, values)
            connection.commit()

            # Fetch and return updated user
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
    def change_password(user_id, current_password, new_password):
        """
        Change user password

        Args:
            user_id (int): User's ID
            current_password (str): Current password
            new_password (str): New password

        Returns:
            tuple: (success: bool, message: str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Get current password hash
            cursor.execute("SELECT Password FROM User WHERE UserID = %s", (user_id,))
            user = cursor.fetchone()

            if not user:
                return False, "User not found"

            # Verify current password
            if not verify_password(current_password, user['Password']):
                return False, "Current password is incorrect"

            # Hash and update new password
            new_password_hash = hash_password(new_password)
            cursor.execute(
                "UPDATE User SET Password = %s WHERE UserID = %s",
                (new_password_hash, user_id)
            )
            connection.commit()

            return True, "Password changed successfully"

        except pymysql.Error as e:
            if connection:
                connection.rollback()
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def delete_user(user_id):
        """
        Delete a user account (soft delete or hard delete based on requirements)

        Args:
            user_id (int): User's ID

        Returns:
            tuple: (success: bool, message: str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Check if user exists
            cursor.execute("SELECT UserID FROM User WHERE UserID = %s", (user_id,))
            if not cursor.fetchone():
                return False, "User not found"

            # Delete user (cascade will handle related records)
            cursor.execute("DELETE FROM User WHERE UserID = %s", (user_id,))
            connection.commit()

            return True, "Account deleted successfully"

        except pymysql.Error as e:
            if connection:
                connection.rollback()
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()
