from app import app
from app import socketio
socketio.run(app, host="0.0.0.0")
