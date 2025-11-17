"""
Authentication utilities for password hashing and session management
"""
import hashlib
import secrets
from functools import wraps
from flask import session, jsonify, current_app
import pymysql


def hash_password(password):
    """
    Hash a password using SHA-256

    Args:
        password (str): Plain text password

    Returns:
        str: Hashed password
    """
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password, hashed_password):
    """
    Verify a password against its hash

    Args:
        plain_password (str): Plain text password to verify
        hashed_password (str): Stored hashed password

    Returns:
        bool: True if password matches, False otherwise
    """
    return hash_password(plain_password) == hashed_password


def generate_session_token():
    """
    Generate a secure random session token

    Returns:
        str: Random session token
    """
    return secrets.token_urlsafe(32)


def get_db_connection():
    """
    Get a database connection using the app config

    Returns:
        pymysql.Connection: Database connection
    """
    return pymysql.connect(**current_app.config['DB_CONFIG'])


def login_required(f):
    """
    Decorator to require authentication for routes

    Usage:
        @app.route('/protected')
        @login_required
        def protected_route():
            return jsonify({'message': 'Access granted'})
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({
                'error': 'Authentication required',
                'message': 'Please login to access this resource'
            }), 401
        return f(*args, **kwargs)
    return decorated_function


def role_required(*allowed_roles):
    """
    Decorator to require specific user roles for routes

    Args:
        *allowed_roles: Variable number of role strings ('Listener', 'Artist')

    Usage:
        @app.route('/artist-only')
        @role_required('Artist')
        def artist_route():
            return jsonify({'message': 'Artist access'})
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return jsonify({
                    'error': 'Authentication required',
                    'message': 'Please login to access this resource'
                }), 401

            if 'role' not in session:
                return jsonify({
                    'error': 'Invalid session',
                    'message': 'Session is missing role information'
                }), 401

            if session['role'] not in allowed_roles:
                return jsonify({
                    'error': 'Forbidden',
                    'message': f'This resource requires one of the following roles: {", ".join(allowed_roles)}'
                }), 403

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def get_current_user():
    """
    Get the current logged-in user's information from session

    Returns:
        dict: User information from session or None
    """
    if 'user_id' not in session:
        return None

    return {
        'user_id': session.get('user_id'),
        'email': session.get('email'),
        'username': session.get('username'),
        'role': session.get('role'),
        'first_name': session.get('first_name'),
        'last_name': session.get('last_name')
    }


def create_session(user_data):
    """
    Create a session for a logged-in user

    Args:
        user_data (dict): Dictionary containing user information
    """
    session['user_id'] = user_data['UserID']
    session['email'] = user_data['Email']
    session['username'] = user_data['Username']
    session['role'] = user_data['Role']
    session['first_name'] = user_data.get('FirstName')
    session['last_name'] = user_data.get('LastName')
    session.permanent = True  # Make session persistent


def clear_session():
    """
    Clear the current user session
    """
    session.clear()
