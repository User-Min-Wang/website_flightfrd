from app import create_app
from extensions import socketio
import os


app = create_app()


@app.shell_context_processor
def make_shell_context():
    from extensions import db
    from app.models import Aircraft, Flight, Image, ATCMessage, User
    return {
        'db': db,
        'Aircraft': Aircraft,
        'Flight': Flight,
        'Image': Image,
        'ATCMessage': ATCMessage,
        'User': User
    }


if __name__ == '__main__':
    # Get host and port from environment variables or use defaults
    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Run the application with SocketIO support
    socketio.run(app, host=host, port=port, debug=debug, use_reloader=False)