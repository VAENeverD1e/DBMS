import os
import requests
from typing import Optional, Dict, List

class JamendoService:
    def __init__(self):
        self.base_url = os.getenv('JAMENDO_API_BASEURL', 'https://api.jamendo.com/v3.0')
        self.client_id = os.getenv('JAMENDO_CLIENT_ID', 'f72ed6e5')
        
        if not self.client_id:
            raise ValueError("JAMENDO_CLIENT_ID environment variable is required")
    
    def search_tracks(self, query: str, limit: int = 20, offset: int = 0) -> Optional[Dict]:
        """
        Search for tracks on Jamendo
        """
        params = {
            'client_id': self.client_id,
            'format': 'json',
            'search': query,
            'limit': limit,
            'offset': offset,
            'include': 'musicinfo',  # Include additional metadata
            'audioformat': 'mp32'    # Get MP3 audio format
        }
        
        try:
            response = requests.get(f"{self.base_url}/tracks/", params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error calling Jamendo API: {e}")
            return None
    
    def get_track_by_id(self, track_id: str) -> Optional[Dict]:
        """
        Get a specific track by Jamendo ID
        """
        params = {
            'client_id': self.client_id,
            'format': 'json',
            'id': track_id,
            'include': 'musicinfo',
            'audioformat': 'mp32'
        }
        
        try:
            response = requests.get(f"{self.base_url}/tracks/", params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('results') and len(data['results']) > 0:
                return data['results'][0]
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error calling Jamendo API: {e}")
            return None
    
    def get_tracks_by_genre(self, genre: str, limit: int = 20) -> Optional[Dict]:
        """
        Get tracks by genre/tag
        """
        params = {
            'client_id': self.client_id,
            'format': 'json',
            'tags': genre,
            'limit': limit,
            'include': 'musicinfo',
            'audioformat': 'mp32',
            'featured': '1'  # Get featured tracks
        }
        
        try:
            response = requests.get(f"{self.base_url}/tracks/", params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error calling Jamendo API: {e}")
            return None
    
    def format_track_response(self, jamendo_track: Dict) -> Dict:
        """
        Format Jamendo track data for our frontend
        """
        return {
            'jamendo_id': jamendo_track.get('id'),
            'title': jamendo_track.get('name', ''),
            'artist': jamendo_track.get('artist_name', ''),
            'album': jamendo_track.get('album_name', ''),
            'duration': jamendo_track.get('duration'),
            'image_url': jamendo_track.get('image', ''),
            'audio_url': jamendo_track.get('audio', ''),
            'license': jamendo_track.get('license_ccurl', '').split('/')[-2] if jamendo_track.get('license_ccurl') else 'Unknown',
            'license_url': jamendo_track.get('license_ccurl', ''),
            'release_date': jamendo_track.get('releasedate', ''),
            'genre': jamendo_track.get('musicinfo', {}).get('tags', {}).get('genres', []) if jamendo_track.get('musicinfo') else []
        }
    
    def search_albums(self, query: str, limit: int = 20, offset: int = 0) -> Optional[Dict]:
        """
        Search for albums on Jamendo
        """
        params = {
            'client_id': self.client_id,
            'format': 'json',
            'search': query,
            'limit': limit,
            'offset': offset,
            'include': 'musicinfo'
        }
        
        try:
            response = requests.get(f"{self.base_url}/albums/", params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error calling Jamendo API: {e}")
            return None
    
    def get_album_by_id(self, album_id: str) -> Optional[Dict]:
        """
        Get a specific album by Jamendo ID
        """
        params = {
            'client_id': self.client_id,
            'format': 'json',
            'id': album_id,
            'include': 'musicinfo'
        }
        
        try:
            response = requests.get(f"{self.base_url}/albums/", params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('results') and len(data['results']) > 0:
                return data['results'][0]
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error calling Jamendo API: {e}")
            return None
    
    def get_albums_by_genre(self, genre: str, limit: int = 20) -> Optional[Dict]:
        """
        Get albums by genre/tag
        """
        params = {
            'client_id': self.client_id,
            'format': 'json',
            'tags': genre,
            'limit': limit,
            'include': 'musicinfo',
            'featured': '1'  # Get featured albums
        }
        
        try:
            response = requests.get(f"{self.base_url}/albums/", params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error calling Jamendo API: {e}")
            return None
    
    def get_album_tracks(self, album_id: str, limit: int = 100) -> Optional[Dict]:
        """
        Get all tracks within an album
        """
        params = {
            'client_id': self.client_id,
            'format': 'json',
            'album_id': album_id,
            'limit': limit,
            'include': 'musicinfo',
            'audioformat': 'mp32'
        }
        
        try:
            response = requests.get(f"{self.base_url}/tracks/", params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error calling Jamendo API: {e}")
            return None
    
    def format_album_response(self, jamendo_album: Dict) -> Dict:
        """
        Format Jamendo album data for our frontend
        """
        return {
            'jamendo_id': jamendo_album.get('id'),
            'title': jamendo_album.get('name', ''),
            'artist': jamendo_album.get('artist_name', ''),
            'image_url': jamendo_album.get('image', ''),
            'release_date': jamendo_album.get('releasedate', ''),
            'track_count': jamendo_album.get('tracks_count', 0),
            'license': jamendo_album.get('license_ccurl', '').split('/')[-2] if jamendo_album.get('license_ccurl') else 'Unknown',
            'license_url': jamendo_album.get('license_ccurl', ''),
            'genre': jamendo_album.get('musicinfo', {}).get('tags', {}).get('genres', []) if jamendo_album.get('musicinfo') else []
        }
