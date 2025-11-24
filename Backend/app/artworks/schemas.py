"""
Schema validation for artwork module
"""


def validate_artwork_create(data):
    """
    Validate artwork creation data

    Args:
        data (dict): Request data to validate

    Returns:
        tuple: (is_valid: bool, errors: dict)
    """
    errors = {}

    # Validate title
    if 'title' not in data:
        errors['title'] = 'Title is required'
    elif not isinstance(data['title'], str):
        errors['title'] = 'Title must be a string'
    elif not data['title'].strip():
        errors['title'] = 'Title cannot be empty'
    elif len(data['title']) > 255:
        errors['title'] = 'Title must not exceed 255 characters'

    # Validate type
    if 'type' not in data:
        errors['type'] = 'Type is required'
    elif data['type'] not in ['Album', 'Single']:
        errors['type'] = 'Type must be either "Album" or "Single"'

    # Validate genre (optional)
    if 'genre' in data:
        if not isinstance(data['genre'], str):
            errors['genre'] = 'Genre must be a string'
        elif len(data['genre']) > 100:
            errors['genre'] = 'Genre must not exceed 100 characters'

    # Validate release_date (optional)
    if 'release_date' in data:
        if not isinstance(data['release_date'], str):
            errors['release_date'] = 'Release date must be a string (YYYY-MM-DD format)'
        # Additional date format validation could be added here

    # Validate cover_image (optional)
    if 'cover_image' in data:
        if not isinstance(data['cover_image'], str):
            errors['cover_image'] = 'Cover image must be a string (URL)'
        elif len(data['cover_image']) > 500:
            errors['cover_image'] = 'Cover image URL must not exceed 500 characters'

    return len(errors) == 0, errors


def validate_artwork_update(data):
    """
    Validate artwork update data

    Args:
        data (dict): Request data to validate

    Returns:
        tuple: (is_valid: bool, errors: dict)
    """
    errors = {}

    # At least one field must be provided
    allowed_fields = ['title', 'genre', 'cover_image', 'release_date']
    has_valid_field = any(field in data for field in allowed_fields)

    if not has_valid_field:
        errors['general'] = 'At least one field must be provided for update'
        return False, errors

    # Validate title if provided
    if 'title' in data:
        if not isinstance(data['title'], str):
            errors['title'] = 'Title must be a string'
        elif not data['title'].strip():
            errors['title'] = 'Title cannot be empty'
        elif len(data['title']) > 255:
            errors['title'] = 'Title must not exceed 255 characters'

    # Validate genre if provided
    if 'genre' in data:
        if not isinstance(data['genre'], str):
            errors['genre'] = 'Genre must be a string'
        elif len(data['genre']) > 100:
            errors['genre'] = 'Genre must not exceed 100 characters'

    # Validate cover_image if provided
    if 'cover_image' in data:
        if not isinstance(data['cover_image'], str):
            errors['cover_image'] = 'Cover image must be a string (URL)'
        elif len(data['cover_image']) > 500:
            errors['cover_image'] = 'Cover image URL must not exceed 500 characters'

    # Validate release_date if provided
    if 'release_date' in data:
        if not isinstance(data['release_date'], str):
            errors['release_date'] = 'Release date must be a string (YYYY-MM-DD format)'

    return len(errors) == 0, errors
