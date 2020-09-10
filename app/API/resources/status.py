from flask import request
from flask_restful import Resource, marshal_with
from ..fields import Fields
from app.models.models import Status, db

status_fields = Fields().status_fields()

class StatusListAPI(Resource):

    @marshal_with(status_fields)
    def get(self):
        statuss = Status.query.all()
        return statuss

    @marshal_with(status_fields)
    def post(self):
        return {}


class StatusAPI(Resource):

    @marshal_with(status_fields)
    def get(self, id):
        status = Status.query.get(id)
        return status

    @marshal_with(status_fields)
    def delete(self, id):
        status = Status.query.get(id)
        db.session.delete(status)
        db.session.commit()
        statuss = Status.query.all()
        return statuss

    @marshal_with(status_fields)
    def put(self, id):
        return {}