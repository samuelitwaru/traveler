import datetime
from flask import request
import flask_sqlalchemy
from flask_restful import Resource, marshal_with, reqparse, inputs
from ..fields import Fields
from app.models.models import Bus, Journey, db


bus_fields = Fields().bus_fields()


class BusListAPI(Resource):
    get_buses_parser = reqparse.RequestParser()
    
    def __init__(self):
        self.get_buses_parser.add_argument('departure_time', type=inputs.datetime_from_iso8601, help='Invalid depature_date', location="args")
        self.get_buses_parser.add_argument('company_id', type=int, help='Invalid company_id', location="args")
        self.get_buses_parser.add_argument('from', type=str, help='Invalid from', location="args")
        self.get_buses_parser.add_argument('to', type=str, help='Invalid to', location="args")

    @marshal_with(bus_fields)
    def get(self):
        args = self.get_buses_parser.parse_args()
        departure_time = args.get("departure_time")
        company_id = args.get("company_id")
        from_ = args.get("from")
        to = args.get("to")
        
        journeys_query = Journey.query
        if from_:
            journeys_query = journeys_query.filter(Journey.from_==from_)
        if to:
            journeys_query = journeys_query.filter(Journey.to==to)

        journeys = journeys_query.all()
        buses_query = Bus.query
        if journeys:
            buses_query = Bus.query.filter(Bus.journey_id.in_([journey.id for journey in journeys]))
        if departure_time:
            departure_time_range = datetime.timedelta(hours=2)
            departure_time_upper_limit = departure_time + departure_time_range
            departure_time_lower_limit = departure_time - departure_time_range
            buses_query = buses_query.filter(
                (Bus.departure_time > departure_time_lower_limit) & 
                (Bus.departure_time < departure_time_upper_limit)
            )
        if company_id:
            buses_query = buses_query.filter_by(company_id=company_id)

        return buses_query.all()


class BusAPI(Resource):

    @marshal_with(bus_fields)
    def get(self, id):
        bus = Bus.query.get(id)
        return bus
