from flask import request
from flask_restful import Resource, fields, marshal_with
from application.database.models import Pickup, Journey, db

journey_fields = {
    "id": fields.Integer,
    "_from": fields.String,
    "to": fields.String
}

pickup_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "journey": fields.Nested(journey_fields)
}


class PickupListAPI(Resource):

    @marshal_with(pickup_fields)
    def get(self):
        pickups = Pickup.query.all()
        return pickups

    @marshal_with(pickup_fields)
    def post(self):
        name = request.json["name"]
        journey_id = request.json["journey_id"]
        journey_ = Journey.query.get(journey_id)
        pickup = Pickup(name, journey_)
        db.session.add(pickup)
        db.session.commit()
        pickups = Pickup.query.all()
        return pickups


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
        pickup = Pickup.query.all()
        return pickup

    @marshal_with(pickup_fields)
    def put(self, id):  # TODO: See how put requests are done ie, dealing with update of specific columns
        pass
