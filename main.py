from app import app
from app import socketio
#app.run()
#socketio.run(app, host="10.42.0.1")
HOST = "192.168.1.117"
HOST = "traveler-ug.herokuapp.com"
socketio.run(app)
