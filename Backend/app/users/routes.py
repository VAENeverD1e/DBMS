"""
User routes for user-specific operations
"""
from flask import Blueprint, request, jsonify
from app.utils.decorators import login_required, listener_required
from .services import UserService
from .schemas import validate_preferences_update


# Create Blueprint
users_bp = Blueprint('users', __name__, url_prefix='/api/users')


@users_bp.route('/me/stats', methods=['GET'])
@login_required
def get_user_stats(user_id):
    """
    Get current user's statistics (playlists count, followers, following, etc.)

    Returns:
        200: User statistics
        401: Not authenticated
        500: Server error
    """
    try:
        stats = UserService.get_user_stats(user_id)

        if stats is None:
            return jsonify({'error': 'Failed to fetch user statistics'}), 500

        return jsonify({'stats': stats}), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@users_bp.route('/me/preferences', methods=['PUT', 'PATCH'])
@listener_required
def update_preferences(user_id):
    """
    Update listener preferences

    Request Body:
        {
            "preference": "string",  // optional
            "favorite_genre": "Rock"  // optional
        }

    Returns:
        200: Preferences updated successfully
        400: Validation error
        401: Not authenticated
        403: Not a listener
        500: Server error
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Request body is required'}), 400

        # Validate request data
        is_valid, errors = validate_preferences_update(data)
        if not is_valid:
            return jsonify({'error': 'Validation failed', 'details': errors}), 400

        # Update preferences
        success, result = UserService.update_listener_preferences(
            user_id=user_id,
            preference=data.get('preference'),
            favorite_genre=data.get('favorite_genre')
        )

        if not success:
            return jsonify({'error': result}), 500

        return jsonify({
            'message': 'Preferences updated successfully',
            'preferences': result
        }), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@users_bp.route('/me/history', methods=['GET'])
@listener_required
def get_play_history(user_id):
    """
    Get current user's play history

    Query Parameters:
        limit (int): Number of records to return (default: 50)
        offset (int): Offset for pagination (default: 0)

    Returns:
        200: Play history
        401: Not authenticated
        403: Not a listener
        500: Server error
    """
    try:
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)

        # Validate pagination parameters
        if limit < 1 or limit > 100:
            return jsonify({'error': 'Limit must be between 1 and 100'}), 400

        if offset < 0:
            return jsonify({'error': 'Offset must be non-negative'}), 400

        success, result = UserService.get_play_history(user_id, limit, offset)

        if not success:
            return jsonify({'error': result}), 500

        return jsonify({
            'history': result,
            'pagination': {
                'limit': limit,
                'offset': offset,
                'count': len(result)
            }
        }), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@users_bp.route('/me/history', methods=['POST'])
@listener_required
def record_play(user_id):
    """
    Record a song play in user's history

    Request Body:
        {
            "song_id": 123,
            "listen_duration": 180  // in seconds
        }

    Returns:
        201: Play recorded successfully
        400: Validation error
        401: Not authenticated
        403: Not a listener
        500: Server error
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Request body is required'}), 400

        # Validate required fields
        if 'song_id' not in data:
            return jsonify({'error': 'song_id is required'}), 400

        if 'listen_duration' not in data:
            return jsonify({'error': 'listen_duration is required'}), 400

        success, result = UserService.record_play_history(
            user_id=user_id,
            song_id=data['song_id'],
            listen_duration=data['listen_duration']
        )

        if not success:
            return jsonify({'error': result}), 500

        return jsonify(result), 201

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@users_bp.route('/me/following', methods=['GET'])
@listener_required
def get_following(user_id):
    """
    Get list of artists the user is following

    Query Parameters:
        limit (int): Number of records to return (default: 50)
        offset (int): Offset for pagination (default: 0)

    Returns:
        200: List of followed artists
        401: Not authenticated
        403: Not a listener
        500: Server error
    """
    try:
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)

        # Validate pagination parameters
        if limit < 1 or limit > 100:
            return jsonify({'error': 'Limit must be between 1 and 100'}), 400

        if offset < 0:
            return jsonify({'error': 'Offset must be non-negative'}), 400

        success, result = UserService.get_following_artists(user_id, limit, offset)

        if not success:
            return jsonify({'error': result}), 500

        return jsonify({
            'artists': result,
            'pagination': {
                'limit': limit,
                'offset': offset,
                'count': len(result)
            }
        }), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@users_bp.route('/me/following/<int:artist_id>', methods=['POST'])
