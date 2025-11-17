"""
Schema validation for user module
"""


def validate_preferences_update(data):
    """
    Validate listener preferences update data

    Args:
        data (dict): Request data to validate

    Returns:
        tuple: (is_valid: bool, errors: dict)
    """
    errors = {}

    # Check if at least one field is provided
    if not any(key in data for key in ['preference', 'favorite_genre']):
        errors['general'] = 'At least one field (preference or favorite_genre) must be provided'

    # Validate preference if provided
    if 'preference' in data:
        preference = data['preference']
        if preference and not isinstance(preference, str):
            errors['preference'] = 'Preference must be a string'
        elif preference and len(preference) > 500:
            errors['preference'] = 'Preference must not exceed 500 characters'

    # Validate favorite_genre if provided
    if 'favorite_genre' in data:
        favorite_genre = data['favorite_genre']
        if favorite_genre and not isinstance(favorite_genre, str):
            errors['favorite_genre'] = 'Favorite genre must be a string'
        elif favorite_genre and len(favorite_genre) > 100:
            errors['favorite_genre'] = 'Favorite genre must not exceed 100 characters'

    return len(errors) == 0, errors
