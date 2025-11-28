"""
Artist routes for artist operations
"""

from flask import Blueprint, request, jsonify
from app.utils.decorators import guest_optional, artist_required, listener_required, login_required
from .services import ArtistService
from .schemas import validate_artist_profile_update, validate_social_links_update


# Create Blueprint
artists_bp = Blueprint("artists", __name__, url_prefix="/api/artists")


@artists_bp.route("/", methods=["GET"])
@guest_optional
def get_artists(user_id=None):
    """
    Get all artists with optional filters

    Query Parameters:
        genre (str): Filter by genre
        verified (str): Filter by verified status ('Verified', 'Pending', 'Unverified')
        search (str): Search by artist username or name
        limit (int): Number of records to return (default: 50)
        offset (int): Offset for pagination (default: 0)

    Returns:
        200: List of artists
        400: Validation error
        500: Server error
    """
    try:
        genre = request.args.get("genre")
        verified = request.args.get("verified")
        search = request.args.get("search")
        limit = request.args.get("limit", 50, type=int)
        offset = request.args.get("offset", 0, type=int)

        # Validate pagination parameters
        if limit < 1 or limit > 100:
            return jsonify({"error": "Limit must be between 1 and 100"}), 400

        if offset < 0:
            return jsonify({"error": "Offset must be non-negative"}), 400

        # Validate verified status if provided
        if verified and verified not in ["Verified", "Pending", "Unverified"]:
            return jsonify(
                {
                    "error": "Verified status must be one of: Verified, Pending, Unverified"
                }
            ), 400

        success, result = ArtistService.get_all_artists(
            genre, verified, search, limit, offset
        )

        if not success:
            return jsonify({"error": result}), 500

        return jsonify(
            {
                "artists": result,
                "pagination": {"limit": limit, "offset": offset, "count": len(result)},
            }
        ), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@artists_bp.route("/<int:artist_id>", methods=["GET"])
@guest_optional
def get_artist(artist_id, user_id=None):
    """
    Get artist details by artist ID

    Returns:
        200: Artist details
        404: Artist not found
        500: Server error
    """
    try:
        success, result = ArtistService.get_artist_by_id(artist_id)

        if not success:
            status_code = 404 if "not found" in result.lower() else 500
            return jsonify({"error": result}), status_code

        return jsonify({"artist": result}), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@artists_bp.route("/<int:artist_id>/artworks", methods=["GET"])
@guest_optional
def get_artist_artworks(artist_id, user_id=None):
    """
    Get artworks created by an artist

    Query Parameters:
        limit (int): Number of records to return (default: 50)
        offset (int): Offset for pagination (default: 0)

    Returns:
        200: List of artworks
        400: Validation error
        404: Artist not found
        500: Server error
    """
    try:
        limit = request.args.get("limit", 50, type=int)
        offset = request.args.get("offset", 0, type=int)

        # Validate pagination parameters
        if limit < 1 or limit > 100:
            return jsonify({"error": "Limit must be between 1 and 100"}), 400

        if offset < 0:
            return jsonify({"error": "Offset must be non-negative"}), 400

        success, result = ArtistService.get_artist_artworks(artist_id, limit, offset)

        if not success:
            status_code = 404 if "not found" in result.lower() else 500
            return jsonify({"error": result}), status_code

        return jsonify(
            {
                "artworks": result,
                "pagination": {"limit": limit, "offset": offset, "count": len(result)},
            }
        ), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@artists_bp.route("/<int:artist_id>/stats", methods=["GET"])
@guest_optional
def get_artist_stats(artist_id, user_id=None):
    """
    Get artist statistics (followers, artworks count, total likes)

    Returns:
        200: Artist statistics
        404: Artist not found
        500: Server error
    """
    try:
        success, result = ArtistService.get_artist_stats(artist_id)

        if not success:
            status_code = 404 if "not found" in result.lower() else 500
            return jsonify({"error": result}), status_code

        return jsonify({"stats": result}), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@artists_bp.route("/me", methods=["GET"])
@artist_required
def get_current_artist(user_id):
    """
    Get current authenticated artist's profile and stats

    Returns:
        200: Artist profile with stats
        404: User is not an artist
        500: Server error
    """
    try:
        # Get artist ID from user ID
        artist_id = ArtistService.get_artist_id(user_id)
        if not artist_id:
            return jsonify({"error": "User is not an artist"}), 404

        # Get artist details
        success, artist = ArtistService.get_artist_by_id(artist_id)
        if not success:
            return jsonify({"error": artist}), 500

        # Get artist stats
        success, stats = ArtistService.get_artist_stats(artist_id)
        if not success:
            return jsonify({"error": stats}), 500

        # Get recent artworks (limit 10)
        success, artworks = ArtistService.get_artist_artworks(artist_id, limit=10, offset=0)
        if not success:
            artworks = []

        return jsonify({
            "artist": artist,
            "stats": stats,
            "recent_artworks": artworks
        }), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@artists_bp.route("/me", methods=["PUT", "PATCH"])
