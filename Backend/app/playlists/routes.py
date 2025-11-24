"""
Playlist routes for playlist operations
"""
from flask import Blueprint, request, jsonify
from app.utils.decorators import listener_required, guest_optional
from .services import PlaylistService
from .schemas import validate_playlist_create, validate_playlist_update, validate_add_song


# Create Blueprint
playlists_bp = Blueprint('playlists', __name__, url_prefix='/api/playlists')


@playlists_bp.route('/', methods=['GET'])
@guest_optional
def get_playlists(user_id=None):
    """
    Get all playlists (public view or user's own playlists)

    Query Parameters:
        limit (int): Number of records to return (default: 50)
        offset (int): Offset for pagination (default: 0)
        own (bool): Filter to show only own playlists (requires authentication)

    Returns:
        200: List of playlists
        400: Validation error
        500: Server error
    """
    try:
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        own = request.args.get('own', 'false').lower() == 'true'

        # Validate pagination parameters
        if limit < 1 or limit > 100:
            return jsonify({'error': 'Limit must be between 1 and 100'}), 400

        if offset < 0:
            return jsonify({'error': 'Offset must be non-negative'}), 400

        # If 'own' filter is requested but user is not authenticated
        if own and not user_id:
            return jsonify({'error': 'Authentication required to view own playlists'}), 401

        # Determine which user_id to filter by
        filter_user_id = user_id if own else None

        success, result = PlaylistService.get_all_playlists(filter_user_id, limit, offset)

        if not success:
            return jsonify({'error': result}), 500

        return jsonify({
            'playlists': result,
            'pagination': {
                'limit': limit,
                'offset': offset,
                'count': len(result)
            }
        }), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@playlists_bp.route('/<int:playlist_id>', methods=['GET'])
@guest_optional
def get_playlist(playlist_id, user_id=None):
    """
    Get playlist details with songs

    Returns:
        200: Playlist details
        404: Playlist not found
        500: Server error
    """
    try:
        success, result = PlaylistService.get_playlist_by_id(playlist_id, user_id)

        if not success:
            status_code = 404 if 'not found' in result.lower() else 500
            return jsonify({'error': result}), status_code

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@playlists_bp.route('/', methods=['POST'])
@listener_required
def create_playlist(user_id):
    """
    Create a new playlist (Listener only)

    Request Body:
        {
            "name": "My Playlist"
        }

    Returns:
        201: Playlist created successfully
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
        is_valid, errors = validate_playlist_create(data)
        if not is_valid:
            return jsonify({'error': 'Validation failed', 'details': errors}), 400

        # Create playlist
        success, result = PlaylistService.create_playlist(
            user_id=user_id,
            name=data['name']
        )

        if not success:
            return jsonify({'error': result}), 500

        return jsonify({
            'message': 'Playlist created successfully',
            'playlist': result
        }), 201

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@playlists_bp.route('/<int:playlist_id>', methods=['PUT', 'PATCH'])
@listener_required
def update_playlist(playlist_id, user_id):
    """
    Update playlist name (Listener only, owner only)

    Request Body:
        {
            "name": "Updated Playlist Name"
        }

    Returns:
        200: Playlist updated successfully
        400: Validation error
        401: Not authenticated
        403: Not a listener or not owner
        404: Playlist not found
        500: Server error
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Request body is required'}), 400

        # Validate request data
        is_valid, errors = validate_playlist_update(data)
        if not is_valid:
            return jsonify({'error': 'Validation failed', 'details': errors}), 400

        # Update playlist
        success, result = PlaylistService.update_playlist(
            user_id=user_id,
            playlist_id=playlist_id,
            name=data['name']
        )

        if not success:
            if 'not found' in result.lower():
                status_code = 404
            elif 'not the owner' in result.lower():
                status_code = 403
            else:
                status_code = 500
            return jsonify({'error': result}), status_code

        return jsonify({
            'message': 'Playlist updated successfully',
            'playlist': result
        }), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@playlists_bp.route('/<int:playlist_id>', methods=['DELETE'])
@listener_required
def delete_playlist(playlist_id, user_id):
    """
    Delete playlist (Listener only, owner only)

    Returns:
        200: Playlist deleted successfully
        401: Not authenticated
        403: Not a listener or not owner
        404: Playlist not found
        500: Server error
    """
    try:
        success, result = PlaylistService.delete_playlist(user_id, playlist_id)

        if not success:
            if 'not found' in result.lower():
                status_code = 404
            elif 'not the owner' in result.lower():
                status_code = 403
            else:
                status_code = 500
            return jsonify({'error': result}), status_code

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@playlists_bp.route('/<int:playlist_id>/songs', methods=['POST'])
@listener_required
def add_song_to_playlist(playlist_id, user_id):
    """
    Add song to playlist (Listener only, owner only)

    Request Body:
        {
            "song_id": 123,
            "order_index": 0  // optional
        }

    Returns:
        201: Song added successfully
        400: Validation error
        401: Not authenticated
        403: Not a listener or not owner
        404: Playlist or song not found
        409: Song already in playlist
        500: Server error
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Request body is required'}), 400

        # Validate request data
        is_valid, errors = validate_add_song(data)
        if not is_valid:
            return jsonify({'error': 'Validation failed', 'details': errors}), 400

        # Add song to playlist
        success, result = PlaylistService.add_song_to_playlist(
            user_id=user_id,
            playlist_id=playlist_id,
            song_id=data['song_id'],
            order_index=data.get('order_index')
        )

        if not success:
            if 'not found' in result.lower():
                status_code = 404
            elif 'not the owner' in result.lower():
                status_code = 403
            elif 'already in' in result.lower():
                status_code = 409
            else:
                status_code = 500
            return jsonify({'error': result}), status_code

        return jsonify(result), 201

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@playlists_bp.route('/<int:playlist_id>/songs/<int:song_id>', methods=['DELETE'])
@listener_required
def remove_song_from_playlist(playlist_id, song_id, user_id):
    """
    Remove song from playlist (Listener only, owner only)

    Returns:
        200: Song removed successfully
        401: Not authenticated
        403: Not a listener or not owner
        404: Playlist not found or song not in playlist
        500: Server error
    """
    try:
        success, result = PlaylistService.remove_song_from_playlist(
            user_id=user_id,
            playlist_id=playlist_id,
            song_id=song_id
        )

        if not success:
            if 'not found' in result.lower() or 'not in' in result.lower():
                status_code = 404
            elif 'not the owner' in result.lower():
                status_code = 403
            else:
                status_code = 500
            return jsonify({'error': result}), status_code

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
