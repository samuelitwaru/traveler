from flask import request
from flask_restful import Resource, fields, marshal_with
from application.database.models import Bus, Branch, Seat, db

journey_fields = {
    "id": fields.Integer,
    "_from": fields.String,
    "to": fields.String
}

branch_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "location": fields.String,
}

payment_fields = {
    "id": fields.Integer,
    "reference": fields.String,
    "amount": fields.Integer,
    "method": fields.String,
    "time": fields.DateTime,
    "app": fields.String,
    "company_name": fields.String,
    "branch_name": fields.String,
    "bus_number": fields.String,
    "passenger_name": fields.String
}

seat_fields = {
    "id": fields.Integer,
    "number": fields.String,
    "grid_x": fields.Integer,
    "grid_y": fields.Integer,
    "booked": fields.Boolean,
    "payment": fields.Nested(payment_fields),
}

bus_fields = {
    "id": fields.Integer,
    "number": fields.String,
    "columns": fields.Integer,
    "departure_time": fields.DateTime,
    "journey": fields.Nested(journey_fields),
    "branch": fields.Nested(branch_fields),
    "seats": fields.Nested(seat_fields)
}


class BusListAPI(Resource):

    @marshal_with(bus_fields)
    def get(self):
        buses = Bus.query.all()
        return buses

    @marshal_with(bus_fields)
    def post(self):
        number = request.json["number"]
        columns = request.json["columns"]
        company_id = request.json["company_id"]
        company_ = Branch.query.get(company_id)
        bus = Bus(number, columns, company_,)

        seats = request.json["seats"]
        for seat in seats:
            Seat(seat["number"], seat["grid_x"], seat["grid_y"], bus)

        db.session.add(bus)
        db.session.commit()
        buses = Bus.query.all()
        return buses


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
        buses = Bus.query.all()
        return buses

    @marshal_with(bus_fields)
    def put(self, id):  # TODO: See how put requests are done ie, dealing with update of specific columns
        pass
