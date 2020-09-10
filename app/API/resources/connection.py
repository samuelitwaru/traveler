from flask import request
from flask_restful import Resource, marshal_with
from ..fields import Fields
from app.models.models import Connection, db

connection_fields = Fields().connection_fields()

class ConnectionListAPI(Resource):

    @marshal_with(connection_fields)
    def get(self):
        connections = Connection.query.all()
        return connections

    @marshal_with(connection_fields)
    def post(self):
        return {}


class ConnectionAPI(Resource):

    @marshal_with(connection_fields)
    def get(self, id):
        connection = Connection.query.get(id)
        return connection

    @marshal_with(connection_fields)
    def delete(self, id):
        connection = Connection.query.get(id)
        db.session.delete(connection)
        db.session.commit()
        connections = Connection.query.all()
        return connections

    @marshal_with(connection_fields)
    def put(self, id):
        return {}