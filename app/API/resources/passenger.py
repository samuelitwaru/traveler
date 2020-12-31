# from flask import request
# from flask_restful import Resource, marshal_with
# from ..fields import Fields
# from app.models.models import Passenger, db

# passenger_fields = Fields().passenger_fields()

# class PassengerListAPI(Resource):

#     @marshal_with(passenger_fields)
#     def get(self):
#         passengers = Passenger.query.all()
#         return passengers

#     @marshal_with(passenger_fields)
#     def post(self):
#         return {}


# class PassengerAPI(Resource):

#     @marshal_with(passenger_fields)
#     def get(self, id):
#         passenger = Passenger.query.get(id)
#         return passenger

#     @marshal_with(passenger_fields)
#     def delete(self, id):
#         passenger = Passenger.query.get(id)
#         db.session.delete(passenger)
#         db.session.commit()
#         passengers = Passenger.query.all()
#         return passengers

#     @marshal_with(passenger_fields)
#     def put(self, id):
#         return {}