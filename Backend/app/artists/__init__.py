"""
Artists module for artist-specific operations
"""
from flask import Blueprint

from .routes import artists_bp

__all__ = ['artists_bp']
