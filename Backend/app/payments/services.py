"""
Payment service layer for managing payment methods and orders
"""
import pymysql
from datetime import datetime
from app.auth.utils import get_db_connection


class PaymentService:
    """Service class for payment and order operations"""

    @staticmethod
    def create_order_with_payment(user_id, subscription_id, payment_method, amount):
        """
        Create an order and payment record

        Args:
            user_id (int): User's ID
            subscription_id (int): Subscription ID (plan)
            payment_method (str): Payment method ('Credit Card', 'PayPal', etc.)
            amount (float): Payment amount

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            # Validate payment method
            valid_methods = ['Credit Card', 'PayPal', 'momo', 'visa', 'mastercard']
            if payment_method.lower() not in [m.lower() for m in valid_methods]:
                return False, f"Invalid payment method"

            # Create order record
            order_query = """
                INSERT INTO Orders (UserID, SubscriptionID, OrderDate)
                VALUES (%s, %s, %s)
            """
            order_date = datetime.now()
            cursor.execute(order_query, (user_id, subscription_id, order_date))
            order_id = cursor.lastrowid

            # Create payment record
            payment_query = """
                INSERT INTO Payment (OrderID, Method, Status, Amount)
                VALUES (%s, %s, 'Completed', %s)
            """
            cursor.execute(payment_query, (order_id, payment_method, amount))
            payment_id = cursor.lastrowid

            connection.commit()

            # Fetch created payment with order details
            cursor.execute(
                """
                SELECT
                    p.PaymentID,
                    p.OrderID,
                    p.Method,
                    p.Status,
                    p.Amount,
                    o.UserID,
                    o.SubscriptionID,
                    o.OrderDate
                FROM Payment p
                JOIN Orders o ON p.OrderID = o.OrderID
                WHERE p.PaymentID = %s
                """,
                (payment_id,)
            )
            payment_data = cursor.fetchone()

            return True, {'payment': payment_data, 'order_id': order_id, 'payment_id': payment_id}

        except pymysql.Error as e:
            if connection:
                connection.rollback()
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_payment_by_id(payment_id):
        """
        Get payment by ID

        Args:
            payment_id (int): Payment ID

        Returns:
            tuple: (success: bool, result: dict/str)
        """
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            query = """
                SELECT
                    p.PaymentID,
                    p.OrderID,
                    p.Method,
                    p.Status,
                    p.Amount,
                    o.UserID,
                    o.SubscriptionID,
                    o.OrderDate
                FROM Payment p
                JOIN Orders o ON p.OrderID = o.OrderID
                WHERE p.PaymentID = %s
            """

            cursor.execute(query, (payment_id,))
            payment = cursor.fetchone()

            if not payment:
                return False, "Payment not found"

            return True, payment

        except pymysql.Error as e:
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_user_payments(user_id, limit=10, offset=0):
        """
        Get user's payment history

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

            query = """
                SELECT
                    p.PaymentID,
                    p.Method,
                    p.Status,
                    p.Amount,
                    o.OrderID,
                    o.SubscriptionID,
                    o.OrderDate,
                    s.Name as SubscriptionName
                FROM Payment p
                JOIN Orders o ON p.OrderID = o.OrderID
                LEFT JOIN Subscription s ON o.SubscriptionID = s.SubscriptionID
                WHERE o.UserID = %s
                ORDER BY o.OrderDate DESC
                LIMIT %s OFFSET %s
            """

            cursor.execute(query, (user_id, limit, offset))
            payments = cursor.fetchall()

            return True, payments

        except pymysql.Error as e:
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_user_orders(user_id, limit=10, offset=0):
        """
        Get user's order history

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
                    o.OrderID,
                    o.UserID,
                    o.SubscriptionID,
                    o.OrderDate,
                    s.Name as SubscriptionName,
                    s.Price,
                    s.Duration,
                    s.Type,
                    p.PaymentID,
                    p.Method as PaymentMethod,
                    p.Status as PaymentStatus,
                    p.Amount
                FROM Orders o
                JOIN Subscription s ON o.SubscriptionID = s.SubscriptionID
                LEFT JOIN Payment p ON o.OrderID = p.OrderID
                WHERE o.UserID = %s
                ORDER BY o.OrderDate DESC
                LIMIT %s OFFSET %s
            """

            cursor.execute(query, (user_id, limit, offset))
            orders = cursor.fetchall()

            return True, orders

        except pymysql.Error as e:
            return False, f"Database error: {str(e)}"

        finally:
            if connection:
                cursor.close()
                connection.close()
