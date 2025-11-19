"""
Role-based access control decorators (JWT-based)
"""
from functools import wraps
from flask import jsonify, request
import jwt
from flask import current_app


def _decode_jwt(token):
    """Helper to decode JWT token"""
    secret = current_app.config.get('SECRET_KEY', 'dev-secret-change-me')
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def _get_user_from_token():
    """Extract user info from Authorization header JWT token"""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header[7:]  # Strip 'Bearer '
    payload = _decode_jwt(token)
    if payload:
        return {
            'user_id': payload.get('sub'),
            'role': payload.get('role'),
            'username': payload.get('username')
        }
    return None


def guest_optional(f):
    """
    Decorator for routes accessible to both authenticated and unauthenticated users.
    Optionally injects user_id if authenticated via JWT.

    Usage:
        @app.route('/music/stream/<id>')
        @guest_optional
        def stream_music(id, user_id=None):
            # user_id is None if not authenticated, or the integer user_id if authenticated
            return jsonify({'message': 'Streaming...'})
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = _get_user_from_token()
        if user:
            kwargs['user_id'] = user['user_id']
        return f(*args, **kwargs)
    return decorated_function


def login_required(f):
    """
    Decorator to require authentication (any logged-in user including Guest role).
    Validates JWT token from Authorization header and injects user_id.

    Usage:
        @app.route('/subscribe')
        @login_required
        def subscribe(user_id):
            return jsonify({'message': 'Subscription page'})
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = _get_user_from_token()
        if not user:
            return jsonify({
                'error': 'Authentication required',
                'message': 'Missing or invalid Authorization header. Use: Authorization: Bearer <token>'
            }), 401
        kwargs['user_id'] = user['user_id']
        return f(*args, **kwargs)
    return decorated_function


def listener_required(f):
    """
    Decorator to require Listener role.
    Validates JWT token and checks for Listener role.
    Listener can: create playlists, react to artworks, follow artists, view play history

    Usage:
        @app.route('/playlists/create')
        @listener_required
        def create_playlist(user_id):
            return jsonify({'message': 'Create playlist'})
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = _get_user_from_token()
        if not user:
            return jsonify({
                'error': 'Authentication required',
                'message': 'Missing or invalid Authorization header. Use: Authorization: Bearer <token>'
            }), 401

        if user['role'] != 'Listener':
            return jsonify({
                'error': 'Forbidden',
                'message': 'This feature is only available to Listener subscribers. Please subscribe to a Listener plan.'
            }), 403

        kwargs['user_id'] = user['user_id']
        return f(*args, **kwargs)
    return decorated_function


def artist_required(f):
    """
    Decorator to require Artist role.
    Validates JWT token and checks for Artist role.
    Artist can: release artworks (songs/albums)
    Artist cannot: create playlists, react, follow (listener features)

    Usage:
        @app.route('/artworks/create')
        @artist_required
        def create_artwork(user_id):
            return jsonify({'message': 'Create artwork'})
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = _get_user_from_token()
        if not user:
            return jsonify({
                'error': 'Authentication required',
                'message': 'Missing or invalid Authorization header. Use: Authorization: Bearer <token>'
            }), 401

        if user['role'] != 'Artist':
            return jsonify({
                'error': 'Forbidden',
                'message': 'This feature is only available to Artists. Please register as an Artist.'
            }), 403

        kwargs['user_id'] = user['user_id']
        return f(*args, **kwargs)
    return decorated_function


def role_required(*allowed_roles):
    """
    Decorator to require one of multiple specific roles.
    Validates JWT token and checks role.

    Args:
        *allowed_roles: Variable number of role strings ('Guest', 'Listener', 'Artist')

    Usage:
        @app.route('/profile')
        @role_required('Listener', 'Artist')
        def profile(user_id):
            return jsonify({'message': 'Profile page'})
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = _get_user_from_token()
            if not user:
                return jsonify({
                    'error': 'Authentication required',
                    'message': 'Missing or invalid Authorization header. Use: Authorization: Bearer <token>'
                }), 401

            if user['role'] not in allowed_roles:
                return jsonify({
                    'error': 'Forbidden',
                    'message': f'This resource requires one of the following roles: {", ".join(allowed_roles)}'
                }), 403

            kwargs['user_id'] = user['user_id']
            return f(*args, **kwargs)
        return decorated_function
    return decorator
