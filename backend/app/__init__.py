from flask import Flask
from flask_cors import CORS
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    
    # 初始化扩展
    from extensions import db, socketio, redis_client
    from app.utils.email_service import mail
    db.init_app(app)
    socketio.init_app(app)
    redis_client.init_app(app)
    mail.init_app(app)
    
    # 注册蓝图
    from app.api.v1 import bp as api_v1_bp
    from app.api.v1 import aircraft, flights, images, atc, calendar, auth
    api_v1_bp.register_blueprint(aircraft.bp)
    api_v1_bp.register_blueprint(flights.bp)
    api_v1_bp.register_blueprint(images.bp)
    api_v1_bp.register_blueprint(atc.bp)
    api_v1_bp.register_blueprint(calendar.bp)
    api_v1_bp.register_blueprint(auth.bp)
    app.register_blueprint(api_v1_bp, url_prefix='/api/v1')
    
    # 注册错误处理器
    from app.api.errors import register_error_handlers
    register_error_handlers(app)
    
    return app