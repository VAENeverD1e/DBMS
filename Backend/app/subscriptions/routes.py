"""
Subscription routes for managing user subscriptions
"""
from flask import Blueprint, request, jsonify
from app.utils.decorators import login_required, guest_optional
from .services import SubscriptionService
from .subscription_service import IntegratedSubscriptionService


# Create Blueprint
subscriptions_bp = Blueprint('subscriptions', __name__, url_prefix='/api/subscriptions')


@subscriptions_bp.route('/me', methods=['GET'])
@login_required
def get_my_subscription(user_id):
    """
    Get current user's active subscription

    Returns:
        200: Subscription details
        401: Not authenticated
        404: No active subscription
        500: Server error
    """
    try:
        success, result = SubscriptionService.get_user_subscription(user_id)

        if not success:
            status_code = 404 if 'not found' in result.lower() else 500
            return jsonify({'error': result}), status_code

        return jsonify({'subscription': result}), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@subscriptions_bp.route('/me/history', methods=['GET'])
@login_required
def get_subscription_history(user_id):
    """
    Get current user's subscription history

    Query Parameters:
        limit (int): Number of records to return (default: 10)
        offset (int): Offset for pagination (default: 0)

    Returns:
        200: Subscription history
        401: Not authenticated
        500: Server error
    """
    try:
        limit = request.args.get('limit', 10, type=int)
        offset = request.args.get('offset', 0, type=int)

        # Validate pagination parameters
        if limit < 1 or limit > 100:
            return jsonify({'error': 'Limit must be between 1 and 100'}), 400

        if offset < 0:
            return jsonify({'error': 'Offset must be non-negative'}), 400

        success, result = SubscriptionService.get_subscription_history(user_id, limit, offset)

        if not success:
            return jsonify({'error': result}), 500

        return jsonify({
            'subscriptions': result,
            'pagination': {
                'limit': limit,
                'offset': offset,
                'count': len(result)
            }
        }), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@subscriptions_bp.route('/me/cancel', methods=['POST'])
@login_required
def cancel_subscription(user_id):
    """
    Cancel current user's active subscription

    Returns:
        200: Subscription cancelled successfully
        401: Not authenticated
        404: No active subscription to cancel
        500: Server error
    """
    try:
        success, result = SubscriptionService.cancel_subscription(user_id)

        if not success:
            status_code = 404 if 'no active' in result.lower() else 500
            return jsonify({'error': result}), status_code

        # No session update needed (stateless JWT)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@subscriptions_bp.route('/me/status', methods=['GET'])
@login_required
def check_subscription_status(user_id):
    """
    Check if current user's subscription is still valid
    Auto-updates status if expired

    Returns:
        200: Subscription status
        401: Not authenticated
        500: Server error
    """
    try:
        success, result = SubscriptionService.check_subscription_status(user_id)

        if not success:
            return jsonify({'error': result}), 500

        # No session update needed (stateless JWT)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@subscriptions_bp.route('/subscribe', methods=['POST'])
@login_required
def subscribe_to_plan(user_id):
    """
    Subscribe to a plan with payment

    Request Body:
        {
            "plan_id": 1,
            "payment_method": "visa",
            "duration_months": 1,
            "card_number": "4242",  // optional - last 4 digits
            "card_holder_name": "John Doe"  // optional
        }

    Returns:
        201: Subscription created successfully
        400: Validation error
        401: Not authenticated
        500: Server error
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Request body is required'}), 400

        # Validate required fields
        if 'plan_id' not in data:
            return jsonify({'error': 'plan_id is required'}), 400

        if 'payment_method' not in data:
            return jsonify({'error': 'payment_method is required'}), 400

        plan_id = data['plan_id']
        payment_method = data['payment_method']
        duration_months = data.get('duration_months', 1)
        card_number = data.get('card_number')
        card_holder_name = data.get('card_holder_name')

        # Validate duration
        if duration_months not in [1, 3, 12]:
            return jsonify({'error': 'duration_months must be 1, 3, or 12'}), 400

        # Validate payment method
        if payment_method.lower() not in ['momo', 'visa', 'mastercard']:
            return jsonify({'error': 'payment_method must be momo, visa, or mastercard'}), 400

        # Card validation for non-momo payments
        if payment_method.lower() in ['visa', 'mastercard']:
            if not card_holder_name:
                return jsonify({'error': 'card_holder_name is required for card payments'}), 400

        # Create subscription
        success, result = IntegratedSubscriptionService.subscribe(
            user_id=user_id,
            subscription_id=plan_id,
            payment_method=payment_method,
            duration_months=duration_months,
            card_number=card_number,
            card_holder_name=card_holder_name
        )

        if not success:
            status_code = 404 if 'not found' in result.lower() else 500
            return jsonify({'error': result}), status_code

        return jsonify(result), 201

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@subscriptions_bp.route('/plans', methods=['GET'])
@guest_optional
def get_available_plans(user_id=None):
    """
    Get all available subscription plans

    Returns:
        200: List of available plans
        500: Server error
    """
    try:
        success, result = IntegratedSubscriptionService.get_available_plans()

        if not success:
            return jsonify({'error': result}), 500

        return jsonify({'plans': result}), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@subscriptions_bp.route('/me/active', methods=['GET'])
@login_required
def get_my_active_subscriptions(user_id):
    """
    Get current user's all active subscriptions

    Returns:
        200: List of active subscriptions
        401: Not authenticated
        500: Server error
    """
    try:
        success, result = IntegratedSubscriptionService.get_user_active_subscriptions(user_id)

        if not success:
            return jsonify({'error': result, 'subscriptions': []}), 200

        return jsonify({'subscriptions': result}), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
