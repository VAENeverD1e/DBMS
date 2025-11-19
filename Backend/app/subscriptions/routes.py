"""
Subscription routes for managing user subscriptions
"""
from flask import Blueprint, request, jsonify
from app.utils.decorators import login_required
from .services import SubscriptionService


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
