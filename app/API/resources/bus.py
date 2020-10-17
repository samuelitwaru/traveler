import datetime
from flask import request
from flask_restful import Resource, marshal_with, reqparse, inputs
from ..fields import Fields
from app.models.models import Bus, db
from ..parser import get_buses_parser

bus_fields = Fields().bus_fields()


class BusListAPI(Resource):

    def __init__(self):
        self.get_buses_parser = reqparse.RequestParser()
        self.get_buses_parser.add_argument('departure_time', type=inputs.datetime_from_iso8601, help='Invalid depature_date', location="args")
        self.get_buses_parser.add_argument('company_id', type=int, help='Invalid company_id', location="args")
        self.get_buses_parser.add_argument('from', type=str, help='Invalid from', location="args")
        self.get_buses_parser.add_argument('to', type=str, help='Invalid to', location="args")

    @marshal_with(bus_fields)
    def get(self):
        args = get_buses_parser.parse_args()
        print(args)
        departure_time = args.get("departure_time")
        company_id = args.get("company_id")
        from_ = args.get("from")
        to = args.get("to")
        buses = Bus.query.all()
        try:
            buses = Bus.query.filter_by(
                departure_time = departure_time
            ).all()

            p_buses = []
            if not buses:
                buses = Bus.query.filter(
                    (
                        Bus.departure_time >= departure_time - datetime.timedelta(days=1)
                    )&(
                        Bus.departure_time <= departure_time + datetime.timedelta(days=1)
                    )
                ).all()
            
            if buses:
                p_buses = list(
                    filter(
                        lambda bus:bus.journey.from_ == from_ and bus.journey.to == to, 
                        buses
                    )
                )
                if not p_buses:
                    p_buses = list(
                        filter(
                            lambda bus:bus.journey.from_ == from_ and any(p.name == to for p in bus.journey.pickups), 
                            buses
                        )
                    )
                    
            return p_buses
        except Exception as e:
            print(e)
            return []

##    @marshal_with(bus_fields)
##    def get(self):
##        buss = Bus.query.all()
##        return buss

    @marshal_with(bus_fields)
    def post(self):
        return {}


class BusAPI(Resource):

    @marshal_with(bus_fields)
    def get(self, id):
        bus = Bus.query.get(id)
        return bus

    @marshal_with(bus_fields)
    def delete(self, id):
        bus = Bus.query.get(id)
        db.session.delete(bus)
        db.session.commit()
        buss = Bus.query.all()
        return buss

    @marshal_with(bus_fields)
    def put(self, id):
        return {}
