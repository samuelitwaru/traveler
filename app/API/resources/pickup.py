from flask import request
from flask_restful import Resource, marshal_with
from ..fields import Fields
from app.models.models import Pickup, db

pickup_fields = Fields().pickup_fields()

class PickupListAPI(Resource):

    @marshal_with(pickup_fields)
    def get(self):
        pickups = Pickup.query.all()
        return pickups

    @marshal_with(pickup_fields)
    def post(self):
        return {}


class PickupAPI(Resource):

    @marshal_with(pickup_fields)
    def get(self, id):
        pickup = Pickup.query.get(id)
        return pickup

    @marshal_with(pickup_fields)
    def delete(self, id):
        pickup = Pickup.query.get(id)
        db.session.delete(pickup)
        db.session.commit()
        pickups = Pickup.query.all()
        return pickups

    @marshal_with(pickup_fields)
    def put(self, id):
        return {}