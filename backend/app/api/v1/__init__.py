from flask import Blueprint

# Create the API v1 blueprint
bp = Blueprint('v1', __name__)

# Import sub-blueprints (they will be registered in app/__init__.py)
from app.api.v1 import aircraft, flights, images, atc, calendar, auth