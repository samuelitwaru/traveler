import json
from flask_login import current_user
from app.utils import parse_query_string
from app.models import Grid, Booking, Pricing, db
from app.utils import create_payment, update_payment, parse_query_string, get_current_branch
from app.WEB.forms import CreatePassengerBookingForm, UpdateBookingForm, DeleteBookingForm


def connect(data):
        pass

def disconnect(data):
    print("disconnected")
    pass

def join(data):
    # add client to room
    join_room(bus_number)

def leave(data):
    # remove client from room
    leave_room(bus_number)

def create_booking(query_string):
    form_data = parse_query_string(query_string)
    grid_id = form_data.get("grid_id")
    grid = Grid.query.get(grid_id)
    bus = grid.bus
    if not bus.booking_time_expired():
        create_passenger_booking_form = CreatePassengerBookingForm(data=form_data, bus=bus)
        if create_passenger_booking_form.validate():
            # create booking
            grid_id = create_passenger_booking_form.grid_id.data;
            pricing_id = create_passenger_booking_form.pricing_id.data
            passenger_name = create_passenger_booking_form.passenger_name.data
            passenger_telephone = create_passenger_booking_form.passenger_telephone.data
            pickup = create_passenger_booking_form.pickup.data
            pricing = Pricing.query.get(pricing_id)
            branch = bus.branch
            user = current_user
            if not user.is_authenticated:
                user = None

            fare = pricing.price;
            stop = pricing.stop;
            booking = Booking(
                passenger_name=passenger_name, passenger_telephone=passenger_telephone, seat_number=grid.number, pickup=pickup, 
                fare=fare, stop=stop, grid_id=grid_id, pricing_id=pricing_id, paid=True, branch=branch, 
                bus=bus, created_by=user.id
            )

            db.session.add(booking)
            grid.booking = booking
        	
            create_payment(booking)
            db.session.commit()
            room = grid.bus.number
            return json.dumps({"handle": "create_booking_passed", "data": grid.grid_dict()})
        else:
            return json.dumps({"handle": "create_booking_failed", "data":create_passenger_booking_form.errors})
    else:
        return json.dumps({"handle":"create_booking_failed", "data":{"error": "Booking Time Ellapsed!"}})


def update_booking(query_string):
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


def delete_booking(query_string):
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



HANDLES = {
    "connect": connect,
    "disconnect": disconnect,
    "join": join,
    "leave": leave,
    "create_booking": create_booking,
    "update_booking": update_booking,
    "delete_booking": delete_booking
}