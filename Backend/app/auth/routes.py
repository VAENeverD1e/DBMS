"""
Authentication routes for user registration, login, and profile management
"""
from flask import Blueprint, request, jsonify, session
from .services import AuthService
from .schemas import (
    validate_registration_data,
    validate_login_data,
    validate_profile_update_data,
    validate_password_change_data
)
from .utils import login_required, get_current_user, create_session, clear_session


# Create Blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user

    Request Body:
        {
            "email": "user@example.com",
            "password": "SecurePass123",
            "username": "johndoe",
            "first_name": "John",  // optional
            "last_name": "Doe",  // optional
            "role": "Guest"  // optional, defaults to "Guest"
        }

    Returns:
        201: User created successfully
        400: Validation error
        409: Email or username already exists
        500: Server error
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Request body is required'}), 400

        # Validate request data
        is_valid, errors = validate_registration_data(data)
        if not is_valid:
            return jsonify({'error': 'Validation failed', 'details': errors}), 400

        # Register user
        success, result = AuthService.register_user(
            email=data['email'],
            password=data['password'],
            username=data['username'],
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            role=data.get('role', 'Guest')
        )

        if not success:
            status_code = 409 if 'already' in result else 500
            return jsonify({'error': result}), status_code

        # Create session for the new user
        create_session(result)

        return jsonify({
            'message': 'User registered successfully',
            'user': {
                'user_id': result['UserID'],
                'email': result['Email'],
                'username': result['Username'],
                'first_name': result['FirstName'],
                'last_name': result['LastName'],
                'role': result['Role']
            }
        }), 201

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user

    Request Body:
        {
            "email": "user@example.com",  // OR "username": "johndoe"
            "password": "SecurePass123"
        }

    Returns:
        200: Login successful
        400: Validation error
        401: Invalid credentials
        500: Server error
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Request body is required'}), 400

        # Validate request data
        is_valid, errors = validate_login_data(data)
        if not is_valid:
            return jsonify({'error': 'Validation failed', 'details': errors}), 400

        # Get login identifier (email or username)
        login_identifier = data.get('email') or data.get('username')

        # Authenticate user
        success, result = AuthService.login_user(login_identifier, data['password'])

        if not success:
            return jsonify({'error': result}), 401

        # Create session
        create_session(result)

        return jsonify({
            'message': 'Login successful',
            'user': {
                'user_id': result['UserID'],
                'email': result['Email'],
                'username': result['Username'],
                'first_name': result['FirstName'],
                'last_name': result['LastName'],
                'role': result['Role']
            }
        }), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """
    Logout current user

    Returns:
        200: Logout successful
        401: Not authenticated
    """
    try:
        clear_session()
        return jsonify({'message': 'Logout successful'}), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@auth_bp.route('/me', methods=['GET'])
@login_required
def get_profile():
    """
    Get current user's profile

    Returns:
        200: Profile data
        401: Not authenticated
        404: User not found
        500: Server error
    """
    try:
        user_id = session.get('user_id')

        # Get detailed profile
        profile = AuthService.get_user_profile(user_id)

        if not profile:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({
            'user': profile
        }), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@auth_bp.route('/me', methods=['PUT', 'PATCH'])
@login_required
def update_profile():
    """
    Update current user's profile

    Request Body:
        {
            "email": "newemail@example.com",  // optional
            "username": "newusername",  // optional
            "first_name": "NewFirstName",  // optional
            "last_name": "NewLastName"  // optional
        }

    Returns:
        200: Profile updated successfully
        400: Validation error
        401: Not authenticated
        409: Email or username already exists
        500: Server error
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Request body is required'}), 400

        # Validate request data
        is_valid, errors = validate_profile_update_data(data)
        if not is_valid:
            return jsonify({'error': 'Validation failed', 'details': errors}), 400

        user_id = session.get('user_id')

        # Update profile
        success, result = AuthService.update_user_profile(
            user_id=user_id,
            email=data.get('email'),
            username=data.get('username'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name')
        )

        if not success:
            status_code = 409 if 'already' in result else 500
            return jsonify({'error': result}), status_code

        # Update session with new data
        create_session(result)

        return jsonify({
            'message': 'Profile updated successfully',
            'user': {
                'user_id': result['UserID'],
                'email': result['Email'],
                'username': result['Username'],
                'first_name': result['FirstName'],
                'last_name': result['LastName'],
                'role': result['Role']
            }
        }), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@auth_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    """
    Change user password

    Request Body:
        {
            "current_password": "OldPass123",
            "new_password": "NewPass456",
            "confirm_password": "NewPass456"
        }

    Returns:
        200: Password changed successfully
        400: Validation error
        401: Not authenticated or incorrect current password
        500: Server error
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Request body is required'}), 400

        # Validate request data
        is_valid, errors = validate_password_change_data(data)
        if not is_valid:
            return jsonify({'error': 'Validation failed', 'details': errors}), 400

        user_id = session.get('user_id')

        # Change password
        success, message = AuthService.change_password(
            user_id=user_id,
            current_password=data['current_password'],
            new_password=data['new_password']
        )

        if not success:
            status_code = 401 if 'incorrect' in message.lower() else 500
            return jsonify({'error': message}), status_code

        return jsonify({'message': message}), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@auth_bp.route('/me', methods=['DELETE'])
@login_required
def delete_account():
    """
    Delete current user's account

    Returns:
        200: Account deleted successfully
        401: Not authenticated
        500: Server error
    """
    try:
        user_id = session.get('user_id')

        # Delete account
        success, message = AuthService.delete_user(user_id)

        if not success:
            return jsonify({'error': message}), 500

        # Clear session
        clear_session()

        return jsonify({'message': message}), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@auth_bp.route('/session', methods=['GET'])
def check_session():
    """
    Check if user has an active session

    Returns:
        200: Session info (authenticated or not)
    """
    try:
        user = get_current_user()

        if user:
            return jsonify({
                'authenticated': True,
                'user': user
            }), 200
        else:
            return jsonify({
                'authenticated': False
            }), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
