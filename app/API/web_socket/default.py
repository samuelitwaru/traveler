from flask_socketio import emit, send, join_room, leave_room, rooms, Namespace
from app import socketio


class DefaultNamespace(Namespace):

    def on_connect(self):
        # store client to database
        pass

    def on_disconnect(self):
        # update disconnect time using the session id stored
        pass
