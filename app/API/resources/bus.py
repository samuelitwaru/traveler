from flask import request
import flask_sqlalchemy
from flask_restful import Resource, marshal_with, reqparse, inputs
from app.utils import find_buses
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

        buses = find_buses(from_=from_, to=to, departure_time=departure_time, company_id=company_id)
        return buses

class BusAPI(Resource):

    @marshal_with(bus_fields)
    def get(self, id):
        bus = Bus.query.get(id)
        return bus
