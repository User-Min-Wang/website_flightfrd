from flask import Blueprint


# Create the API v1 blueprint
bp = Blueprint('v1', __name__, url_prefix='/v1')

# Import API routes to register them
from app.api.v1 import aircraft, flights, images, atc, calendar