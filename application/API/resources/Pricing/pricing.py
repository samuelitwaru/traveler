from flask import request
from flask_restful import Resource, fields, marshal_with
from application.database.models import Pricing, Journey, db

journey_fields = {
    "id": fields.Integer,
    "_from": fields.String,
    "to": fields.String
}

pricing_fields = {
    "id": fields.Integer,
    "category_name": fields.String,
    "price": fields.Integer,
    "journey": fields.Nested(journey_fields)
}


class PricingListAPI(Resource):

    @marshal_with(pricing_fields)
    def get(self):
        pricing = Pricing.query.all()
        return pricing

    @marshal_with(pricing_fields)
    def post(self):
        category_name = request.json["category_name"]
        price = request.json["price"]
        journey_id = request.json["journey_id"]
        journey_ = Journey.query.get(journey_id)
        pricing = Pricing(category_name, price, journey_)
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
