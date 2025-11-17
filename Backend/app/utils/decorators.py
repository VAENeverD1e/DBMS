"""
Role-based access control decorators
"""
from functools import wraps
from flask import session, jsonify


def guest_optional(f):
    """
    Decorator for routes accessible to both authenticated and unauthenticated users.
    Sets a flag to indicate if user is authenticated.

    Usage:
        @app.route('/music/stream/<id>')
        @guest_optional
        def stream_music(id):
            # Access session.get('user_id') to check if authenticated
            return jsonify({'message': 'Streaming...'})
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Just pass through - the route can check session['user_id'] itself
        return f(*args, **kwargs)
    return decorated_function


def login_required(f):
    """
    Decorator to require authentication (any logged-in user including Guest role)

    Usage:
        @app.route('/subscribe')
        @login_required
        def subscribe():
            return jsonify({'message': 'Subscription page'})
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


def listener_required(f):
    """
    Decorator to require Listener role
    Listener can: create playlists, react to artworks, follow artists, view play history

    Usage:
        @app.route('/playlists/create')
        @listener_required
        def create_playlist():
            return jsonify({'message': 'Create playlist'})
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({
                'error': 'Authentication required',
                'message': 'Please login to access this resource'
            }), 401

        if 'role' not in session or session['role'] != 'Listener':
            return jsonify({
                'error': 'Forbidden',
                'message': 'This feature is only available to Listener subscribers. Please subscribe to a Listener plan.'
            }), 403

        return f(*args, **kwargs)
    return decorated_function


def artist_required(f):
    """
    Decorator to require Artist role
    Artist can: release artworks (songs/albums)
    Artist cannot: create playlists, react, follow (listener features)

    Usage:
        @app.route('/artworks/create')
        @artist_required
        def create_artwork():
            return jsonify({'message': 'Create artwork'})
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({
                'error': 'Authentication required',
                'message': 'Please login to access this resource'
            }), 401

        if 'role' not in session or session['role'] != 'Artist':
            return jsonify({
                'error': 'Forbidden',
                'message': 'This feature is only available to Artists. Please register as an Artist.'
            }), 403

        return f(*args, **kwargs)
    return decorated_function


def role_required(*allowed_roles):
    """
    Decorator to require one of multiple specific roles

    Args:
        *allowed_roles: Variable number of role strings ('Guest', 'Listener', 'Artist')

    Usage:
        @app.route('/profile')
        @role_required('Listener', 'Artist')
        def profile():
            return jsonify({'message': 'Profile page'})
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
