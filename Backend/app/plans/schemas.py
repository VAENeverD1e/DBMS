"""
Validation schemas for plans
"""


def validate_plan_creation(data):
    """
    Validate plan creation data

    Args:
        data (dict): Plan data

    Returns:
        tuple: (is_valid: bool, errors: list)
    """
    errors = []

    # Required fields
    if 'name' not in data or not data['name']:
        errors.append('name is required')

    if 'price' not in data:
        errors.append('price is required')
    elif not isinstance(data['price'], (int, float)) or data['price'] < 0:
        errors.append('price must be a non-negative number')

    if 'duration_days' not in data:
        errors.append('duration_days is required')
    elif not isinstance(data['duration_days'], int) or data['duration_days'] <= 0:
        errors.append('duration_days must be a positive integer')

    if 'role_granted' not in data or data['role_granted'] not in ['Listener', 'Artist']:
        errors.append('role_granted must be either "Listener" or "Artist"')

    # Optional fields validation
    if 'description' in data and data['description'] and len(data['description']) > 500:
        errors.append('description must be 500 characters or less')

    return len(errors) == 0, errors