@listener_required
def follow_artist(artist_id, user_id):
    """
    Follow an artist

    Returns:
        200: Successfully followed
        400: Validation error
        401: Not authenticated
        403: Not a listener
        404: Artist not found
        409: Already following
        500: Server error
    """
    try:

        success, result = UserService.follow_artist(user_id, artist_id)

        if not success:
            if 'not found' in result.lower():
                status_code = 404
            elif 'already' in result.lower():
                status_code = 409
            else:
                status_code = 500
            return jsonify({'error': result}), status_code

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@users_bp.route('/me/following/<int:artist_id>', methods=['DELETE'])
@listener_required
def unfollow_artist(artist_id, user_id):
    """
    Unfollow an artist

    Returns:
        200: Successfully unfollowed
        401: Not authenticated
        403: Not a listener
        404: Not following this artist
        500: Server error
    """
    try:

        success, result = UserService.unfollow_artist(user_id, artist_id)

        if not success:
            status_code = 404 if 'not following' in result.lower() else 500
            return jsonify({'error': result}), status_code

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@users_bp.route('/me/reactions', methods=['GET'])
@listener_required
def get_user_reactions(user_id):
    """
    Get user's reactions (liked songs/albums)

    Query Parameters:
        type (str): Filter by type ('Song' or 'Artwork'), optional
        limit (int): Number of records to return (default: 50)
        offset (int): Offset for pagination (default: 0)

    Returns:
        200: List of reactions
        401: Not authenticated
        403: Not a listener
        500: Server error
    """
    try:
        reactable_type = request.args.get('type')
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)

        # Validate pagination parameters
        if limit < 1 or limit > 100:
            return jsonify({'error': 'Limit must be between 1 and 100'}), 400

        if offset < 0:
            return jsonify({'error': 'Offset must be non-negative'}), 400

        # Validate reactable_type if provided
        if reactable_type and reactable_type not in ['Song', 'Artwork']:
            return jsonify({'error': 'Type must be either "Song" or "Artwork"'}), 400

        success, result = UserService.get_user_reactions(user_id, reactable_type, limit, offset)

        if not success:
            return jsonify({'error': result}), 500

        return jsonify({
            'reactions': result,
            'pagination': {
                'limit': limit,
                'offset': offset,
                'count': len(result)
            }
        }), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@users_bp.route('/upgrade-role', methods=['POST'])
@login_required
def upgrade_role(user_id):
    """
    Upgrade user role (called after successful subscription payment)
    This endpoint is typically called by the payment webhook handler

    Request Body:
        {
            "new_role": "Listener"  // or "Artist"
        }

    Returns:
        200: Role upgraded successfully
        400: Validation error
        401: Not authenticated
        409: Invalid role transition
        500: Server error
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Request body is required'}), 400

        if 'new_role' not in data:
            return jsonify({'error': 'new_role is required'}), 400

        new_role = data['new_role']

        if new_role not in ['Listener', 'Artist']:
            return jsonify({'error': 'new_role must be either "Listener" or "Artist"'}), 400

        success, result = UserService.upgrade_user_role(user_id, new_role)

        if not success:
            status_code = 409 if 'already' in result.lower() or 'invalid' in result.lower() else 500
            return jsonify({'error': result}), status_code

        return jsonify({
            'message': 'Role upgraded successfully',
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
