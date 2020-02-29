from flask import request
from flask_restful import Resource, fields, marshal_with
from application.database.models import Pricing, Stop, Status, db

status_fields = {
    "id": fields.Integer,
    "name": fields.String,
}

stop_fields = {
    "id": fields.Integer,
    "name": fields.String,
}

pricing_fields = {
    "id": fields.Integer,
    "price": fields.String,
    "status": fields.Integer,
    "journey": fields.Nested(status_fields),
    "stop": fields.Nested(stop_fields)
}


class PricingListAPI(Resource):

    @marshal_with(pricing_fields)
    def get(self):
        pricing = Pricing.query.all()
        return pricing

    @marshal_with(pricing_fields)
    def post(self):
        price = request.json["price"]
        stop_id = request.json["stop_id"]
        status_id = request.json["status_id"]
        status_ = Status.query.get(status_id)
        stop_ = Stop.query.get(stop_id)
        pricing = Pricing(price, stop_, status_)
        db.session.add(pricing)
        db.session.commit()
        pricing = Pricing.query.all()
        return pricing


class PricingAPI(Resource):

    @marshal_with(pricing_fields)
    def get(self, id):
        pricing = Pricing.query.get(id)
        return pricing

    @marshal_with(pricing_fields)
    def delete(self, id):
        pricing = Pricing.query.get(id)
        db.session.delete(pricing)
        db.session.commit()
        pricing = Pricing.query.all()
        return pricing

    @marshal_with(pricing_fields)
    def put(self, id):  # TODO: See how put requests are done ie, dealing with update of specific columns
        pass
