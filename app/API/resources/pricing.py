from flask import request
from flask_restful import Resource, marshal_with
from ..fields import Fields
from app.models.models import Pricing, db

pricing_fields = Fields().pricing_fields()

class PricingListAPI(Resource):

    @marshal_with(pricing_fields)
    def get(self):
        pricings = Pricing.query.all()
        return pricings

    @marshal_with(pricing_fields)
    def post(self):
        return {}


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
        pricings = Pricing.query.all()
        return pricings

    @marshal_with(pricing_fields)
    def put(self, id):
        return {}