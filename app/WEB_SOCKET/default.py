import json
from flask import request
from flask_socketio import emit, send, join_room, leave_room, rooms, Namespace
from app import socketio
from app.models import Booking, Grid, Pricing, Connection, db
from app.helpers import now
from app.utils import create_payment, update_payment, parse_query_string
from app.WEB.forms import CreateBookingForm, UpdateBookingForm, DeleteBookingForm


class DefaultNamespace(Namespace):

    def on_connect(self):
        pass

    def on_disconnect(self):
        print("disconnected")
        pass

    def on_join(self, bus_number):
        # add client to room
        join_room(bus_number)

    def on_leave(self, bus_id):
        # remove client from room
        leave_room(bus_number)

    def on_create_booking(self, query_string):
        form_data = parse_query_string(query_string)
        grid_id = form_data.get("grid_id")
        grid = Grid.query.get(grid_id)
        bus = grid.bus
        if not bus.booking_time_expired():
            create_booking_form = CreateBookingForm(data=form_data, grid=grid)
            if create_booking_form.validate():
            	# create booking
            	grid_id = create_booking_form.grid_id.data; print(create_booking_form.data)
            	pricing_id = create_booking_form.pricing_id.data
            	passenger_name = create_booking_form.passenger_name.data
            	passenger_telephone = create_booking_form.passenger_telephone.data
            	pickup = create_booking_form.pickup.data
            	paid = create_booking_form.paid.data
            	pricing = Pricing.query.get(pricing_id)
            	fare = pricing.price

            	booking = Booking(passenger_name=passenger_name, passenger_telephone=passenger_telephone, pickup=pickup, fare=fare, paid=paid, grid_id=grid_id, pricing_id=pricing_id)
            	db.session.add(booking)
            	grid.booking = booking
            	create_payment(booking)
            	
            	db.session.commit()
            	room = grid.bus.number
            	emit("create_booking_passed", grid.grid_dict(), room=room, broadcast=True)
            else:
                emit("create_booking_failed", create_booking_form.errors, broadcast=False)
        else:
            emit("create_booking_failed", {"error": "Booking Time Ellapsed!"}, broadcast=False)


    def on_update_booking(self, query_string):
        form_data = parse_query_string(query_string)
        grid_id = form_data.get("grid_id")
        grid = Grid.query.get(grid_id)
        update_booking_form = UpdateBookingForm(data=form_data, grid=grid)
        booking = Booking.query.get(form_data["id"])
        if update_booking_form.validate():
            # update booking
            booking.pricing_id = update_booking_form.pricing_id.data
            booking.passenger_name = update_booking_form.passenger_name.data
            booking.passenger_telephone = update_booking_form.passenger_telephone.data
            booking.pickup = update_booking_form.pickup.data
            booking.paid = update_booking_form.paid.data
            pricing = Pricing.query.get(booking.pricing_id)
            booking.fare = pricing.price

            update_payment(booking)
            
            db.session.commit()
            room = grid.bus.number
            emit("update_booking_passed", grid.grid_dict(), room=room, broadcast=True)
        
        else:
            emit("update_booking_failed", update_booking_form.errors, broadcast=False)


    def on_delete_booking(self, query_string):
        form_data = parse_query_string(query_string)
        delete_booking_form = DeleteBookingForm(data=form_data)
        booking = Booking.query.get(form_data["id"])
        grid = booking.booked_grid
        if delete_booking_form.validate():
            # delete booking
            db.session.delete(booking)
            db.session.commit()
            room = grid.bus.number
            emit("delete_booking_passed", grid.grid_dict(), room=room, broadcast=True)
        else:
            emit("delete_booking_failed", delete_booking_form.errors, broadcast=False)