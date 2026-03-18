from flask import Blueprint


def create_api_blueprint():
    """Create and configure the API blueprint"""
    bp = Blueprint('api', __name__, url_prefix='/api')
    
    # Import and register API routes
    from app.api.v1 import bp as api_v1_bp
    bp.register_blueprint(api_v1_bp, url_prefix='/v1')
    
    return bp