from flask import request
from flask_restful import Resource, fields, marshal_with
from application.database.models import Payment, Seat, Company, Branch, Bus, db

seat_field = {
    "id": fields.Integer,
    "number": fields.String,
    "grid": fields.Integer,
    "booked": fields.Boolean,
}

company_field = {
    "id": fields.Integer,
    "name": fields.String,
    "logo": fields.String,
}

bus_field = {
    "id": fields.Integer,
    "number": fields.String,
    "columns": fields.Integer,
}

branch_field = {
    "id": fields.Integer,
    "name": fields.String,
    "location": fields.String,
}

payment_fields = {
    "id": fields.Integer,
    "reference": fields.String,
    "amount": fields.Integer,
    "time": fields.DateTime,
    "app": fields.String,
    "company_name": fields.String,
    "branch_name": fields.String,
    "bus_number": fields.String,
    "seat_number": fields.String,
    "passenger_name": fields.String,
    "seat": fields.Nested(seat_field),
    "company": fields.Nested(company_field),
    "branch": fields.Nested(branch_field),
    "bus": fields.Nested(bus_field)
}


class PaymentListAPI(Resource):

    @marshal_with(payment_fields)
    def get(self):
        payments = Payment.query.all()
        return payments

    @marshal_with(payment_fields)
    def post(self):
        amount = request.json["amount"]
        method = request.json["method"]
        app = request.json["app"]
        passenger_name = request.json["passenger_name"]
        seat_id = request.json["seat_id"]
        company_id = request.json["company_id"]
        branch_id = request.json["branch_id"]
        bus_id = request.json["bus_id"]

        seat_ = Seat.query.get(seat_id)
        company_ = Company.query.get(company_id)
        branch_ = Branch.query.get(branch_id)
        bus_ = Bus.query.get(bus_id)

        payment = Payment(amount, method, app, passenger_name, seat_, company_, branch_, bus_)
        db.session.add(payment)
        db.session.commit()
        payments = Payment.query.all()
        return payments


class PaymentAPI(Resource):

    @marshal_with(payment_fields)
    def get(self, id):
        payment = Payment.query.get(id)
        return payment

    @marshal_with(payment_fields)
    def delete(self, id):
        payment = Payment.query.get(id)
        db.session.delete(payment)
        db.session.commit()
        payments = Payment.query.all()
        return payments

    @marshal_with(payment_fields)
    def put(self, id):  # TODO: See how put requests are done ie, dealing with update of specific columns
        pass
