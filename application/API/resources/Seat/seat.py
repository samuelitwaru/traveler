from flask import request
from flask_restful import Resource, fields, marshal_with
from application.database.models import Seat, Bus, db


bus_fields = {
    "id": fields.Integer,
    "number": fields.String,
    "columns": fields.Integer,
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
    "grid": fields.Integer,
    "booked": fields.Boolean,
    "payment": fields.Nested(payment_fields),
    "bus": fields.Nested(bus_fields)
}


class SeatListAPI(Resource):

    @marshal_with(seat_fields)
    def get(self):
        seats = Seat.query.all()
        return seats

    @marshal_with(seat_fields)
    def post(self):
        number = request.json["number"]
        grid = request.json["grid"]
        bus_id = request.json["bus_id"]
        bus_ = Bus.query.get(bus_id)
        seat = Seat(number, grid, bus_)
        db.session.add(seat)
        db.session.commit()
        seats = Seat.query.all()
        return seats


class SeatAPI(Resource):

    @marshal_with(seat_fields)
    def get(self, id):
        seat = Seat.query.get(id)
        return seat

    @marshal_with(seat_fields)
    def delete(self, id):
        seat = Seat.query.get(id)
        db.session.delete(seat)
        db.session.commit()
        seats = Seat.query.all()
        return seats

    @marshal_with(seat_fields)
    def put(self, id):  # TODO: See how put requests are done ie, dealing with update of specific columns
        pass
