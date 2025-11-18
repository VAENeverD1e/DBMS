"""
Authentication utilities for JWT token management
"""
import bcrypt
from functools import wraps
from flask import jsonify, current_app, request
import pymysql
import jwt
from datetime import datetime, timedelta


def create_jwt_token(user_data, expires_hours=24):
    """
    Create a JWT token for the given user data.

    Args:
        user_data (dict): User record (expects at least UserID, Username, Role)
        expires_hours (int): Expiration in hours

    Returns:
        str: JWT token
    """
    secret = current_app.config.get('SECRET_KEY', None)
    if not secret:
        # Fallback to a non-production secret if none set
        secret = current_app.config.setdefault('SECRET_KEY', 'dev-secret-change-me')

    payload = {
        'sub': int(user_data['UserID']),
        'username': user_data.get('Username'),
        'role': user_data.get('Role'),
        'exp': datetime.utcnow() + timedelta(hours=expires_hours)
    }

    token = jwt.encode(payload, secret, algorithm='HS256')
    # PyJWT 2.x returns a str
    return token


def decode_jwt_token(token):
    """
    Decode and verify a JWT token.

    Args:
        token (str): JWT token string

    Returns:
        dict: payload if valid

    Raises:
        jwt.PyJWTError: if token invalid/expired
    """
    secret = current_app.config.get('SECRET_KEY', None)
    if not secret:
        secret = current_app.config.setdefault('SECRET_KEY', 'dev-secret-change-me')

    payload = jwt.decode(token, secret, algorithms=['HS256'])
    return payload


def hash_password(password):
    """
    Hash a password using bcrypt

    Args:
        password (str): Plain text password

    Returns:
        str: Hashed password
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(plain_password, hashed_password):
    """
    Verify a password against its hash

    Args:
        plain_password (str): Plain text password to verify
        hashed_password (str): Stored hashed password

    Returns:
        bool: True if password matches, False otherwise
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def get_db_connection():
    """
    Get a database connection using the app config

    Returns:
        pymysql.Connection: Database connection
    """
    return pymysql.connect(**current_app.config['DB_CONFIG'])


def login_required(f):
    """
    Decorator to require JWT authentication for routes.
    Extracts and validates JWT token from Authorization header.

    Usage:
        @app.route('/protected')
        @login_required
        def protected_route():
            return jsonify({'message': 'Access granted'})
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import request
        
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({
                'error': 'Authentication required',
                'message': 'Missing or invalid Authorization header. Use: Authorization: Bearer <token>'
            }), 401
        
        token = auth_header[7:]  # Strip 'Bearer '
        try:
            payload = decode_jwt_token(token)
            # Store user_id in kwargs for the route to access
            kwargs['user_id'] = payload.get('sub')
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({
                'error': 'Token expired',
                'message': 'Your authentication token has expired. Please login again.'
            }), 401
        except jwt.InvalidTokenError as e:
            return jsonify({
                'error': 'Invalid token',
                'message': f'Invalid or tampered authentication token: {str(e)}'
            }), 401
        except Exception as e:
            return jsonify({
                'error': 'Authentication failed',
                'message': f'Error validating token: {str(e)}'
            }), 401
    
    return decorated_function


def role_required(*allowed_roles):
    """
    Decorator to require specific user roles for routes.
    Validates JWT token and checks role.

    Args:
        *allowed_roles: Variable number of role strings ('Listener', 'Artist', 'Guest')

    Usage:
        @app.route('/artist-only')
        @role_required('Artist')
        def artist_route(user_id):
            return jsonify({'message': 'Artist access'})
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask import request
            
            auth_header = request.headers.get('Authorization', '')
            if not auth_header.startswith('Bearer '):
                return jsonify({
                    'error': 'Authentication required',
                    'message': 'Missing or invalid Authorization header. Use: Authorization: Bearer <token>'
                }), 401
            
            token = auth_header[7:]  # Strip 'Bearer '
            try:
                payload = decode_jwt_token(token)
                user_id = payload.get('sub')
                user_role = payload.get('role')
                
                if user_role not in allowed_roles:
                    return jsonify({
                        'error': 'Forbidden',
                        'message': f'This resource requires one of the following roles: {", ".join(allowed_roles)}'
                    }), 403
                
                kwargs['user_id'] = user_id
                return f(*args, **kwargs)
            except jwt.ExpiredSignatureError:
                return jsonify({
                    'error': 'Token expired',
                    'message': 'Your authentication token has expired. Please login again.'
                }), 401
            except jwt.InvalidTokenError as e:
                return jsonify({
                    'error': 'Invalid token',
                    'message': f'Invalid or tampered authentication token: {str(e)}'
                }), 401
            except Exception as e:
                return jsonify({
                    'error': 'Authentication failed',
                    'message': f'Error validating token: {str(e)}'
                }), 401
        
        return decorated_function
    return decorator


def get_current_user_from_token(token_string):
    """
    Extract user information from a JWT token string.

    Args:
        token_string (str): JWT token

    Returns:
        dict: User info from token payload, or None if invalid

    Example usage in a route:
        @app.route('/me')
        def get_me():
            auth_header = request.headers.get('Authorization', '')
            if not auth_header.startswith('Bearer '):
                return jsonify({'error': 'No token'}), 401
            token = auth_header[7:]
            user_info = get_current_user_from_token(token)
            if not user_info:
                return jsonify({'error': 'Invalid token'}), 401
            return jsonify(user_info), 200
    """
    try:
        payload = decode_jwt_token(token_string)
        return {
            'user_id': payload.get('sub'),
            'username': payload.get('username'),
            'role': payload.get('role')
        }
    except Exception:
        return None


