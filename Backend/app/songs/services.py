from services.jamendo_service import JamendoService
from typing import Optional, List, Dict

class SongsService:
    def __init__(self):
        self.jamendo_service = JamendoService()
    
    def search_songs(self, query: str, limit: int = 20, offset: int = 0) -> Optional[List[Dict]]:
        """
        Search for songs from Jamendo API
        
        Args:
            query: Search term (song title, artist name, etc.)
            limit: Number of results (default: 20, max: 100)
            offset: Pagination offset (default: 0)
        
        Returns:
            List of formatted song dictionaries or None if error
        """
        response = self.jamendo_service.search_tracks(query, limit, offset)
        
        if not response:
            return None
        
        # Format the results
        songs = []
        for track in response.get('results', []):
            formatted_song = self.jamendo_service.format_track_response(track)
            songs.append(formatted_song)
        
        return songs
    
    def get_songs_by_genre(self, genre: str, limit: int = 20) -> Optional[List[Dict]]:
        """
        Get songs by genre/tag from Jamendo API
        
        Args:
            genre: Genre or tag name
            limit: Number of results (default: 20, max: 100)
        
        Returns:
            List of formatted song dictionaries or None if error
        """
        response = self.jamendo_service.get_tracks_by_genre(genre, limit)
        
        if not response:
            return None
        
        # Format the results
        songs = []
        for track in response.get('results', []):
            formatted_song = self.jamendo_service.format_track_response(track)
            songs.append(formatted_song)
        
        return songs
    
    def get_song_by_id(self, jamendo_id: str) -> Optional[Dict]:
        """
        Get a specific song by Jamendo ID
        
        Args:
            jamendo_id: Jamendo track ID
        
        Returns:
            Formatted song dictionary or None if not found/error
        """
        track = self.jamendo_service.get_track_by_id(jamendo_id)
        
        if not track:
            return None
        
        return self.jamendo_service.format_track_response(track)
