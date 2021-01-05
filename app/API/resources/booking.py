from flask import request
from flask_restful import Resource, marshal_with, reqparse
from app.models.models import Booking, Grid, Bus, db
from ..fields import Fields

booking_fields = Fields().booking_fields()

class BookingListAPI(Resource):
    get_bookings_parser = reqparse.RequestParser()

    def __init__(self):
        self.get_bookings_parser.add_argument('bus_id', type=int, help='Invalid bus_id', location="args")

    @marshal_with(booking_fields)
    def get(self):
        args = self.get_bookings_parser.parse_args()
        bus_id = args.get("bus_id")
        if bus_id:
            bus = Bus.query.get(bus_id)
            grids = [grid.id for grid in Grid.query.filter_by(bus_id=bus_id).all()]
            bookings = Booking.query.filter(Booking.grid_id.in_(grids)).all()
        else:
            bookings = Booking.query.all()
        
        return bookings

    @marshal_with(booking_fields)
    def post(self, passenger_name, passenger_telephone, pickup, fare, paid, grid_id, pricing_id):
        # create booking
        booking = Booking(passenger_name=passenger_name, passenger_telephone=passenger_telephone, fare=fare, paid=paid, grid_id=grid_id, pricing_id=pricing_id)
        db.session.add(booking)
        # get grid
        grid = Grid.query.get(grid_id)
        # update grid
        grid.booking = booking
        db.session.commit()
        # fire booked event
        return booking


class BookingAPI(Resource):

    @marshal_with(booking_fields)
    def get(self, id):
        booking = Booking.query.get(id)
        return booking

    @marshal_with(booking_fields)
    def delete(self, id):
        booking = Booking.query.get(id)
        db.session.delete(booking)
        db.session.commit()
        bookings = Booking.query.all()
        return bookings

    @marshal_with(booking_fields)
    def put(self, passenger_name, passenger_telephone, pickup, fare, paid, grid_id):

        return {}