from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_redis import FlaskRedis


db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins="*")
redis_client = FlaskRedis()