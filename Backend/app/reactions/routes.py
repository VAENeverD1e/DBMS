"""
Reaction routes for managing listener reactions to songs and artworks
"""
from flask import Blueprint, request, jsonify
from app.utils.decorators import listener_required
from .services import ReactionService
from .schemas import validate_reaction_create


# Create Blueprint
reactions_bp = Blueprint('reactions', __name__, url_prefix='/api/reactions')


@reactions_bp.route('/', methods=['POST'])
@listener_required
def create_reaction(user_id):
    """
    Create a reaction to a song or artwork (listener only)

    Request Body:
        {
            "reactable_type": "Song",  // or "Artwork"
            "reactable_id": 123,
            "emotion": "Like"  // optional: "Like", "Love", "Dislike" (default: "Like")
        }

    Returns:
        201: Reaction created successfully
        200: Reaction updated successfully (if already exists)
        400: Validation error
        401: Not authenticated
        403: Not a listener
        404: Song/Artwork not found
        500: Server error
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Request body is required'}), 400

        # Validate request data
        is_valid, errors = validate_reaction_create(data)
        if not is_valid:
            return jsonify({'error': 'Validation failed', 'details': errors}), 400

        # Create or update reaction
        reactable_type = data['reactable_type']
        reactable_id = data['reactable_id']
        emotion = data.get('emotion', 'Like')

        success, result = ReactionService.create_reaction(
            user_id=user_id,
            reactable_type=reactable_type,
            reactable_id=reactable_id,
            emotion=emotion
        )

        if not success:
            if 'not found' in result.lower():
                status_code = 404
            else:
                status_code = 500
            return jsonify({'error': result}), status_code

        # Return 201 for new reaction, 200 for update
        status_code = 201 if 'created' in result['message'] else 200
        return jsonify(result), status_code

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@reactions_bp.route('/<int:reaction_id>', methods=['DELETE'])
@listener_required
def delete_reaction(reaction_id, user_id):
    """
    Delete a reaction (listener only)

    Returns:
        200: Reaction deleted successfully
        401: Not authenticated
        403: Not a listener
        404: Reaction not found or does not belong to user
        500: Server error
    """
    try:
        success, result = ReactionService.delete_reaction(user_id, reaction_id)

        if not success:
            status_code = 404 if 'not found' in result.lower() else 500
            return jsonify({'error': result}), status_code

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@reactions_bp.route('/song/<int:song_id>', methods=['GET'])
def get_song_reactions(song_id):
    """
    Get all reactions for a specific song

    Returns:
        200: List of reactions with summary
        404: Song not found
        500: Server error
    """
    try:
        success, result = ReactionService.get_reactions_for_song(song_id)

        if not success:
            status_code = 404 if 'not found' in result.lower() else 500
            return jsonify({'error': result}), status_code

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@reactions_bp.route('/artwork/<int:artwork_id>', methods=['GET'])
def get_artwork_reactions(artwork_id):
    """
    Get all reactions for a specific artwork (album)

    Returns:
        200: List of reactions with summary
        404: Artwork not found
        500: Server error
    """
    try:
        success, result = ReactionService.get_reactions_for_artwork(artwork_id)

        if not success:
            status_code = 404 if 'not found' in result.lower() else 500
            return jsonify({'error': result}), status_code

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
