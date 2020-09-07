from flask import request
from flask_restful import Resource, fields, marshal_with
from app.models.models import Payment, Grid, Company, Branch, Bus, db

grid_field = {
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
    "grid_number": fields.String,
    "passenger_name": fields.String,
    "grid": fields.Nested(grid_field),
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
        grid_id = request.json["grid_id"]
        company_id = request.json["company_id"]
        branch_id = request.json["branch_id"]
        bus_id = request.json["bus_id"]

        grid_ = Grid.query.get(grid_id)
        company_ = Company.query.get(company_id)
        branch_ = Branch.query.get(branch_id)
        bus_ = Bus.query.get(bus_id)

        payment = Payment(amount, method, app, passenger_name, grid_, company_, branch_, bus_)
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
    def put(self, id):
        amount = request.json["amount"]
        method = request.json["method"]
        app = request.json["app"]
        passenger_name = request.json["passenger_name"]
        payment = Payment.query.get(id)
        payment.update(amount, method, app, passenger_name)
        db.session.commit()
        return payment