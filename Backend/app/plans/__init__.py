"""
Plans module initialization
"""
from flask import Blueprint

plans_bp = Blueprint('plans', __name__, url_prefix='/api/plans')

from . import routes
