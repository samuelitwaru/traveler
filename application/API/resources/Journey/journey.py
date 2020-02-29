from flask import request
from flask_restful import Resource, fields, marshal_with
from application.database.models import Journey, Branch, db

branch_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "location": fields.String
}

bus_fields = {
    "id": fields.Integer,
    "number": fields.String,
    "columns": fields.Integer
}

pickup_fields = {
    "id": fields.Integer,
    "name": fields.String
}

stop_fields = {
    "name": fields.String,
}

journey_fields = {
    "id": fields.Integer,
    "_from": fields.String,
    "to": fields.String,
    "branch": fields.Nested(branch_fields),
    "buses": fields.Nested(bus_fields),
    "pickups": fields.Nested(pickup_fields),
    "stops": fields.Nested(stop_fields),
}


class JourneyListAPI(Resource):

    @marshal_with(journey_fields)
    def get(self):
        journeys = Journey.query.all()
        return journeys

    @marshal_with(journey_fields)
    def post(self):
        _from = request.json["from"]
        to = request.json["to"]
        branch_id = request.json["branch_id"]
        branch_ = Branch.query.get(branch_id)
        journey = Journey(_from, to, branch_)
        db.session.add(journey)
        db.session.commit()
        journeys = Journey.query.all()
        return journeys


class JourneyAPI(Resource):

    @marshal_with(journey_fields)
    def get(self, id):
        journey = Journey.query.get(id)
        return journey

    @marshal_with(journey_fields)
    def delete(self, id):
        journey = Journey.query.get(id)
        db.session.delete(journey)
        db.session.commit()
        journeys = Journey.query.all()
        return journeys

    @marshal_with(journey_fields)
    def put(self, id):  # TODO: See how put requests are done ie, dealing with update of specific columns
        pass
