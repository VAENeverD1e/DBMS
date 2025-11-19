"""
Subscription service layer for managing user subscriptions
"""
import pymysql
from datetime import datetime, timedelta
from flask import current_app
from app.auth.utils import get_db_connection


class SubscriptionService:
    """Service class for subscription operations"""

    @staticmethod
    def create_subscription(user_id, plan_id, payment_id):
        """
        Create a new subscription after successful payment

        Args:
            user_id (int): User's ID
            plan_id (int): Plan's ID
            payment_id (int): Payment's ID

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Get plan details
            cursor.execute(
                "SELECT PlanID, PlanName, PlanType, Duration FROM Plan WHERE PlanID = %s",
                (plan_id,)
            )
            plan = cursor.fetchone()

            if not plan:
                return False, "Plan not found"

            # Calculate subscription end date based on plan duration
            start_date = datetime.now()
            if plan['Duration']:
                # Duration is in days
                end_date = start_date + timedelta(days=plan['Duration'])
            else:
                # Lifetime subscription
                end_date = None

            # Create subscription
            cursor.execute(
                """
                INSERT INTO Subscription (UserID, PlanID, PaymentID, StartDate, EndDate, Status)
                VALUES (%s, %s, %s, %s, %s, 'Active')
                """,
                (user_id, plan_id, payment_id, start_date, end_date)
            )
            subscription_id = cursor.lastrowid

            # Upgrade user role based on plan type
            if plan['PlanType'] == 'Listener':
                # Update user role to Listener
                cursor.execute("UPDATE User SET Role = 'Listener' WHERE UserID = %s", (user_id,))

                # Create Listener record if doesn't exist
                cursor.execute("SELECT ListenerID FROM Listener WHERE UserID = %s", (user_id,))
                if not cursor.fetchone():
                    cursor.execute("INSERT INTO Listener (UserID) VALUES (%s)", (user_id,))

            elif plan['PlanType'] == 'Artist':
                # Update user role to Artist
                cursor.execute("UPDATE User SET Role = 'Artist' WHERE UserID = %s", (user_id,))

                # Create Artist record if doesn't exist
                cursor.execute("SELECT ArtistID FROM Artist WHERE UserID = %s", (user_id,))
                if not cursor.fetchone():
                    cursor.execute(
                        "INSERT INTO Artist (UserID, VerifiedStatus) VALUES (%s, 'Pending')",
                        (user_id,)
                    )

            connection.commit()

            # Fetch created subscription
            cursor.execute(
                """
                SELECT
                    s.SubscriptionID,
                    s.UserID,
                    s.PlanID,
                    s.StartDate,
                    s.EndDate,
                    s.Status,
                    p.PlanName,
                    p.PlanType,
                    p.Price
                FROM Subscription s
                JOIN Plan p ON s.PlanID = p.PlanID
                WHERE s.SubscriptionID = %s
                """,
                (subscription_id,)
            )
            subscription = cursor.fetchone()

            return True, subscription

        except pymysql.Error as e:
            if connection:
                connection.rollback()
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_user_subscription(user_id):
        """
        Get user's active subscription

        Args:
            user_id (int): User's ID

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Get active subscription
            cursor.execute(
                """
                SELECT
                    s.SubscriptionID,
                    s.UserID,
                    s.PlanID,
                    s.StartDate,
                    s.EndDate,
                    s.Status,
                    p.PlanName,
                    p.PlanType,
                    p.Price,
                    p.Duration
                FROM Subscription s
                JOIN Plan p ON s.PlanID = p.PlanID
                WHERE s.UserID = %s AND s.Status = 'Active'
                ORDER BY s.StartDate DESC
                LIMIT 1
                """,
                (user_id,)
            )
            subscription = cursor.fetchone()

            if not subscription:
                return False, "No active subscription found"

            return True, subscription

        except pymysql.Error as e:
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_subscription_history(user_id, limit=10, offset=0):
        """
        Get user's subscription history

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

            # Get subscription history
            cursor.execute(
                """
                SELECT
                    s.SubscriptionID,
                    s.PlanID,
                    s.StartDate,
                    s.EndDate,
                    s.Status,
                    p.PlanName,
                    p.PlanType,
                    p.Price
                FROM Subscription s
                JOIN Plan p ON s.PlanID = p.PlanID
                WHERE s.UserID = %s
                ORDER BY s.StartDate DESC
                LIMIT %s OFFSET %s
                """,
                (user_id, limit, offset)
            )
            subscriptions = cursor.fetchall()

            return True, subscriptions

        except pymysql.Error as e:
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def cancel_subscription(user_id):
        """
        Cancel user's active subscription

        Args:
            user_id (int): User's ID

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Get active subscription
            cursor.execute(
                """
                SELECT SubscriptionID, PlanID
                FROM Subscription
                WHERE UserID = %s AND Status = 'Active'
                ORDER BY StartDate DESC
                LIMIT 1
                """,
                (user_id,)
            )
            subscription = cursor.fetchone()

            if not subscription:
                return False, "No active subscription to cancel"

            # Update subscription status to Cancelled
            cursor.execute(
                "UPDATE Subscription SET Status = 'Cancelled' WHERE SubscriptionID = %s",
                (subscription['SubscriptionID'],)
            )

            # Downgrade user role to Guest
            cursor.execute("UPDATE User SET Role = 'Guest' WHERE UserID = %s", (user_id,))

            connection.commit()

            return True, {'message': 'Subscription cancelled successfully'}

        except pymysql.Error as e:
            if connection:
                connection.rollback()
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def check_subscription_status(user_id):
        """
        Check if user's subscription is still valid (not expired)
        Auto-update status if expired

        Args:
            user_id (int): User's ID

        Returns:
            tuple: (success: bool, result: dict/str)
                result dict contains: {'is_active': bool, 'subscription': dict or None}
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Get active subscription
            cursor.execute(
                """
                SELECT
                    s.SubscriptionID,
                    s.EndDate,
                    s.Status,
                    p.PlanName,
                    p.PlanType
                FROM Subscription s
                JOIN Plan p ON s.PlanID = p.PlanID
                WHERE s.UserID = %s AND s.Status = 'Active'
                ORDER BY s.StartDate DESC
                LIMIT 1
                """,
                (user_id,)
            )
            subscription = cursor.fetchone()

            if not subscription:
                return True, {'is_active': False, 'subscription': None}

            # Check if subscription has expired
            if subscription['EndDate']:
                current_time = datetime.now()
                end_date = subscription['EndDate']

                if current_time > end_date:
                    # Subscription has expired - update status
                    cursor.execute(
                        "UPDATE Subscription SET Status = 'Expired' WHERE SubscriptionID = %s",
                        (subscription['SubscriptionID'],)
                    )

                    # Downgrade user role to Guest
                    cursor.execute("UPDATE User SET Role = 'Guest' WHERE UserID = %s", (user_id,))

                    connection.commit()

                    return True, {
                        'is_active': False,
                        'subscription': None,
                        'message': 'Subscription has expired'
                    }

            # Subscription is still active
            return True, {'is_active': True, 'subscription': subscription}

        except pymysql.Error as e:
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()
