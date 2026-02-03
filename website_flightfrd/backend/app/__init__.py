from flask import Flask
from flask_cors import CORS
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 初始化扩展
    from extensions import db, socketio, redis_client
    db.init_app(app)
    socketio.init_app(app)
    redis_client.init_app(app)
    
    # 注册蓝图
    from api.v1 import bp as api_v1_bp
    app.register_blueprint(api_v1_bp, url_prefix='/api/v1')
    
    # 注册错误处理器
    from api.errors import register_error_handlers
    register_error_handlers(app)
    
    return app