"""
Validation schemas for payments
"""


def validate_payment_creation(data):
    """
    Validate payment creation data

    Args:
        data (dict): Payment data

    Returns:
        tuple: (is_valid: bool, errors: list)
    """
    errors = []

    # Required fields
    if 'payment_method' not in data or not data['payment_method']:
        errors.append('payment_method is required')
    elif data['payment_method'].lower() not in ['momo', 'visa', 'mastercard']:
        errors.append('payment_method must be one of: momo, visa, mastercard')

    if 'amount' not in data:
        errors.append('amount is required')
    elif not isinstance(data['amount'], (int, float)) or data['amount'] <= 0:
        errors.append('amount must be a positive number')

    # Card validation for non-momo payments
    if data.get('payment_method', '').lower() in ['visa', 'mastercard']:
        if not data.get('card_number'):
            errors.append('card_number is required for card payments')

        if not data.get('card_holder_name'):
            errors.append('card_holder_name is required for card payments')

    return len(errors) == 0, errors