@artist_required
def update_artist_profile(user_id):
    """
    Update own artist profile (Artist only)

    Request Body:
        {
            "genre": "Rock"  // optional
        }

    Returns:
        200: Profile updated successfully
        400: Validation error
        401: Not authenticated
        403: Not an artist
        500: Server error
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Request body is required"}), 400

        # Validate request data
        is_valid, errors = validate_artist_profile_update(data)
        if not is_valid:
            return jsonify({"error": "Validation failed", "details": errors}), 400

        # Update profile
        success, result = ArtistService.update_artist_profile(
            user_id=user_id, genre=data.get("genre")
        )

        if not success:
            return jsonify({"error": result}), 500

        return jsonify(
            {"message": "Artist profile updated successfully", "artist": result}
        ), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@artists_bp.route("/me/social-links", methods=["PUT", "PATCH"])
@artist_required
def update_social_links(user_id):
    """
    Update social media links (Artist only)

    Request Body:
        {
            "social_links": "https://twitter.com/artist, https://instagram.com/artist"
        }

    Returns:
        200: Social links updated successfully
        400: Validation error
        401: Not authenticated
        403: Not an artist
        500: Server error
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Request body is required"}), 400

        # Validate request data
        is_valid, errors = validate_social_links_update(data)
        if not is_valid:
            return jsonify({"error": "Validation failed", "details": errors}), 400

        # Update social links
        success, result = ArtistService.update_social_links(
            user_id=user_id, social_links=data["social_links"]
        )

        if not success:
            return jsonify({"error": result}), 500

        return jsonify(
            {"message": "Social links updated successfully", "artist": result}
        ), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

# In routes.py
@artists_bp.route("/<int:artist_id>/followers", methods=["GET"])
@guest_optional
def get_followers(artist_id, user_id=None):
    """
    Get followers of an artist

    Query Parameters:
        limit (int): Records per page (1-100, default 50)
        offset (int): Pagination offset (default 0)
    """
    try:
        limit = request.args.get("limit", 50, type=int)
        offset = request.args.get("offset", 0, type=int)

        if limit < 1 or limit > 100:
            return jsonify({"error": "Limit must be between 1 and 100"}), 400
        if offset < 0:
            return jsonify({"error": "Offset must be non-negative"}), 400

        success, result = ArtistService.get_followers(artist_id, limit, offset)

        if not success:
            status_code = 404 if "not found" in result.lower() else 500
            return jsonify({"error": result}), status_code

        return jsonify(
            {
                "followers": result["followers"],
                "total": result["total"],
                "pagination": {
                    "limit": limit,
                    "offset": offset,
                    "count": len(result["followers"]),
                },
            }
        ), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

# In routes.py
@artists_bp.route("/me/verify", methods=["POST"])
@artist_required
def self_verify(user_id):
    """
    Self-verify artist if prerequisites met

    Prerequisites (from project PDF):
    - Followers >= 670
    - Artworks >= 3

    Returns:
        200: Verified successfully or already verified
        400: Prerequisites not met (with reasons)
        403: Not an artist
    """
    try:
        success, result = ArtistService.self_verify(user_id)

        if not success:
            # If result is a dict, it has detailed reasons
            if isinstance(result, dict):
                return jsonify(result), 400
            else:
                return jsonify({"error": result}), 400

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@artists_bp.route("/<int:artist_id>/follow", methods=["POST"])
@listener_required
def follow_artist(artist_id, user_id):
    """
    Follow an artist (Listener only)

    Returns:
        200: Successfully followed
        400: Already following
        404: Artist not found
        500: Server error
    """
    try:
        success, result = ArtistService.follow_artist(user_id, artist_id)

        if not success:
            if "not found" in result.lower():
                return jsonify({"error": result}), 404
            elif "already" in result.lower():
                return jsonify({"error": result}), 400
            return jsonify({"error": result}), 500

        return jsonify({"message": "Successfully followed artist", "data": result}), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@artists_bp.route("/<int:artist_id>/follow", methods=["DELETE"])
@listener_required
def unfollow_artist(artist_id, user_id):
    """
    Unfollow an artist (Listener only)

    Returns:
        200: Successfully unfollowed
        400: Not following
        404: Artist not found
        500: Server error
    """
    try:
        success, result = ArtistService.unfollow_artist(user_id, artist_id)

        if not success:
            if "not found" in result.lower():
                return jsonify({"error": result}), 404
            elif "not following" in result.lower():
                return jsonify({"error": result}), 400
            return jsonify({"error": result}), 500

        return jsonify({"message": "Successfully unfollowed artist"}), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@artists_bp.route("/<int:artist_id>/relationship", methods=["GET"])
