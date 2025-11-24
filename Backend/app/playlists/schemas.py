"""
Schema validation for playlist module
"""


def validate_playlist_create(data):
    """
    Validate playlist creation data

    Args:
        data (dict): Request data to validate

    Returns:
        tuple: (is_valid: bool, errors: dict)
    """
    errors = {}

    # Validate name
    if 'name' not in data:
        errors['name'] = 'Name is required'
    elif not isinstance(data['name'], str):
        errors['name'] = 'Name must be a string'
    elif not data['name'].strip():
        errors['name'] = 'Name cannot be empty'
    elif len(data['name']) > 255:
        errors['name'] = 'Name must not exceed 255 characters'

    return len(errors) == 0, errors


def validate_playlist_update(data):
    """
    Validate playlist update data

    Args:
        data (dict): Request data to validate

    Returns:
        tuple: (is_valid: bool, errors: dict)
    """
    errors = {}

    # Check if name is provided
    if 'name' not in data:
        errors['general'] = 'Name field is required for update'
        return False, errors

    # Validate name if provided
    if not isinstance(data['name'], str):
        errors['name'] = 'Name must be a string'
    elif not data['name'].strip():
        errors['name'] = 'Name cannot be empty'
    elif len(data['name']) > 255:
        errors['name'] = 'Name must not exceed 255 characters'

    return len(errors) == 0, errors


def validate_add_song(data):
    """
    Validate add song to playlist data

    Args:
        data (dict): Request data to validate

    Returns:
        tuple: (is_valid: bool, errors: dict)
    """
    errors = {}

    # Validate song_id
    if 'song_id' not in data:
        errors['song_id'] = 'Song ID is required'
    elif not isinstance(data['song_id'], int):
        errors['song_id'] = 'Song ID must be an integer'

    # Validate order_index (optional)
    if 'order_index' in data:
        if not isinstance(data['order_index'], int):
            errors['order_index'] = 'Order index must be an integer'
        elif data['order_index'] < 0:
            errors['order_index'] = 'Order index must be non-negative'

    return len(errors) == 0, errors
