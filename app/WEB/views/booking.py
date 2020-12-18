import json
from weasyprint import HTML, CSS
from flask import Blueprint, render_template, url_for, request, redirect, flash, session, make_response
from flask_login import current_user
import flask_sqlalchemy
from app.models import Grid, Pricing, Passenger, Booking, Bus, db
from app.utils import  get_current_branch
from ..forms import CreateBookingForm, UpdateBookingForm, DeleteBookingForm, FilterBookingsForm, SearchBusesForm, CreatePassengerBookingForm
from ..data import CreatePassengerBookingFormData
from .payment import create_payment


booking_bp = Blueprint('booking', __name__, url_prefix='/booking')


@booking_bp.route("/", methods=["GET"])
def get_company_bookings():
	company = get_current_branch().company
	
	buses_query = Bus.query.filter_by(company_id=company.id)
	
	bus_id_choices = [(bus.id, bus) for bus in buses_query.all()]
	
	filter_bookings_form = FilterBookingsForm(formdata=request.args, bus_id_choices=bus_id_choices)
	
	bookings_query = Booking.query
	
	bus_id = None
	created_on_gte = None
	created_on_lte = None

	if request.args:
		if filter_bookings_form.validate():
			data = filter_bookings_form.data
			created_on_gte = filter_bookings_form.created_on_gte.data
			created_on_lte = filter_bookings_form.created_on_lte.data
			bus_id = filter_bookings_form.bus_id.data
			if bus_id:
				bookings_query = bookings_query.filter_by(bus_id=bus_id)

	if created_on_gte:
		bookings_query = bookings_query.filter(Booking.created_at>=created_on_gte)
	if created_on_lte:
		bookings_query = bookings_query.filter(Booking.created_at<=created_on_lte)

	bookings = bookings_query.all()

	filter_bookings_form.created_on_gte.data = request.args.get("created_on_gte")
	filter_bookings_form.created_on_lte.data = request.args.get("created_on_lte")
	
	return render_template("booking/booking-history.html", bookings=bookings, filter_bookings_form=filter_bookings_form)


@booking_bp.route("/<int:bus_id>", methods=["GET"])
def get_bus_bookings(bus_id):
	bus = Bus.query.get(bus_id)
	grids = [grid for grid in Grid.query.filter_by(bus_id=bus_id).filter(Grid.booking_id!=None).all()]
	bookings  = [grid.booking for grid in grids]
	total_fare = sum([booking.fare for booking in bookings])
	total_paid = sum([booking.fare for booking in list(filter(lambda booking: booking.paid, bookings))])
	bus_bookings_patch_template = render_template('booking/bookings-patch.html', bookings=bookings, bus=bus, total_fare=total_fare, total_paid=total_paid)
	data = {
        "form_templates": {
            "#busBookingsPatch": bus_bookings_patch_template
        }
    };return data


@booking_bp.route("/passenger", methods=["GET"])
def get_passenger_bookings():
	passenger = current_user
	bookings = Booking.query.filter_by(created_by=passenger.id).all()
	search_buses_form = SearchBusesForm()

	return render_template('booking/passenger-bookings.html', search_buses_form=search_buses_form, bookings=bookings)


@booking_bp.route("/<int:booking_id>", methods=["GET"])
def get_booking(booking_id):
	company = get_current_branch().company
	booking = Booking.query.get(booking_id)
	update_booking_schedule_form = UpdateBookingScheduleForm()
	update_booking_layout_form = UpdateBookingLayoutForm()
	return render_template("booking/booking.html", booking=booking, update_booking_schedule_form=update_booking_schedule_form, update_booking_layout_form=update_booking_layout_form)


