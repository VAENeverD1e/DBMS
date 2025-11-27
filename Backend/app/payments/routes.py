"""
Payment routes for managing payment methods and history
"""
from flask import Blueprint, request, jsonify
from app.utils.decorators import login_required
from .services import PaymentService
from .schemas import validate_payment_creation


# Create Blueprint
payments_bp = Blueprint('payments', __name__, url_prefix='/api/payments')


@payments_bp.route('/me', methods=['GET'])
@login_required
def get_my_payments(user_id):
    """
    Get current user's payment history

    Query Parameters:
        limit (int): Number of records to return (default: 10)
        offset (int): Offset for pagination (default: 0)

    Returns:
        200: Payment history
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

        success, result = PaymentService.get_user_payments(user_id, limit, offset)

        if not success:
            return jsonify({'error': result}), 500

        return jsonify({
            'payments': result,
            'pagination': {
                'limit': limit,
                'offset': offset,
                'count': len(result)
            }
        }), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@payments_bp.route('/<int:payment_id>', methods=['GET'])
@login_required
def get_payment(payment_id, user_id):
    """
    Get a specific payment by ID

    Returns:
        200: Payment details
        401: Not authenticated
        404: Payment not found
        500: Server error
    """
    try:
        success, result = PaymentService.get_payment_by_id(payment_id)

        if not success:
            status_code = 404 if 'not found' in result.lower() else 500
            return jsonify({'error': result}), status_code

        # Ensure user owns this payment
        if result['UserID'] != user_id:
            return jsonify({'error': 'Unauthorized access to payment'}), 403

        return jsonify({'payment': result}), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
