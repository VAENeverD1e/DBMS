from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.songs.schemas import SongSearchSchema, GenreSearchSchema
from app.songs.services import SongsService

songs_bp = Blueprint('songs', __name__, url_prefix='/api/songs')
songs_service = SongsService()

@songs_bp.route('/search', methods=['GET'])
def search_songs():
    """
    Search for songs from Jamendo
    
    Query Parameters:
        - query (required): Search term
        - limit (optional): Number of results (1-100, default: 20)
        - offset (optional): Pagination offset (default: 0)
    
    Example:
        GET /api/songs/search?query=jazz&limit=10
    """
    try:
        schema = SongSearchSchema()
        params = schema.load({
            'query': request.args.get('query'),
            'limit': request.args.get('limit', 20, type=int),
            'offset': request.args.get('offset', 0, type=int)
        })
    except ValidationError as err:
        return jsonify({'error': 'Invalid parameters', 'messages': err.messages}), 400
    
    songs = songs_service.search_songs(
        query=params['query'],
        limit=params['limit'],
        offset=params['offset']
    )
    
    if songs is None:
        return jsonify({'error': 'Failed to search songs from Jamendo API'}), 500
    
    return jsonify({
        'success': True,
        'count': len(songs),
        'query': params['query'],
        'limit': params['limit'],
        'offset': params['offset'],
        'songs': songs
    }), 200

@songs_bp.route('/genre/<genre>', methods=['GET'])
def get_songs_by_genre(genre):
    """
    Get songs by genre/tag from Jamendo
    
    Path Parameters:
        - genre: Genre or tag name (e.g., 'rock', 'jazz', 'electronic')
        
    Query Parameters:
        - limit (optional): Number of results (1-100, default: 20)
    
    Example:
        GET /api/songs/genre/rock?limit=15
    """
    try:
        schema = GenreSearchSchema()
        params = schema.load({
            'genre': genre,
            'limit': request.args.get('limit', 20, type=int)
        })
    except ValidationError as err:
        return jsonify({'error': 'Invalid parameters', 'messages': err.messages}), 400
    
    songs = songs_service.get_songs_by_genre(
        genre=params['genre'],
        limit=params['limit']
    )
    
    if songs is None:
        return jsonify({'error': 'Failed to fetch songs from Jamendo API'}), 500
    
    return jsonify({
        'success': True,
        'count': len(songs),
        'genre': params['genre'],
        'limit': params['limit'],
        'songs': songs
    }), 200

@songs_bp.route('/<jamendo_id>', methods=['GET'])
def get_song(jamendo_id):
    """
    Get a specific song by Jamendo ID
    
    Path Parameters:
        - jamendo_id: Jamendo track ID
    
    Example:
        GET /api/songs/12345678
    """
    song = songs_service.get_song_by_id(jamendo_id)
    
    if not song:
        return jsonify({'error': 'Song not found'}), 404
    
    return jsonify({
        'success': True,
        'song': song
    }), 200
