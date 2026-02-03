from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES
from app.api.v1 import bp


def register_error_handlers(app):
    """Register error handlers for the application"""
    app.register_error_handler(400, bad_request)
    app.register_error_handler(404, not_found)
    app.register_error_handler(500, internal_error)
    
    # Register with blueprint as well for API-specific errors
    bp.register_error_handler(400, bad_request)
    bp.register_error_handler(404, not_found)
    bp.register_error_handler(500, internal_error)


def error_response(status_code, message=None):
    """Generate error response with given status code and optional message"""
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


def bad_request(message=None):
    """Handle 400 Bad Request errors"""
    return error_response(400, message)


def not_found(message=None):
    """Handle 404 Not Found errors"""
    return error_response(404, message)


def internal_error(error):
    """Handle 500 Internal Server Error"""
    # In production, we might want to log the error details
    # but not expose them to the client
    return error_response(500, str(error))