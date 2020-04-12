from flask import request
from flask_restful import Resource, fields, marshal_with
from application.database.models import Passenger, Bus, db

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

passenger_fields = {
    "first_name": fields.String,
    "last_name": fields.String,
    "email": fields.String,
    "telephone": fields.String,
    "payments": fields.Nested(payment_fields)
}


class PassengerListAPI(Resource):

    @marshal_with(passenger_fields)
    def get(self):
        passengers = Passenger.query.all()
        return passengers

    @marshal_with(passenger_fields)
    def post(self):
        first_name = request.json.get("first_name")
        last_name = request.json.get("last_name")
        email = request.json.get("email")
        telephone = request.get("telephone")
        password = request.json.get("password")
        passenger = Passenger(first_name, last_name, email, telephone, password)
        db.session.add(passenger)
        db.session.commit()
        passengers = Passenger.query.all()
        return passengers


class PassengerAPI(Resource):

    @marshal_with(passenger_fields)
    def get(self, id):
        passenger = Passenger.query.get(id)
        return passenger

    @marshal_with(passenger_fields)
    def delete(self, id):
        passenger = Passenger.query.get(id)
        db.session.delete(passenger)
        db.session.commit()
        passengers = Passenger.query.all()
        return passengers

    @marshal_with(passenger_fields)
    def put(self, id):
        first_name = request.json.get("first_name")
        last_name = request.json.get("last_name")
        email = request.json.get("email")
        telephone = request.get("telephone")
        passenger = Passenger.query.get(id)
        passenger.update(first_name, last_name, email, telephone)
        db.session.commit()
        return passenger
