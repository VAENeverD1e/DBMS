"""
Artwork routes for artwork operations
"""
from flask import Blueprint, request, jsonify
from app.utils.decorators import artist_required, guest_optional
from .services import ArtworkService
from .schemas import validate_artwork_create, validate_artwork_update


# Create Blueprint
artworks_bp = Blueprint('artworks', __name__, url_prefix='/api/artworks')


@artworks_bp.route('/', methods=['GET'])
@guest_optional
def get_artworks(user_id=None):
    """
    Get all artworks with optional filters

    Query Parameters:
        artist_id (int): Filter by artist ID
        genre (str): Filter by genre
        type (str): Filter by type ('Album' or 'Single')
        search (str): Search by title
        limit (int): Number of records to return (default: 50)
        offset (int): Offset for pagination (default: 0)

    Returns:
        200: List of artworks
        400: Validation error
        500: Server error
    """
    try:
        artist_id = request.args.get('artist_id', type=int)
        genre = request.args.get('genre', type=str)
        artwork_type = request.args.get('type', type=str)
        search = request.args.get('search', type=str)
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)

        # Validate pagination parameters
        if limit < 1 or limit > 100:
            return jsonify({'error': 'Limit must be between 1 and 100'}), 400

        if offset < 0:
            return jsonify({'error': 'Offset must be non-negative'}), 400

        # Validate type if provided
        if artwork_type and artwork_type not in ['Album', 'Single']:
            return jsonify({'error': 'Type must be either "Album" or "Single"'}), 400

        success, result = ArtworkService.get_all_artworks(
            artist_id=artist_id,
            genre=genre,
            artwork_type=artwork_type,
            search=search,
            limit=limit,
            offset=offset
        )

        if not success:
            return jsonify({'error': result}), 500

        return jsonify({
            'artworks': result,
            'pagination': {
                'limit': limit,
                'offset': offset,
                'count': len(result)
            }
        }), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@artworks_bp.route('/<int:artwork_id>', methods=['GET'])
@guest_optional
def get_artwork(artwork_id, user_id=None):
    """
    Get artwork details with songs

    Returns:
        200: Artwork details
        404: Artwork not found
        500: Server error
    """
    try:
        success, result = ArtworkService.get_artwork_by_id(artwork_id)

        if not success:
            status_code = 404 if 'not found' in result.lower() else 500
            return jsonify({'error': result}), status_code

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@artworks_bp.route('/<int:artwork_id>/songs', methods=['GET'])
@guest_optional
def get_artwork_songs(artwork_id, user_id=None):
    """
    Get all songs in an artwork

    Returns:
        200: List of songs
        404: Artwork not found
        500: Server error
    """
    try:
        success, result = ArtworkService.get_artwork_songs(artwork_id)

        if not success:
            status_code = 404 if 'not found' in result.lower() else 500
            return jsonify({'error': result}), status_code

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@artworks_bp.route('/', methods=['POST'])
@artist_required
def create_artwork(user_id):
    """
    Create a new artwork (album or single) - Artist only

    Request Body:
        {
            "title": "Album Title",
            "type": "Album",  // or "Single"
            "genre": "Pop",  // optional
            "release_date": "2024-01-01",  // optional (YYYY-MM-DD)
            "cover_image": "https://example.com/cover.jpg"  // optional
        }

    Returns:
        201: Artwork created successfully
        400: Validation error
        401: Not authenticated
        403: Not an artist
        500: Server error
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Request body is required'}), 400

        # Validate request data
        is_valid, errors = validate_artwork_create(data)
        if not is_valid:
            return jsonify({'error': 'Validation failed', 'details': errors}), 400

        # Create artwork
        success, result = ArtworkService.create_artwork(
            user_id=user_id,
            title=data['title'],
            artwork_type=data['type'],
            genre=data.get('genre'),
            release_date=data.get('release_date'),
            cover_image=data.get('cover_image')
        )

        if not success:
            return jsonify({'error': result}), 500

        return jsonify({
            'message': 'Artwork created successfully',
            'artwork': result
        }), 201

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@artworks_bp.route('/<int:artwork_id>', methods=['PUT', 'PATCH'])
@artist_required
def update_artwork(artwork_id, user_id):
    """
    Update artwork - Artist only, owner only

    Request Body:
        {
            "title": "Updated Title",  // optional
            "genre": "Rock",  // optional
            "cover_image": "https://example.com/new-cover.jpg",  // optional
            "release_date": "2024-02-01"  // optional
        }

    Returns:
        200: Artwork updated successfully
        400: Validation error
        401: Not authenticated
        403: Not an artist or not owner
        404: Artwork not found
        500: Server error
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Request body is required'}), 400

        # Validate request data
        is_valid, errors = validate_artwork_update(data)
        if not is_valid:
            return jsonify({'error': 'Validation failed', 'details': errors}), 400

        # Update artwork
        success, result = ArtworkService.update_artwork(
            user_id=user_id,
            artwork_id=artwork_id,
            title=data.get('title'),
            genre=data.get('genre'),
            cover_image=data.get('cover_image'),
            release_date=data.get('release_date')
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
            'message': 'Artwork updated successfully',
            'artwork': result
        }), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@artworks_bp.route('/<int:artwork_id>', methods=['DELETE'])
@artist_required
def delete_artwork(artwork_id, user_id):
    """
    Delete artwork - Artist only, owner only

    Returns:
        200: Artwork deleted successfully
        401: Not authenticated
        403: Not an artist or not owner
        404: Artwork not found
        500: Server error
    """
    try:
        success, result = ArtworkService.delete_artwork(user_id, artwork_id)

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
