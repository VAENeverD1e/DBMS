from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.artworks.schemas import AlbumSearchSchema, GenreSearchSchema
from app.artworks.services import ArtworksService

artworks_bp = Blueprint('artworks', __name__, url_prefix='/api/artworks')
artworks_service = ArtworksService()


@artworks_bp.route('/search', methods=['GET'])
def search_albums():
    """
    Search for albums from Jamendo
    
    Query Parameters:
        - query (required): Search term
        - limit (optional): Number of results (1-100, default: 20)
        - offset (optional): Pagination offset (default: 0)
    
    Example:
        GET /api/artworks/search?query=electronic&limit=10
    """
    try:
        schema = AlbumSearchSchema()
        params = schema.load({
            'query': request.args.get('query'),
            'limit': request.args.get('limit', 20, type=int),
            'offset': request.args.get('offset', 0, type=int)
        })
    except ValidationError as err:
        return jsonify({'error': 'Invalid parameters', 'messages': err.messages}), 400
    
    albums = artworks_service.search_albums(
        query=params['query'],
        limit=params['limit'],
        offset=params['offset']
    )
    
    if albums is None:
        return jsonify({'error': 'Failed to search albums from Jamendo API'}), 500
    
    return jsonify({
        'success': True,
        'count': len(albums),
        'query': params['query'],
        'limit': params['limit'],
        'offset': params['offset'],
        'albums': albums
    }), 200


@artworks_bp.route('/genre/<genre>', methods=['GET'])
def get_albums_by_genre(genre):
    """
    Get albums by genre/tag from Jamendo
    
    Path Parameters:
        - genre: Genre or tag name (e.g., 'rock', 'jazz', 'electronic')
        
    Query Parameters:
        - limit (optional): Number of results (1-100, default: 20)
    
    Example:
        GET /api/artworks/genre/rock?limit=15
    """
    try:
        schema = GenreSearchSchema()
        params = schema.load({
            'genre': genre,
            'limit': request.args.get('limit', 20, type=int)
        })
    except ValidationError as err:
        return jsonify({'error': 'Invalid parameters', 'messages': err.messages}), 400
    
    albums = artworks_service.get_albums_by_genre(
        genre=params['genre'],
        limit=params['limit']
    )
    
    if albums is None:
        return jsonify({'error': 'Failed to fetch albums from Jamendo API'}), 500
    
    return jsonify({
        'success': True,
        'count': len(albums),
        'genre': params['genre'],
        'limit': params['limit'],
        'albums': albums
    }), 200


@artworks_bp.route('/<jamendo_id>', methods=['GET'])
def get_album(jamendo_id):
    """
    Get a specific album by Jamendo ID
    
    Path Parameters:
        - jamendo_id: Jamendo album ID
    
    Example:
        GET /api/artworks/12345678
    """
    album = artworks_service.get_album_by_id(jamendo_id)
    
    if not album:
        return jsonify({'error': 'Album not found'}), 404
    
    return jsonify({
        'success': True,
        'album': album
    }), 200


@artworks_bp.route('/<jamendo_id>/tracks', methods=['GET'])
def get_album_tracks(jamendo_id):
    """
    Get all tracks within an album
    
    Path Parameters:
        - jamendo_id: Jamendo album ID
    
    Example:
        GET /api/artworks/12345678/tracks
    """
    album = artworks_service.get_album_by_id(jamendo_id)
    
    if not album:
        return jsonify({'error': 'Album not found'}), 404
    
    tracks = artworks_service.get_album_tracks(jamendo_id)
    
    if tracks is None:
        return jsonify({'error': 'Failed to fetch album tracks from Jamendo API'}), 500
    
    return jsonify({
        'success': True,
        'album_id': jamendo_id,
        'album_title': album.get('title'),
        'album_artist': album.get('artist'),
        'count': len(tracks),
        'tracks': tracks
    }), 200
