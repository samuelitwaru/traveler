from flask import request
from flask_socketio import emit, send, join_room, leave_room, rooms, Namespace
from app import socketio
from app.models import db, Connection
from app.helpers import now

class DesktopNamespace(Namespace):

    def on_connect(self):
        # store client to database
        connection = Connection(sid=request.sid, client_type=self.namespace)
        db.session.add(connection)
        db.session.commit()
        pass

    def on_disconnect(self):
        # update disconnect time using the session id stored
        connection = Connection.query.filter(Connection.disconnect_time==None).filter_by(sid=request.sid).first()
        connection.disconnect_time = now()
        db.session.commit()
        print(connection)
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
