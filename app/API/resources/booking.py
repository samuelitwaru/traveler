from flask import request
from flask_restful import Resource, marshal_with
from ..fields import Fields
from app.models.models import Booking, db

booking_fields = Fields().booking_fields()

class BookingListAPI(Resource):

    @marshal_with(booking_fields)
    def get(self):
        bookings = Booking.query.all()
        return bookings

    @marshal_with(booking_fields)
    def post(self):
        return {}


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
    def put(self, id):
        return {}