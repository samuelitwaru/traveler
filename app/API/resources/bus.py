from flask import request
from flask_restful import Resource, marshal_with
from ..fields import Fields
from app.models.models import Bus, db

bus_fields = Fields().bus_fields()

class BusListAPI(Resource):

    @marshal_with(bus_fields)
    def get(self):
        buss = Bus.query.all()
        return buss

    @marshal_with(bus_fields)
    def post(self):
        return {}


class BusAPI(Resource):

    @marshal_with(bus_fields)
    def get(self, id):
        bus = Bus.query.get(id)
        return bus

    @marshal_with(bus_fields)
    def delete(self, id):
        bus = Bus.query.get(id)
        db.session.delete(bus)
        db.session.commit()
        buss = Bus.query.all()
        return buss

    @marshal_with(bus_fields)
    def put(self, id):
        return {}