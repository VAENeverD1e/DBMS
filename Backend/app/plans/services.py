"""
Plan service layer for subscription plan operations
"""
import pymysql
from app.auth.utils import get_db_connection


class PlanService:
    """Service class for plan operations"""

    @staticmethod
    def get_all_plans(active_only=True):
        """
        Get all subscription plans

        Args:
            active_only (bool): If True, only return active plans (not used in current schema)

        Returns:
            tuple: (success: bool, result: list/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            query = """
                SELECT
                    SubscriptionID,
                    Name,
                    Price,
                    Duration,
                    Type
                FROM Subscription
                ORDER BY Price ASC
            """

            cursor.execute(query)
            plans = cursor.fetchall()

            return True, plans

        except pymysql.Error as e:
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_plan_by_id(plan_id):
        """
        Get a specific plan by ID

        Args:
            plan_id (int): Subscription ID

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            query = """
                SELECT
                    SubscriptionID,
                    Name,
                    Price,
                    Duration,
                    Type
                FROM Subscription
                WHERE SubscriptionID = %s
            """

            cursor.execute(query, (plan_id,))
            plan = cursor.fetchone()

            if not plan:
                return False, "Plan not found"

            return True, plan

        except pymysql.Error as e:
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def create_plan(name, price, duration_days, plan_type):
        """
        Create a new subscription plan (Admin only)

        Args:
            name (str): Plan name
            price (float): Plan price
            duration_days (int): Plan duration in days
            plan_type (str): Plan type ('Listener' or 'Artist')

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Check if plan with same name exists
            cursor.execute("SELECT SubscriptionID FROM Subscription WHERE Name = %s", (name,))
            if cursor.fetchone():
                return False, "Plan with this name already exists"

            # Insert new plan
            query = """
                INSERT INTO Subscription (Name, Price, Duration, Type)
                VALUES (%s, %s, %s, %s)
            """

            cursor.execute(query, (name, price, duration_days, plan_type))
            plan_id = cursor.lastrowid
            connection.commit()

            # Fetch created plan
            cursor.execute(
                """
                SELECT
                    SubscriptionID,
                    Name,
                    Price,
                    Duration,
                    Type
                FROM Subscription
                WHERE SubscriptionID = %s
                """,
                (plan_id,)
            )
            plan = cursor.fetchone()

            return True, plan

        except pymysql.Error as e:
            if connection:
                connection.rollback()
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def update_plan(plan_id, name=None, price=None, duration_days=None, plan_type=None):
        """
        Update an existing plan (Admin only)

        Args:
            plan_id (int): Subscription ID
            name (str): New plan name (optional)
            price (float): New price (optional)
            duration_days (int): New duration (optional)
            plan_type (str): New plan type (optional)

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Check if plan exists
            cursor.execute("SELECT SubscriptionID FROM Subscription WHERE SubscriptionID = %s", (plan_id,))
            if not cursor.fetchone():
                return False, "Plan not found"

            # Build update query
            update_fields = []
            values = []

            if name is not None:
                update_fields.append("Name = %s")
                values.append(name)

            if price is not None:
                update_fields.append("Price = %s")
                values.append(price)

            if duration_days is not None:
                update_fields.append("Duration = %s")
                values.append(duration_days)

            if plan_type is not None:
                update_fields.append("Type = %s")
                values.append(plan_type)

            if not update_fields:
                return False, "No fields to update"

            values.append(plan_id)
            query = f"UPDATE Subscription SET {', '.join(update_fields)} WHERE SubscriptionID = %s"

            cursor.execute(query, values)
            connection.commit()

            # Fetch updated plan
            cursor.execute(
                """
                SELECT
                    SubscriptionID,
                    Name,
                    Price,
                    Duration,
                    Type
                FROM Subscription
                WHERE SubscriptionID = %s
                """,
                (plan_id,)
            )
            plan = cursor.fetchone()

            return True, plan

        except pymysql.Error as e:
            if connection:
                connection.rollback()
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def delete_plan(plan_id):
        """
        Delete a plan (hard delete from database)

        Args:
            plan_id (int): Subscription ID

        Returns:
            tuple: (success: bool, result: str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Check if plan exists
            cursor.execute("SELECT SubscriptionID FROM Subscription WHERE SubscriptionID = %s", (plan_id,))
            if not cursor.fetchone():
                return False, "Plan not found"

            # Hard delete
            cursor.execute("DELETE FROM Subscription WHERE SubscriptionID = %s", (plan_id,))
            connection.commit()

            return True, "Plan deleted successfully"

        except pymysql.Error as e:
            if connection:
                connection.rollback()
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()
