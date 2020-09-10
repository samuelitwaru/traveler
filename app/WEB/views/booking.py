import json
from flask import Blueprint, render_template, url_for, request, redirect, flash, session
from app.models import Grid, Pricing, Passenger, Booking, db
from app.utils import  get_current_branch
from ..forms import CreateBookingForm
from .payment import create_payment


booking_bp = Blueprint('booking', __name__, url_prefix='/booking')


@booking_bp.route("/", methods=["GET"])
def get_bookings():
	company = get_current_branch().company
	bookings = Booking.query.filter_by(company_id=company.id)
	return render_template("booking/bookings.html", bookings=bookings)

@booking_bp.route("/<int:bus_id>", methods=["GET"])
def get_bus_bookings(bus_id):
	grids = [grid.id for grid in Grid.query.filter_by(bus_id=bus_id).all()]
	bookings = Booking.query.filter(Grid.id.in_(grids)).all()
	bus_bookings_patch_template = render_template('booking/bookings-patch.html', bookings=bookings)
	data = {
        "form_templates": {
            "#busBookingsPatch": bus_bookings_patch_template
        }
    };return data

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
	bus = grid.bus
	if request.method == "POST":
		create_booking_form = CreateBookingForm(grid=grid)
		if create_booking_form.validate_on_submit():
			# create booking
			grid_id = create_booking_form.grid_id.data
			pricing_id = create_booking_form.pricing_id.data
			passenger_name = create_booking_form.passenger_name.data
			passenger_telephone = create_booking_form.passenger_telephone.data
			paid = create_booking_form.paid.data
			pricing = Pricing.query.get(pricing_id)
			fare = pricing.price

			booking = Booking(passenger_name=passenger_name, passenger_telephone=passenger_telephone, fare=fare, paid=paid, grid_id=grid_id, pricing_id=pricing_id)
			db.session.add(booking)
			grid.booking = booking
			create_payment(booking)
			db.session.commit()
			flash("Booking created.", "success")
		else:
			flash(str(create_booking_form.errors), "danger")
	else:
		create_booking_form = CreateBookingForm(grid=grid)
		create_booking_patch_template = render_template('booking/create-booking-patch.html', grid=grid, create_booking_form=create_booking_form)
		data = {
            "form_templates": {
                "#createBookingPatch": create_booking_patch_template
            }
        };return data
	return redirect(request.referrer)


@booking_bp.route("/<int:booking_id>/create", methods=["GET", "POST"])
def update_booking(booking_id):
	booking = Booking.query.get(grid_id)
	
	if request.method == "POST":
		update_booking_form = UpdateBookingForm(grid=grid)
		if update_booking_form.validate_on_submit():
			# update booking
			flash("Booking updated.", "success")
		else:
			flash(str(create_booking_form.errors), "danger")
	else:
		update_booking_form = UpadateBookingForm()
		update_booking_patch_template = render_template('booking/update-booking-patch.html', update_booking_form=update_booking_form)
		data = {
            "form_templates": {
                "#updateBookingPatch": update_booking_patch_template
            }
        };return data
	return redirect(request.referrer)