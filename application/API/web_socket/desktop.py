from flask_socketio import emit, send, join_room, leave_room, rooms, Namespace
from application import socketio


class DesktopNamespace(Namespace):

    def on_connect(self):
        # store client to database
        pass

    def on_disconnect(self):
        # update disconnect time using the session id stored
        pass

    # rooms in mobile: [{bus_numbers}]
    def on_join(self, data):
        # add client to room
        pass

    # rooms in mobile: [{bus_numbers}]
    def on_leave(self, data):
        # remove client from room
        pass

    def on_book(self, data):
        # update bus seat column 'booked' to True
        # emit 'seat booked' event to bus room in global name space
        pass

    def on_unbook(self, data):
        # update bus seat column booked to False
        # emit 'seat unbooked' to bus room in global name space
        pass


socketio.on_namespace(DesktopNamespace('/desktop'))
