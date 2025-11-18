"""
Request validation schemas for authentication endpoints
"""
import re


def validate_email(email):
    """
    Validate email format

    Args:
        email (str): Email address to validate

    Returns:
        bool: True if valid, False otherwise
    """
    if not email:
        return False

    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email) is not None


def validate_password(password):
    """
    Validate password strength
    Requirements:
    - At least 8 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one number

    Args:
        password (str): Password to validate

    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if not password:
        return False, "Password is required"

    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"

    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"

    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"

    return True, ""


def validate_username(username):
    """
    Validate username format
    Requirements:
    - 3-100 characters
    - Alphanumeric and underscores only
    - Cannot start with a number

    Args:
        username (str): Username to validate

    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if not username:
        return False, "Username is required"

    if len(username) < 3:
        return False, "Username must be at least 3 characters long"

    if len(username) > 100:
        return False, "Username must be at most 100 characters long"

    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', username):
        return False, "Username must start with a letter and contain only letters, numbers, and underscores"

    return True, ""


def validate_registration_data(data):
    """
    Validate registration request data

    Args:
        data (dict): Registration data

    Returns:
        tuple: (bool, dict) - (is_valid, errors_dict)
    """
    errors = {}

    # Validate required fields
    if 'email' not in data or not data['email']:
        errors['email'] = "Email is required"
    elif not validate_email(data['email']):
        errors['email'] = "Invalid email format"

    if 'password' not in data or not data['password']:
        errors['password'] = "Password is required"
    else:
        is_valid, error_msg = validate_password(data['password'])
        if not is_valid:
            errors['password'] = error_msg

    if 'username' not in data or not data['username']:
        errors['username'] = "Username is required"
    else:
        is_valid, error_msg = validate_username(data['username'])
        if not is_valid:
            errors['username'] = error_msg

    # Validate role
    if 'role' in data and data['role']:
        if data['role'] not in ['Guest', 'Listener', 'Artist']:
            errors['role'] = "Role must be 'Guest', 'Listener', or 'Artist'"

    # Optional fields validation
    if 'first_name' in data and data['first_name']:
        if len(data['first_name']) > 100:
            errors['first_name'] = "First name must be at most 100 characters"

    if 'last_name' in data and data['last_name']:
        if len(data['last_name']) > 100:
            errors['last_name'] = "Last name must be at most 100 characters"

    return len(errors) == 0, errors


def validate_login_data(data):
    """
    Validate login request data

    Args:
        data (dict): Login data

    Returns:
        tuple: (bool, dict) - (is_valid, errors_dict)
    """
    errors = {}

    # Accept either email or username
    if ('email' not in data or not data['email']) and ('username' not in data or not data['username']):
        errors['login'] = "Email or username is required"

    if 'password' not in data or not data['password']:
        errors['password'] = "Password is required"

    return len(errors) == 0, errors


def validate_profile_update_data(data):
    """
    Validate profile update request data

    Args:
        data (dict): Profile update data

    Returns:
        tuple: (bool, dict) - (is_valid, errors_dict)
    """
    errors = {}

    # Email validation (if provided)
    if 'email' in data and data['email']:
        if not validate_email(data['email']):
            errors['email'] = "Invalid email format"

    # Username validation (if provided)
    if 'username' in data and data['username']:
        is_valid, error_msg = validate_username(data['username'])
        if not is_valid:
            errors['username'] = error_msg

    # First name validation (if provided)
    if 'first_name' in data and data['first_name']:
        if len(data['first_name']) > 100:
            errors['first_name'] = "First name must be at most 100 characters"

    # Last name validation (if provided)
    if 'last_name' in data and data['last_name']:
        if len(data['last_name']) > 100:
            errors['last_name'] = "Last name must be at most 100 characters"

    return len(errors) == 0, errors


def validate_password_change_data(data):
    """
    Validate password change request data

    Args:
        data (dict): Password change data

    Returns:
        tuple: (bool, dict) - (is_valid, errors_dict)
    """
    errors = {}

    if 'current_password' not in data or not data['current_password']:
        errors['current_password'] = "Current password is required"

    if 'new_password' not in data or not data['new_password']:
        errors['new_password'] = "New password is required"
    else:
        is_valid, error_msg = validate_password(data['new_password'])
        if not is_valid:
            errors['new_password'] = error_msg

    if 'confirm_password' not in data or not data['confirm_password']:
        errors['confirm_password'] = "Password confirmation is required"
    elif data.get('new_password') != data.get('confirm_password'):
        errors['confirm_password'] = "Passwords do not match"

    return len(errors) == 0, errors
