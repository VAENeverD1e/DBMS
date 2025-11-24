"""
Schema validation for artist module
"""


def validate_artist_profile_update(data):
    """
    Validate artist profile update data

    Args:
        data (dict): Request data to validate

    Returns:
        tuple: (is_valid: bool, errors: dict)
    """
    errors = {}

    # Check if at least one field is provided
    if not any(key in data for key in ['genre']):
        errors['general'] = 'At least one field must be provided for update'

    # Validate genre if provided
    if 'genre' in data:
        genre = data['genre']
        if genre and not isinstance(genre, str):
            errors['genre'] = 'Genre must be a string'
        elif genre and len(genre) > 100:
            errors['genre'] = 'Genre must not exceed 100 characters'

    return len(errors) == 0, errors


def validate_social_links_update(data):
    """
    Validate social media links update data

    Args:
        data (dict): Request data to validate

    Returns:
        tuple: (is_valid: bool, errors: dict)
    """
    errors = {}

    # Check if social_links is provided
    if 'social_links' not in data:
        errors['general'] = 'social_links field is required'
        return False, errors

    # Validate social_links
    social_links = data['social_links']
    if social_links is not None:
        if not isinstance(social_links, str):
            errors['social_links'] = 'Social links must be a string'
        elif len(social_links) > 500:
            errors['social_links'] = 'Social links must not exceed 500 characters'

    return len(errors) == 0, errors
