"""
Plan routes for subscription plan operations
"""
from flask import request, jsonify
from app.utils.decorators import guest_optional, login_required
from .services import PlanService
from .schemas import validate_plan_creation
from . import plans_bp


@plans_bp.route('', methods=['GET'])
@guest_optional
def get_all_plans(user_id=None):
    """
    Get all available subscription plans

    Query Parameters:
        include_inactive (bool): Include inactive plans (default: False)

    Returns:
        200: List of plans
        500: Server error
    """
    try:
        include_inactive = request.args.get('include_inactive', 'false').lower() == 'true'
        active_only = not include_inactive

        success, result = PlanService.get_all_plans(active_only=active_only)

        if not success:
            return jsonify({'error': result}), 500

        return jsonify({'plans': result}), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@plans_bp.route('/<int:plan_id>', methods=['GET'])
@guest_optional
def get_plan(plan_id, user_id=None):
    """
    Get a specific plan by ID

    Returns:
        200: Plan details
        404: Plan not found
        500: Server error
    """
    try:
        success, result = PlanService.get_plan_by_id(plan_id)

        if not success:
            status_code = 404 if 'not found' in result.lower() else 500
            return jsonify({'error': result}), status_code

        return jsonify({'plan': result}), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@plans_bp.route('', methods=['POST'])
@login_required
def create_plan(user_id):
    """
    Create a new subscription plan (Admin only - to be implemented)

    Request Body:
        {
            "name": "Listener Monthly",
            "description": "Monthly subscription for listeners",
            "price": 9.99,
            "duration_days": 30,
            "role_granted": "Listener"
        }

    Returns:
        201: Plan created successfully
        400: Validation error
        401: Not authenticated
        500: Server error
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Request body is required'}), 400

        # Validate request data
        is_valid, errors = validate_plan_creation(data)
        if not is_valid:
            return jsonify({'error': 'Validation failed', 'details': errors}), 400

        # Create plan
        success, result = PlanService.create_plan(
            name=data['name'],
            price=data['price'],
            duration_days=data['duration_days'],
            role_granted=data['role_granted'],
            description=data.get('description')
        )

        if not success:
            status_code = 409 if 'already exists' in result.lower() else 500
            return jsonify({'error': result}), status_code

        return jsonify({'message': 'Plan created successfully', 'plan': result}), 201

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@plans_bp.route('/<int:plan_id>', methods=['PUT', 'PATCH'])
@login_required
def update_plan(plan_id, user_id):
    """
    Update an existing plan (Admin only - to be implemented)

    Request Body:
        {
            "name": "New Name",  // optional
            "description": "New Description",  // optional
            "price": 14.99,  // optional
            "duration_days": 30,  // optional
            "is_active": true  // optional
        }

    Returns:
        200: Plan updated successfully
        400: Validation error
        401: Not authenticated
        404: Plan not found
        500: Server error
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Request body is required'}), 400

        # Update plan
        success, result = PlanService.update_plan(
            plan_id=plan_id,
            name=data.get('name'),
            description=data.get('description'),
            price=data.get('price'),
            duration_days=data.get('duration_days'),
            is_active=data.get('is_active')
        )

        if not success:
            status_code = 404 if 'not found' in result.lower() else 500
            return jsonify({'error': result}), status_code

        return jsonify({'message': 'Plan updated successfully', 'plan': result}), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@plans_bp.route('/<int:plan_id>', methods=['DELETE'])
@login_required
def delete_plan(plan_id, user_id):
    """
    Deactivate a plan (Admin only - to be implemented)

    Returns:
        200: Plan deactivated successfully
        401: Not authenticated
        404: Plan not found
        500: Server error
    """
    try:
        success, result = PlanService.delete_plan(plan_id)

        if not success:
            status_code = 404 if 'not found' in result.lower() else 500
            return jsonify({'error': result}), status_code

        return jsonify({'message': result}), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
