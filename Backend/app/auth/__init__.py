"""
Authentication module for user registration, login, and profile management
"""
from .routes import auth_bp
from .utils import login_required, role_required, get_current_user

__all__ = ['auth_bp', 'login_required', 'role_required', 'get_current_user']
