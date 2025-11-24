"""
Schema validation for songs module
"""


def validate_song_create(data):
    """
    Validate song creation data

    Args:
        data (dict): Request data to validate

    Returns:
        tuple: (is_valid: bool, errors: dict)
    """
    errors = {}

    # Validate artwork_id (required)
    if 'artwork_id' not in data:
        errors['artwork_id'] = 'artwork_id is required'
    elif not isinstance(data['artwork_id'], int) or data['artwork_id'] <= 0:
        errors['artwork_id'] = 'artwork_id must be a positive integer'

    # Validate title (required)
    if 'title' not in data:
        errors['title'] = 'title is required'
    elif not isinstance(data['title'], str):
        errors['title'] = 'title must be a string'
    elif not data['title'].strip():
        errors['title'] = 'title cannot be empty'
    elif len(data['title']) > 255:
        errors['title'] = 'title must not exceed 255 characters'

    # Validate track_number (required)
    if 'track_number' not in data:
        errors['track_number'] = 'track_number is required'
    elif not isinstance(data['track_number'], int) or data['track_number'] <= 0:
        errors['track_number'] = 'track_number must be a positive integer'

    # Validate duration (required, in seconds)
    if 'duration' not in data:
        errors['duration'] = 'duration is required'
    elif not isinstance(data['duration'], (int, float)) or data['duration'] <= 0:
        errors['duration'] = 'duration must be a positive number (in seconds)'

    # Validate audio_file_url (required)
    if 'audio_file_url' not in data:
        errors['audio_file_url'] = 'audio_file_url is required'
    elif not isinstance(data['audio_file_url'], str):
        errors['audio_file_url'] = 'audio_file_url must be a string'
    elif not data['audio_file_url'].strip():
        errors['audio_file_url'] = 'audio_file_url cannot be empty'
    elif len(data['audio_file_url']) > 500:
        errors['audio_file_url'] = 'audio_file_url must not exceed 500 characters'

    # Validate release_date (optional)
    if 'release_date' in data and data['release_date']:
        if not isinstance(data['release_date'], str):
            errors['release_date'] = 'release_date must be a string in YYYY-MM-DD format'

    return len(errors) == 0, errors


def validate_song_update(data):
    """
    Validate song update data

    Args:
        data (dict): Request data to validate

    Returns:
        tuple: (is_valid: bool, errors: dict)
    """
    errors = {}

    # At least one field should be provided
    if not data or not any(key in data for key in ['title', 'track_number', 'duration', 'audio_file_url', 'release_date']):
        errors['general'] = 'At least one field must be provided for update (title, track_number, duration, audio_file_url, release_date)'
        return False, errors

    # Validate title (optional)
    if 'title' in data:
        if not isinstance(data['title'], str):
            errors['title'] = 'title must be a string'
        elif not data['title'].strip():
            errors['title'] = 'title cannot be empty'
        elif len(data['title']) > 255:
            errors['title'] = 'title must not exceed 255 characters'

    # Validate track_number (optional)
    if 'track_number' in data:
        if not isinstance(data['track_number'], int) or data['track_number'] <= 0:
            errors['track_number'] = 'track_number must be a positive integer'

    # Validate duration (optional, in seconds)
    if 'duration' in data:
        if not isinstance(data['duration'], (int, float)) or data['duration'] <= 0:
            errors['duration'] = 'duration must be a positive number (in seconds)'

    # Validate audio_file_url (optional)
    if 'audio_file_url' in data:
        if not isinstance(data['audio_file_url'], str):
            errors['audio_file_url'] = 'audio_file_url must be a string'
        elif not data['audio_file_url'].strip():
            errors['audio_file_url'] = 'audio_file_url cannot be empty'
        elif len(data['audio_file_url']) > 500:
            errors['audio_file_url'] = 'audio_file_url must not exceed 500 characters'

    # Validate release_date (optional)
    if 'release_date' in data and data['release_date']:
        if not isinstance(data['release_date'], str):
            errors['release_date'] = 'release_date must be a string in YYYY-MM-DD format'

    return len(errors) == 0, errors
