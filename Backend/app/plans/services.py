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
            active_only (bool): If True, only return active plans

        Returns:
            tuple: (success: bool, result: list/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            if active_only:
                query = """
                    SELECT
                        PlanID,
                        Name,
                        Description,
                        Price,
                        DurationDays,
                        RoleGranted,
                        IsActive,
                        CreatedAt
                    FROM Plan
                    WHERE IsActive = TRUE
                    ORDER BY Price ASC
                """
            else:
                query = """
                    SELECT
                        PlanID,
                        Name,
                        Description,
                        Price,
                        DurationDays,
                        RoleGranted,
                        IsActive,
                        CreatedAt
                    FROM Plan
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
            plan_id (int): Plan ID

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            query = """
                SELECT
                    PlanID,
                    Name,
                    Description,
                    Price,
                    DurationDays,
                    RoleGranted,
                    IsActive,
                    CreatedAt
                FROM Plan
                WHERE PlanID = %s
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
    def create_plan(name, price, duration_days, role_granted, description=None):
        """
        Create a new subscription plan (Admin only)

        Args:
            name (str): Plan name
            price (float): Plan price
            duration_days (int): Plan duration in days
            role_granted (str): Role granted ('Listener' or 'Artist')
            description (str): Plan description (optional)

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Check if plan with same name exists
            cursor.execute("SELECT PlanID FROM Plan WHERE Name = %s", (name,))
            if cursor.fetchone():
                return False, "Plan with this name already exists"

            # Insert new plan
            query = """
                INSERT INTO Plan (Name, Description, Price, DurationDays, RoleGranted)
                VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(query, (name, description, price, duration_days, role_granted))
            plan_id = cursor.lastrowid
            connection.commit()

            # Fetch created plan
            cursor.execute(
                """
                SELECT
                    PlanID,
                    Name,
                    Description,
                    Price,
                    DurationDays,
                    RoleGranted,
                    IsActive,
                    CreatedAt
                FROM Plan
                WHERE PlanID = %s
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
    def update_plan(plan_id, name=None, description=None, price=None, duration_days=None, is_active=None):
        """
        Update an existing plan (Admin only)

        Args:
            plan_id (int): Plan ID
            name (str): New plan name (optional)
            description (str): New description (optional)
            price (float): New price (optional)
            duration_days (int): New duration (optional)
            is_active (bool): Active status (optional)

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Check if plan exists
            cursor.execute("SELECT PlanID FROM Plan WHERE PlanID = %s", (plan_id,))
            if not cursor.fetchone():
                return False, "Plan not found"

            # Build update query
            update_fields = []
            values = []

            if name is not None:
                update_fields.append("Name = %s")
                values.append(name)

            if description is not None:
                update_fields.append("Description = %s")
                values.append(description)

            if price is not None:
                update_fields.append("Price = %s")
                values.append(price)

            if duration_days is not None:
                update_fields.append("DurationDays = %s")
                values.append(duration_days)

            if is_active is not None:
                update_fields.append("IsActive = %s")
                values.append(is_active)

            if not update_fields:
                return False, "No fields to update"

            values.append(plan_id)
            query = f"UPDATE Plan SET {', '.join(update_fields)} WHERE PlanID = %s"

            cursor.execute(query, values)
            connection.commit()

            # Fetch updated plan
            cursor.execute(
                """
                SELECT
                    PlanID,
                    Name,
                    Description,
                    Price,
                    DurationDays,
                    RoleGranted,
                    IsActive,
                    CreatedAt
                FROM Plan
                WHERE PlanID = %s
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
        Soft delete a plan (set IsActive = FALSE)

        Args:
            plan_id (int): Plan ID

        Returns:
            tuple: (success: bool, result: str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Check if plan exists
            cursor.execute("SELECT PlanID FROM Plan WHERE PlanID = %s", (plan_id,))
            if not cursor.fetchone():
                return False, "Plan not found"

            # Soft delete (set IsActive = FALSE)
            cursor.execute("UPDATE Plan SET IsActive = FALSE WHERE PlanID = %s", (plan_id,))
            connection.commit()

            return True, "Plan deactivated successfully"

        except pymysql.Error as e:
            if connection:
                connection.rollback()
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()
