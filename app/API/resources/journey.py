from flask import request
from flask_restful import Resource, marshal_with
from ..fields import Fields
from app.models.models import Journey, db

journey_fields = Fields().journey_fields()

class JourneyListAPI(Resource):

    @marshal_with(journey_fields)
    def get(self):
        journeys = Journey.query.all()
        return journeys

    @marshal_with(journey_fields)
    def post(self):
        return {}


class JourneyAPI(Resource):

    @marshal_with(journey_fields)
    def get(self, id):
        journey = Journey.query.get(id)
        return journey

    @marshal_with(journey_fields)
    def delete(self, id):
        journey = Journey.query.get(id)
        db.session.delete(journey)
        db.session.commit()
        journeys = Journey.query.all()
        return journeys

    @marshal_with(journey_fields)
    def put(self, id):
        return {}