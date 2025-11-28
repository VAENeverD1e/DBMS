import requests
import json
from pprint import pprint

BASE_URL = "http://localhost:5000/api/songs"

def test_search_songs():
    """Test searching for songs"""
    print("\n" + "="*60)
    print("TEST 1: Search Songs")
    print("="*60)
    
    params = {
        "query": "jazz",
        "limit": 5,
        "offset": 0
    }
    
    try:
        response = requests.get(f"{BASE_URL}/search", params=params)
        print(f"Status Code: {response.status_code}")
        print(f"Response:")
        pprint(response.json())
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_search_songs_advanced():
    """Test searching with different queries"""
    print("\n" + "="*60)
    print("TEST 2: Search Different Genres")
    print("="*60)
    
    queries = ["rock", "electronic", "classical", "hip-hop"]
    
    for query in queries:
        print(f"\n--- Searching for: {query} ---")
        params = {
            "query": query,
            "limit": 3
        }
        
        try:
            response = requests.get(f"{BASE_URL}/search", params=params)
            data = response.json()
            print(f"Found {data.get('count', 0)} songs")
            
            # Print first song details
            if data.get('songs'):
                song = data['songs'][0]
                print(f"  Top result: {song.get('title')} by {song.get('artist')}")
        except Exception as e:
            print(f"Error: {e}")

def test_get_by_genre():
    """Test getting songs by genre"""
    print("\n" + "="*60)
    print("TEST 3: Get Songs by Genre")
    print("="*60)
    
    genre = "rock"
    params = {"limit": 5}
    
    try:
        response = requests.get(f"{BASE_URL}/genre/{genre}", params=params)
        print(f"Status Code: {response.status_code}")
        print(f"Response:")
        data = response.json()
        pprint(data)
        
        # Extract jamendo_id for next test
        if data.get('songs'):
            return data['songs'][0].get('jamendo_id')
    except Exception as e:
        print(f"Error: {e}")
    return None

def test_get_song_by_id(jamendo_id):
    """Test getting a specific song by ID"""
    print("\n" + "="*60)
    print("TEST 4: Get Specific Song by ID")
    print("="*60)
    
    if not jamendo_id:
        print("No jamendo_id provided, skipping test")
        return
    
    print(f"Fetching song with ID: {jamendo_id}")
    
    try:
        response = requests.get(f"{BASE_URL}/{jamendo_id}")
        print(f"Status Code: {response.status_code}")
        print(f"Response:")
        pprint(response.json())
    except Exception as e:
        print(f"Error: {e}")

def test_pagination():
    """Test pagination"""
    print("\n" + "="*60)
    print("TEST 5: Pagination Test")
    print("="*60)
    
    query = "music"
    
    for offset in [0, 5, 10]:
        print(f"\n--- Offset: {offset} ---")
        params = {
            "query": query,
            "limit": 3,
            "offset": offset
        }
        
        try:
            response = requests.get(f"{BASE_URL}/search", params=params)
            data = response.json()
            
            if data.get('songs'):
                for i, song in enumerate(data['songs']):
                    print(f"  {i+1}. {song.get('title')} by {song.get('artist')}")
        except Exception as e:
            print(f"Error: {e}")

def test_error_cases():
    """Test error handling"""
    print("\n" + "="*60)
    print("TEST 6: Error Handling")
    print("="*60)
    
    # Test 1: Missing required parameter
    print("\n--- Test: Missing query parameter ---")
    try:
        response = requests.get(f"{BASE_URL}/search")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Invalid limit
    print("\n--- Test: Invalid limit (too high) ---")
    try:
        response = requests.get(f"{BASE_URL}/search", params={"query": "music", "limit": 500})
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Non-existent song
    print("\n--- Test: Non-existent song ID ---")
    try:
        response = requests.get(f"{BASE_URL}/999999999")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Starting Jamendo API Tests...")
    print("Make sure your Flask server is running on http://localhost:5000")
    
    # Run tests
    test_search_songs()
    test_search_songs_advanced()
    jamendo_id = test_get_by_genre()
    test_get_song_by_id(jamendo_id)
    test_pagination()
    test_error_cases()
    
    print("\n" + "="*60)
    print("All tests completed!")
    print("="*60)