@login_required
def get_relationship(artist_id, user_id):
    """
    Check if current user is following an artist

    Returns:
        200: Relationship status
        404: Artist not found
        500: Server error
    """
    try:
        success, result = ArtistService.get_follow_relationship(user_id, artist_id)

        if not success:
            if "not found" in result.lower():
                return jsonify({"error": result}), 404
            return jsonify({"error": result}), 500

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@artists_bp.route("/me/artworks/<int:artwork_id>", methods=["GET"])
@artist_required
def get_my_artwork_detail(artwork_id, user_id):
    """
    Get detailed information about an artwork owned by the current artist

    Returns:
        200: Artwork details with tracks
        403: Artwork not owned by this artist
        404: Artwork not found
        500: Server error
    """
    try:
        success, result = ArtistService.get_artwork_detail(user_id, artwork_id)

        if not success:
            if "not found" in result.lower():
                return jsonify({"error": result}), 404
            elif "not owned" in result.lower() or "permission" in result.lower():
                return jsonify({"error": result}), 403
            return jsonify({"error": result}), 500

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@artists_bp.route("/me/artworks/<int:artwork_id>", methods=["DELETE"])
@artist_required
def delete_my_artwork(artwork_id, user_id):
    """
    Delete an artwork owned by the current artist

    Returns:
        200: Artwork deleted successfully
        403: Artwork not owned by this artist
        404: Artwork not found
        500: Server error
    """
    try:
        success, result = ArtistService.delete_artwork(user_id, artwork_id)

        if not success:
            if "not found" in result.lower():
                return jsonify({"error": result}), 404
            elif "not owned" in result.lower() or "permission" in result.lower():
                return jsonify({"error": result}), 403
            return jsonify({"error": result}), 500

        return jsonify({"message": "Artwork deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@artists_bp.route("/me/artworks", methods=["POST"])
@artist_required
def create_artwork(user_id):
    """
    Create a new artwork (Single or Album) with file uploads to S3

    Request Body (multipart/form-data):
        - mode: 'single' or 'album' (required)
        - title: Artwork title (required)
        - genre: Genre name (required)
        - cover_image: Cover image file (required)
        - track_files[]: Audio files array (required, 1 for single, N for album)
        - track_titles[]: Track titles array (required, same length as track_files)
        - track_numbers[]: Track numbers array (optional, for album ordering)
        - collaborations[]: Collaborator usernames array (optional, without @)

    Returns:
        201: Artwork created successfully
        400: Validation error
        401: Not authenticated
        403: Not an artist
        500: Server error
    """
    try:
        # Validate required fields
        mode = request.form.get("mode")
        title = request.form.get("title")
        genre = request.form.get("genre")
        cover_image = request.files.get("cover_image")

        if not mode or mode not in ["single", "album"]:
            return jsonify({"error": "Mode must be 'single' or 'album'"}), 400

        if not title or not title.strip():
            return jsonify({"error": "Title is required"}), 400

        if not genre or not genre.strip():
            return jsonify({"error": "Genre is required"}), 400

        if not cover_image:
            return jsonify({"error": "Cover image is required"}), 400

        # Get track files and titles
        track_files = request.files.getlist("track_files[]")
        track_titles = request.form.getlist("track_titles[]")
        track_numbers = request.form.getlist("track_numbers[]")
        collaborations = request.form.getlist("collaborations[]")

        if not track_files or len(track_files) == 0:
            return jsonify({"error": "At least one track file is required"}), 400

        if len(track_titles) != len(track_files):
            return jsonify({"error": "Track titles count must match track files count"}), 400

        if mode == "single" and len(track_files) != 1:
            return jsonify({"error": "Single mode requires exactly one track"}), 400

        # Validate file types
        allowed_audio_types = {"audio/mpeg", "audio/mp3", "audio/wav", "audio/x-wav"}
        allowed_image_types = {"image/jpeg", "image/jpg", "image/png", "image/gif", "image/webp"}

        if cover_image.content_type not in allowed_image_types:
            return jsonify({"error": f"Invalid cover image type: {cover_image.content_type}"}), 400

        for i, track_file in enumerate(track_files):
            if track_file.content_type not in allowed_audio_types:
                return jsonify({"error": f"Invalid audio type for track {i + 1}: {track_file.content_type}"}), 400

        # Call service to create artwork
        success, result = ArtistService.create_artwork(
            user_id=user_id,
            mode=mode,
            title=title.strip(),
            genre=genre.strip(),
            cover_image=cover_image,
            track_files=track_files,
            track_titles=[t.strip() for t in track_titles],
            track_numbers=[int(n) if n else i + 1 for i, n in enumerate(track_numbers)] if track_numbers else None,
            collaborations=[c.strip().lstrip("@") for c in collaborations if c.strip()]
        )

        if not success:
            return jsonify({"error": result}), 500

        return jsonify({
            "message": "Artwork created successfully",
            "artwork": result
        }), 201

    except ValueError as e:
        return jsonify({"error": f"Invalid value: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500