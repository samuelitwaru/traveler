from flask import request
from flask_restful import Resource, marshal_with
from ..fields import Fields
from app.models.models import Payment, db

payment_fields = Fields().payment_fields()

class PaymentListAPI(Resource):

    @marshal_with(payment_fields)
    def get(self):
        payments = Payment.query.all()
        return payments

    @marshal_with(payment_fields)
    def post(self):
        return {}


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
        return {}