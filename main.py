from application import app
from application import socketio
# app.run()
socketio.run(app, host="0.0.0.0")
