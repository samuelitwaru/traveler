from flask import request
from flask_restful import Resource, marshal_with, reqparse
from ..fields import Fields
from app.models.models import Journey, db

journey_fields = Fields().journey_fields()


class JourneyListAPI(Resource):
    get_journeys_parser = reqparse.RequestParser()

    @marshal_with(journey_fields)
    def get(self):
        self.get_journeys_parser.add_argument('branch_id', type=int, help='Invalid branch_id', location="args")
        args = self.get_journeys_parser.parse_args()
        branch_id = args.get("branch_id")
        if branch_id:
            journeys = Journey.query.filter_by(branch_id=branch_id).all()
        else:
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