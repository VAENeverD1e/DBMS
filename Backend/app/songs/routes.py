"""
Song routes for managing songs and audio streaming
"""
from flask import Blueprint, request, jsonify, Response
from app.utils.decorators import guest_optional, artist_required
from .services import SongService
from .schemas import validate_song_create, validate_song_update


# Create Blueprint
songs_bp = Blueprint('songs', __name__, url_prefix='/api/songs')


@songs_bp.route('/', methods=['GET'])
@guest_optional
def get_songs(user_id=None):
    """
    Get all songs with optional filters (accessible to everyone)

    Query Parameters:
        genre (str): Filter by genre
        artist_id (int): Filter by artist ID
        search (str): Search in song title, artwork title, or artist name
        limit (int): Number of records to return (default: 50, max: 100)
        offset (int): Offset for pagination (default: 0)

    Returns:
        200: List of songs
        400: Validation error
        500: Server error
    """
    try:
        genre = request.args.get('genre')
        artist_id = request.args.get('artist_id', type=int)
        search = request.args.get('search')
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)

        # Validate pagination parameters
        if limit < 1 or limit > 100:
            return jsonify({'error': 'Limit must be between 1 and 100'}), 400

        if offset < 0:
            return jsonify({'error': 'Offset must be non-negative'}), 400

        success, result = SongService.get_all_songs(
            genre=genre,
            artist_id=artist_id,
            search=search,
            limit=limit,
            offset=offset
        )

        if not success:
            return jsonify({'error': result}), 500

        return jsonify({
            'songs': result,
            'pagination': {
                'limit': limit,
                'offset': offset,
                'count': len(result)
            },
            'filters': {
                'genre': genre,
                'artist_id': artist_id,
                'search': search
            }
        }), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@songs_bp.route('/<int:song_id>', methods=['GET'])
