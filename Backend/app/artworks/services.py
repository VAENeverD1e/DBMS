from services.jamendo_service import JamendoService
from typing import Optional, List, Dict


class ArtworksService:
    def __init__(self):
        self.jamendo_service = JamendoService()
    
    def search_albums(self, query: str, limit: int = 20, offset: int = 0) -> Optional[List[Dict]]:
        """
        Search for albums from Jamendo API
        
        Args:
            query: Search term (album name, artist name, etc.)
            limit: Number of results (default: 20, max: 100)
            offset: Pagination offset (default: 0)
        
        Returns:
            List of formatted album dictionaries or None if error
        """
        response = self.jamendo_service.search_albums(query, limit, offset)
        
        if not response:
            return None
        
        # Format the results
        albums = []
        for album in response.get('results', []):
            formatted_album = self.jamendo_service.format_album_response(album)
            albums.append(formatted_album)
        
        return albums
    
    def get_albums_by_genre(self, genre: str, limit: int = 20) -> Optional[List[Dict]]:
        """
        Get albums by genre/tag from Jamendo API
        
        Args:
            genre: Genre or tag name
            limit: Number of results (default: 20, max: 100)
        
        Returns:
            List of formatted album dictionaries or None if error
        """
        response = self.jamendo_service.get_albums_by_genre(genre, limit)
        
        if not response:
            return None
        
        # Format the results
        albums = []
        for album in response.get('results', []):
            formatted_album = self.jamendo_service.format_album_response(album)
            albums.append(formatted_album)
        
        return albums
    
    def get_album_by_id(self, jamendo_id: str) -> Optional[Dict]:
        """
        Get a specific album by Jamendo ID
        
        Args:
            jamendo_id: Jamendo album ID
        
        Returns:
            Formatted album dictionary or None if not found/error
        """
        album = self.jamendo_service.get_album_by_id(jamendo_id)
        
        if not album:
            return None
        
        return self.jamendo_service.format_album_response(album)
    
    def get_album_tracks(self, jamendo_id: str) -> Optional[List[Dict]]:
        """
        Get all tracks within an album
        
        Args:
            jamendo_id: Jamendo album ID
        
        Returns:
            List of formatted track dictionaries or None if error
        """
        response = self.jamendo_service.get_album_tracks(jamendo_id)
        
        if not response:
            return None
        
        # Format the results
        tracks = []
        for track in response.get('results', []):
            formatted_track = self.jamendo_service.format_track_response(track)
            tracks.append(formatted_track)
        
        return tracks
