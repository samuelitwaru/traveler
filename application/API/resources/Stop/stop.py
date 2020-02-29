from flask import request
from flask_restful import Resource, fields, marshal_with
from application.database.models import Stop, db

pricing_fields = {
    "id": fields.Integer,
    "category_name": fields.String,
    "price": fields.Integer,
}

journey_fields = {
    "id": fields.Integer,
    "_from": fields.String,
    "to": fields.String,
}

stop_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "journey": fields.Nested(journey_fields),
    "pricing": fields.Nested(pricing_fields)
}


class StopListAPI(Resource):

    @marshal_with(stop_fields)
    def get(self):
        stops = Stop.query.all()
        return stops

    @marshal_with(stop_fields)
    def post(self):
        name = request.json["name"]
        stop = Stop(name)
        db.session.add(stop)
        db.session.commit()
        stops = Stop.query.all()
        return stops


class StopAPI(Resource):

    @marshal_with(stop_fields)
    def get(self, id):
        stop = Stop.query.get(id)
        return stop

    @marshal_with(stop_fields)
    def delete(self, id):
        company = stop_fields.query.get(id)
        db.session.delete(company)
        db.session.commit()
        stops = stop_fields.query.all()
        return stops

    def put(self, id):  # TODO: See how put requests are done ie, dealing with update of specific columns
        pass
