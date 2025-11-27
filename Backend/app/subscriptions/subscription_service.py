"""
Integrated subscription service combining plans (Subscription), orders, payments, and user subscriptions
Based on actual database schema: Subscription, Orders, Payment, UserSubscription tables
"""
import pymysql
from datetime import datetime, timedelta
from app.auth.utils import get_db_connection
from app.plans.services import PlanService
from app.payments.services import PaymentService
from app.utils.common import info, debug, error


class IntegratedSubscriptionService:
    """Integrated service for managing the complete subscription flow"""

    @staticmethod
    def subscribe(user_id, subscription_id, payment_method, duration_months=1, card_number=None, card_holder_name=None):
        """
        Complete subscription flow: create order, payment, and user subscription

        Args:
            user_id (int): User's ID
            subscription_id (int): Subscription ID (plan) from Subscription table
            payment_method (str): Payment method ('momo', 'visa', 'mastercard', 'Credit Card', 'PayPal')
            duration_months (int): Subscription duration in months (1, 3, or 12)

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            # Get plan details first
            success, plan = PlanService.get_plan_by_id(subscription_id)
            if not success:
                return False, plan

            # Calculate total amount based on plan price and duration
            base_price = float(plan['Price'])

            # Apply discounts for longer subscriptions
            price_multipliers = {
                1: 1.0,      # 1 month - full price
                3: 2.75,     # 3 months - ~8% discount
                12: 10.0     # 12 months - ~17% discount
            }

            multiplier = price_multipliers.get(duration_months, 1.0)
            total_amount = base_price * multiplier

            # Start transaction
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Step 1: Create Order record
            order_query = """
                INSERT INTO Orders (UserID, SubscriptionID, OrderDate)
                VALUES (%s, %s, %s)
            """
            order_date = datetime.now()
            cursor.execute(order_query, (user_id, subscription_id, order_date))
            order_id = cursor.lastrowid

            # Step 2: Create Payment record
            payment_query = """
                INSERT INTO Payment (OrderID, Method, Status, Amount)
                VALUES (%s, %s, 'Completed', %s)
            """
            cursor.execute(payment_query, (order_id, payment_method, total_amount))
            payment_id = cursor.lastrowid

            # Step 3: Calculate subscription dates
            start_date = datetime.now().date()
            duration_days = plan['Duration'] * duration_months
            end_date = start_date + timedelta(days=duration_days) if duration_days else None

            # Determine plan type early (used below when checking for same-type active subscriptions)
            plan_type = plan.get('Type')

            # Step 4: Check if user has active subscription of the same type
            cursor.execute(
                """
                SELECT us.UserID, us.SubscriptionID, us.Status, s.Type
                FROM UserSubscription us
                JOIN Subscription s ON us.SubscriptionID = s.SubscriptionID
                WHERE us.UserID = %s AND us.Status = 'Active' AND s.Type = %s
                LIMIT 1
                """,
                (user_id, plan_type)
            )
            
            active_sub = cursor.fetchone()

            # Log the result of the active-subscription lookup
            try:
                debug('Checked for existing active subscription of same type', extra={
                    'user_id': user_id,
                    'subscription_id': subscription_id,
                    'plan_type': plan_type,
                    'active_sub': active_sub
                })
            except Exception:
                # don't let logging errors disrupt the flow
                pass

            if active_sub:
                # Cancel existing subscription of the same type using composite key
                cursor.execute(
                    """
                    UPDATE UserSubscription
                    SET Status = 'Cancelled'
                    WHERE UserID = %s AND SubscriptionID = %s
                    """,
                    (active_sub['UserID'], active_sub['SubscriptionID'])
                )

            # Step 5: Check if this user+subscription combination exists
            cursor.execute(
                """
                SELECT UserID, SubscriptionID FROM UserSubscription
                WHERE UserID = %s AND SubscriptionID = %s
                """,
                (user_id, subscription_id)
            )
            existing_record = cursor.fetchone()

            if existing_record:
                # Update existing record
                cursor.execute(
                    """
                    UPDATE UserSubscription
                    SET Status = 'Active', StartDate = %s
                    WHERE UserID = %s AND SubscriptionID = %s
                    """,
                    (start_date, user_id, subscription_id)
                )
            else:
                # Create new UserSubscription (composite key: UserID + SubscriptionID)
                user_sub_query = """
                    INSERT INTO UserSubscription (UserID, SubscriptionID, Status, StartDate)
                    VALUES (%s, %s, 'Active', %s)
                """
                cursor.execute(user_sub_query, (user_id, subscription_id, start_date))

            # Step 6: Upgrade user role based on plan type
            plan_type = plan['Type']  # 'Listener' or 'Artist'

            # Update user role
            cursor.execute("UPDATE User SET Role = %s WHERE UserID = %s", (plan_type, user_id))

            # Create Listener or Artist record if doesn't exist
            if plan_type == 'Listener':
                cursor.execute("SELECT ListenerID FROM Listener WHERE UserID = %s", (user_id,))
                if not cursor.fetchone():
                    cursor.execute("INSERT INTO Listener (UserID) VALUES (%s)", (user_id,))
            elif plan_type == 'Artist':
                cursor.execute("SELECT ArtistID FROM Artist WHERE UserID = %s", (user_id,))
                if not cursor.fetchone():
                    cursor.execute(
                        "INSERT INTO Artist (UserID, VerifiedStatus) VALUES (%s, 'Pending')",
                        (user_id,)
                    )

            # Commit transaction
            connection.commit()

            # Step 7: Fetch complete subscription details using composite key
            cursor.execute(
                """
                SELECT
                    us.UserID,
                    us.SubscriptionID,
                    us.StartDate,
                    us.Status,
                    s.Name as PlanName,
                    s.Price as PlanPrice,
                    s.Duration as PlanDuration,
                    s.Type as PlanType,
                    o.OrderID,
                    o.OrderDate,
                    p.PaymentID,
                    p.Method as PaymentMethod,
                    p.Amount as TotalAmount,
                    p.Status as PaymentStatus
                FROM UserSubscription us
                JOIN Subscription s ON us.SubscriptionID = s.SubscriptionID
                JOIN Orders o ON o.UserID = us.UserID AND o.SubscriptionID = us.SubscriptionID
                JOIN Payment p ON p.OrderID = o.OrderID
                WHERE us.UserID = %s AND us.SubscriptionID = %s
                ORDER BY o.OrderDate DESC
                LIMIT 1
                """,
                (user_id, subscription_id)
            )
            subscription_data = cursor.fetchone()

            return True, {
                'subscription': subscription_data,
                'message': f'Successfully subscribed to {plan["Name"]} plan',
                'duration_months': duration_months
            }

        except pymysql.Error as e:
            if connection:
                connection.rollback()
            return False, f"Database error: {str(e)}"

        except Exception as e:
            if connection:
                connection.rollback()
            return False, f"Error processing subscription: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_available_plans():
        """
        Get all available subscription plans

        Returns:
            tuple: (success: bool, result: list/str)
        """
        return PlanService.get_all_plans(active_only=True)

    @staticmethod
    def get_user_subscription(user_id):
        """
        Get user's active subscription with payment details

        Args:
            user_id (int): User's ID

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            query = """
                SELECT
                    us.UserID,
                    us.SubscriptionID,
                    us.StartDate,
                    us.Status,
                    s.Name as PlanName,
                    s.Price as PlanPrice,
                    s.Duration as PlanDuration,
                    s.Type as PlanType
                FROM UserSubscription us
                JOIN Subscription s ON us.SubscriptionID = s.SubscriptionID
                WHERE us.UserID = %s AND us.Status = 'Active'
                ORDER BY us.StartDate DESC
                LIMIT 1
            """

            cursor.execute(query, (user_id,))
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
    def get_user_active_subscriptions(user_id):
        """
        Get all user's active subscriptions (can have both Listener and Artist)

        Args:
            user_id (int): User's ID

        Returns:
            tuple: (success: bool, result: list/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            query = """
                SELECT
                    us.UserID,
                    us.SubscriptionID,
                    us.StartDate,
                    us.Status,
                    s.Name as PlanName,
                    s.Price as PlanPrice,
                    s.Duration as PlanDuration,
                    s.Type as PlanType
                FROM UserSubscription us
                JOIN Subscription s ON us.SubscriptionID = s.SubscriptionID
                WHERE us.UserID = %s AND us.Status = 'Active'
                ORDER BY us.StartDate DESC
            """

            cursor.execute(query, (user_id,))
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

            # Get active subscription using composite key
            cursor.execute(
                """
                SELECT UserID, SubscriptionID
                FROM UserSubscription
                WHERE UserID = %s AND Status = 'Active'
                ORDER BY StartDate DESC
                LIMIT 1
                """,
                (user_id,)
            )
            subscription = cursor.fetchone()

            if not subscription:
                return False, "No active subscription to cancel"

            # Update subscription status using composite key
            cursor.execute(
                """
                UPDATE UserSubscription
                SET Status = 'Cancelled'
                WHERE UserID = %s AND SubscriptionID = %s
                """,
                (subscription['UserID'], subscription['SubscriptionID'])
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
    def get_subscription_history(user_id, limit=10, offset=0):
        """
        Get user's subscription history with order and payment details

        Args:
            user_id (int): User's ID
            limit (int): Number of records
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
                    us.UserID,
                    us.SubscriptionID,
                    us.StartDate,
                    us.Status,
                    s.Name as PlanName,
                    s.Price as PlanPrice,
                    s.Type as PlanType,
                    o.OrderID,
                    o.OrderDate,
                    p.PaymentID,
                    p.Method as PaymentMethod,
                    p.Amount as TotalAmount,
                    p.Status as PaymentStatus
                FROM UserSubscription us
                JOIN Subscription s ON us.SubscriptionID = s.SubscriptionID
                LEFT JOIN Orders o ON o.UserID = us.UserID AND o.SubscriptionID = us.SubscriptionID
                LEFT JOIN Payment p ON p.OrderID = o.OrderID
                WHERE us.UserID = %s
                ORDER BY us.StartDate DESC
                LIMIT %s OFFSET %s
            """

            cursor.execute(query, (user_id, limit, offset))
            subscriptions = cursor.fetchall()

            return True, subscriptions

        except pymysql.Error as e:
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()