#@only_bookable_grid
@booking_bp.route("/create/<int:grid_id>", methods=["GET", "POST"])
def create_booking(grid_id):
	grid = Grid.query.get(grid_id)
	if request.method == "POST":
		create_booking_form = CreateBookingForm(grid=grid)
		if create_booking_form.validate_on_submit():
			# create booking
			grid_id = create_booking_form.grid_id.data
			pricing_id = create_booking_form.pricing_id.data
			passenger_name = create_booking_form.passenger_name.data
			passenger_telephone = create_booking_form.passenger_telephone.data
			pickup = create_booking_form.pickup.data
			paid = create_booking_form.paid.data
			pricing = Pricing.query.get(pricing_id)
			fare = pricing.price
			stop = pricing.stop

			booking = Booking(passenger_name=passenger_name, passenger_telephone=passenger_telephone, pickup=pickup, stop=stop, fare=fare, paid=paid, grid_id=grid_id, pricing_id=pricing_id)
			db.session.add(booking)
			grid.booking = booking
			create_payment(booking)
			db.session.commit()
			flash("Booking created.", "success")
		else:
			flash(str(create_booking_form.errors), "danger")
		
		return redirect(request.referrer)

	else:
		bus = grid.bus
		if bus.journey:
			create_booking_form = CreateBookingForm(grid=grid)
			create_booking_patch_template = render_template('booking/create-booking-patch.html', grid=grid, create_booking_form=create_booking_form, bus=bus)
		else:
			create_booking_patch_template = render_template('booking/create-booking-patch.html', bus=bus)

		data = {
	        "form_templates": {
	            "#createBookingPatch": create_booking_patch_template
	        }
	    };return data


@booking_bp.route("/create/<int:grid_id>/passenger", methods=["GET", "POST"])
def create_passenger_booking(grid_id):
	grid = Grid.query.get(grid_id)
	bus = grid.bus
	create_passenger_booking_form_data = None
	if current_user.is_authenticated:
		passenger = current_user.profile
		create_passenger_booking_form_data = CreatePassengerBookingFormData(passenger)
	
	create_passenger_booking_form = CreatePassengerBookingForm(obj=create_passenger_booking_form_data, grid=grid)
	create_passenger_booking_patch_template = render_template('booking/create-passenger-booking-form.html', grid=grid, create_passenger_booking_form=create_passenger_booking_form, bus=bus)
	
	data = {
        "form_templates": {
            "#createPassengerBookingPatch": create_passenger_booking_patch_template
        }
    };return data


@booking_bp.route("/<int:booking_id>/update", methods=["GET", "POST"])
def update_booking(booking_id):
	booking = Booking.query.get(booking_id)
	grid = booking.booked_grid
	if request.method == "POST":
		update_booking_form = UpdateBookingForm(grid=grid)
		if update_booking_form.validate_on_submit():
			# update booking
			flash("Booking updated.", "success")
		else:
			flash(str(update_booking_form.errors), "danger")
		return redirect(request.referrer)
	else:
		bus = grid.bus
		if bus.journey:
			update_booking_form = UpdateBookingForm(obj=booking, grid=grid)
			update_booking_patch_template = render_template('booking/update-booking-patch.html', update_booking_form=update_booking_form, booking=booking, grid=grid, bus=bus)
		else:
			update_booking_patch_template = render_template('booking/update-booking-patch.html', bus=bus)

		data = {
            "form_templates": {
                "#updateBookingPatch": update_booking_patch_template
            }
        };return data


@booking_bp.route("/<int:booking_id>/delete", methods=["GET", "POST"])
def delete_booking(booking_id):
	booking = Booking.query.get(booking_id)
	grid = booking.booked_grid
	if request.method == "POST":
		delete_booking_form = DeleteBookingForm(grid=grid)
		if delete_booking_form.validate_on_submit():
			# delete booking
			flash("Booking deleted.", "success")
		else:
			flash(str(delete_booking_form.errors), "danger")
		
		return redirect(request.referrer)

	else:
		delete_booking_form = DeleteBookingForm(obj=booking, grid=grid)
		delete_booking_patch_template = render_template('booking/delete-booking-patch.html', delete_booking_form=delete_booking_form, booking=booking, grid=grid)
		data = {
            "form_templates": {
                "#deleteBookingPatch": delete_booking_patch_template
            }
        };return data


@booking_bp.route('<int:bus_id>/print', methods=["GET"])
def print_bookings(bus_id):
	bus = Bus.query.get(bus_id)
	grids = [grid.id for grid in Grid.query.filter_by(bus_id=bus_id).all()]
	bookings = Booking.query.filter(Booking.grid_id.in_(grids)).all()
	total_fare = sum([booking.fare for booking in bookings])
	total_paid = sum([booking.fare for booking in list(filter(lambda booking: booking.paid, bookings))])
	bus_bookings_patch_template = render_template('prints/bookings.html', bookings=bookings, total_fare=total_fare, total_paid=total_paid, bus=bus)

	pdf_file = HTML(string=bus_bookings_patch_template).write_pdf()

	response = make_response(pdf_file)
	response.headers.set('Content-Disposition', 'attachment', filename='booking.pdf')
	response.headers.set('Content-Type', 'application/pdf')
	return response