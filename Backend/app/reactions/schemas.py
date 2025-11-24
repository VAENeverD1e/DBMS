"""
Schema validation for reactions module
"""


def validate_reaction_create(data):
    """
    Validate reaction creation data

    Args:
        data (dict): Request data to validate

    Returns:
        tuple: (is_valid: bool, errors: dict)
    """
    errors = {}

    # Validate reactable_type (required)
    if 'reactable_type' not in data:
        errors['reactable_type'] = 'reactable_type is required'
    elif data['reactable_type'] not in ['Song', 'Artwork']:
        errors['reactable_type'] = 'reactable_type must be either "Song" or "Artwork"'

    # Validate reactable_id (required)
    if 'reactable_id' not in data:
        errors['reactable_id'] = 'reactable_id is required'
    elif not isinstance(data['reactable_id'], int) or data['reactable_id'] <= 0:
        errors['reactable_id'] = 'reactable_id must be a positive integer'

    # Validate emotion (optional, defaults to 'Like')
    if 'emotion' in data:
        emotion = data['emotion']
        if emotion not in ['Like', 'Love', 'Dislike']:
            errors['emotion'] = 'emotion must be one of: "Like", "Love", "Dislike"'

    return len(errors) == 0, errors
