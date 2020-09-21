from flask import request
from flask_restful import Resource, marshal_with
from ..fields import Fields
from app.models.models import Bus, db

bus_fields = Fields().bus_fields()

class BusListAPI(Resource):

    @marshal_with(bus_fields)
    def get(self,from_place, to_place, dateTime):
        try:
            from_place = str.capitalize(from_place)
            to_place = str.capitalize(to_place)
            buses = Bus.query.filter_by(
                departure_time = datetime.datetime.strptime(
                    dateTime, 
                    '%d-%m-%Y %I:%M %p'
                )
            ).all()
            p_buses = []
            if not buses:
                buses = Bus.query.filter(
                    (
                        Bus.departure_time >= datetime.datetime.strptime(
                            dateTime, '%d-%m-%Y %I:%M %p'
                        ) - datetime.timedelta(minutes=60)
                    )&(
                        Bus.departure_time <= datetime.datetime.strptime(
                            dateTime, '%d-%m-%Y %I:%M %p'
                        ) + datetime.timedelta(minutes=60)
                    )
                ).all()
            
            if buses:
                p_buses = list(
                    filter(
                        lambda bus:bus.journey._from == from_place and bus.journey.to == to_place, 
                        buses
                    )
                )
                if not p_buses:
                    p_buses = list(
                        filter(
                            lambda bus:bus.journey._from == from_place and any(p.name == to_place for p in bus.journey.pickups), 
                            buses
                        )
                    )
                    
            return p_buses
        except:
            #abort
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