@guest_optional
def get_song(song_id, user_id=None):
    """
    Get song details by ID (accessible to everyone)

    Returns:
        200: Song details
        404: Song not found
        500: Server error
    """
    try:
        success, result = SongService.get_song_by_id(song_id)

        if not success:
            status_code = 404 if 'not found' in result.lower() else 500
            return jsonify({'error': result}), status_code

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@songs_bp.route('/<int:song_id>/stream', methods=['GET'])
@guest_optional
def stream_song(song_id, user_id=None):
    """
    Stream song audio

    Access Control:
    - Not logged in (guest): 30-second preview only
    - Logged in (any role): Full audio streaming

    Query Parameters:
        preview (bool): Force preview mode even if authenticated (default: false)

    Returns:
        200: Streaming information with audio URL and access details
        404: Song not found
        500: Server error
    """
    try:
        # Get song details
        success, song = SongService.get_song_by_id(song_id)

        if not success:
            status_code = 404 if 'not found' in result.lower() else 500
            return jsonify({'error': song}), status_code

        # Determine access level
        preview_mode = request.args.get('preview', 'false').lower() == 'true'

        # If user is not logged in, force preview mode
        if not user_id:
            preview_mode = True

        # Build response
        response = {
            'song_id': song['SongID'],
            'title': song['Title'],
            'duration': song['Duration'],
            'audio_url': song['AudioFileURL'],
            'preview_mode': preview_mode,
            'access_info': {
                'authenticated': user_id is not None,
                'full_access': user_id is not None and not preview_mode,
                'preview_duration': 30 if preview_mode else None,
                'message': '30-second preview only. Please log in for full access.' if preview_mode and not user_id else
                          '30-second preview mode' if preview_mode else
                          'Full audio access granted'
            },
            'artwork': {
                'artwork_id': song['ArtworkID'],
                'title': song['artwork_title'],
                'cover_image': song['CoverImage']
            },
            'artist': {
                'artist_id': song['ArtistID'],
                'username': song['artist_username'],
                'name': f"{song['artist_first_name']} {song['artist_last_name']}"
            }
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@songs_bp.route('/', methods=['POST'])
@artist_required
def create_song(user_id):
    """
    Create a new song (Artist only)

    Request Body:
        {
            "artwork_id": 123,
            "title": "Song Title",
            "track_number": 1,
            "duration": 240.5,
            "audio_file_url": "https://example.com/audio.mp3",
            "release_date": "2025-01-01"  // optional, YYYY-MM-DD
        }

    Returns:
        201: Song created successfully
        400: Validation error
        401: Not authenticated
        403: Not an artist or not artwork owner
        404: Artwork not found
        409: Track number already exists for this artwork
        500: Server error
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Request body is required'}), 400

        # Validate request data
        is_valid, errors = validate_song_create(data)
        if not is_valid:
            return jsonify({'error': 'Validation failed', 'details': errors}), 400

        # Create song
        success, result = SongService.create_song(
            user_id=user_id,
            artwork_id=data['artwork_id'],
            title=data['title'],
            track_number=data['track_number'],
            duration=data['duration'],
            audio_file_url=data['audio_file_url'],
            release_date=data.get('release_date')
        )

        if not success:
            if 'not found' in result.lower():
                status_code = 404
            elif 'not the owner' in result.lower() or 'not an artist' in result.lower():
                status_code = 403
            elif 'already exists' in result.lower():
                status_code = 409
            else:
                status_code = 500
            return jsonify({'error': result}), status_code

        return jsonify({
            'message': 'Song created successfully',
            'song': result
        }), 201

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@songs_bp.route('/<int:song_id>', methods=['PUT', 'PATCH'])
@artist_required
def update_song(song_id, user_id):
    """
    Update song (Artist only, owner only)

    Request Body (all fields optional, at least one required):
        {
            "title": "Updated Title",
            "track_number": 2,
            "duration": 250.0,
            "audio_file_url": "https://example.com/new-audio.mp3",
            "release_date": "2025-02-01"
        }

    Returns:
        200: Song updated successfully
        400: Validation error
        401: Not authenticated
        403: Not an artist or not owner
        404: Song not found
        409: Track number already exists for this artwork
        500: Server error
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Request body is required'}), 400

        # Validate request data
        is_valid, errors = validate_song_update(data)
        if not is_valid:
            return jsonify({'error': 'Validation failed', 'details': errors}), 400

        # Build updates dictionary
        updates = {}
        if 'title' in data:
            updates['title'] = data['title']
        if 'track_number' in data:
            updates['track_number'] = data['track_number']
        if 'duration' in data:
            updates['duration'] = data['duration']
        if 'audio_file_url' in data:
            updates['audio_file_url'] = data['audio_file_url']
        if 'release_date' in data:
            updates['release_date'] = data['release_date']

        # Update song
        success, result = SongService.update_song(
            user_id=user_id,
            song_id=song_id,
            **updates
        )

        if not success:
            if 'not found' in result.lower():
                status_code = 404
            elif 'not the owner' in result.lower() or 'not an artist' in result.lower():
                status_code = 403
            elif 'already exists' in result.lower():
                status_code = 409
            else:
                status_code = 500
            return jsonify({'error': result}), status_code

        return jsonify({
            'message': 'Song updated successfully',
            'song': result
        }), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@songs_bp.route('/<int:song_id>', methods=['DELETE'])
@artist_required
def delete_song(song_id, user_id):
    """
    Delete song (Artist only, owner only)

    Returns:
        200: Song deleted successfully
        401: Not authenticated
        403: Not an artist or not owner
        404: Song not found
        500: Server error
    """
    try:
        success, result = SongService.delete_song(user_id, song_id)

        if not success:
            if 'not found' in result.lower():
                status_code = 404
            elif 'not the owner' in result.lower() or 'not an artist' in result.lower():
                status_code = 403
            else:
                status_code = 500
            return jsonify({'error': result}), status_code

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
