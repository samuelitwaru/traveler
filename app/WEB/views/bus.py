import json
from datetime import timedelta
from flask import Blueprint, render_template, url_for, request, redirect, flash, session
from flask_login import current_user
from app.models import Bus, Company, Grid, Booking, db
from app.utils import  get_current_branch, set_bus_layout, change_bus_layout, find_buses, set_bus_free
from app import app
from ..forms import CreateBusForm, UpdateBusLayoutForm, UpdateBusScheduleForm, DeleteBusScheduleForm, SearchBusesForm, DeleteBusForm, CreatePassengerBookingForm
from .. guards import check_branch_journeys
from ..data import BusSchedule, CreatePassengerBookingFormData


bus_bp = Blueprint('bus', __name__, url_prefix='/bus')


@bus_bp.route("/search", methods=["GET"])
def search_buses():
	search_buses_form = SearchBusesForm(request.args)
	from_ = None
	to = None
	departure_time = None
	if search_buses_form.validate():
		data = search_buses_form.data
		from_ = data.get("from_")
		to = data.get("to")
		departure_time = data.get("departure_time")
		
	buses = find_buses(from_=from_, to=to, departure_time=departure_time)
	# change departure time format to that compatible with form widget
	if departure_time:
		search_buses_form.departure_time.data = departure_time.strftime(app.config.get("TIME_FORMAT"))
	template = "index/search-buses-results.html"
	if current_user.is_authenticated:
		template = "bus/passenger-buses.html"
	return render_template(template, buses=buses, search_buses_form=search_buses_form)


@bus_bp.route("/", methods=["GET"])
@check_branch_journeys
def get_buses():
	branch = get_current_branch()
	company = branch.company
	free_buses = Bus.query.filter_by(company_id=company.id, branch_id=None)
	scheduled_buses = Bus.query.filter_by(branch_id=branch.id)
	return render_template("bus/buses.html", free_buses=free_buses, scheduled_buses=scheduled_buses)


@bus_bp.route("/<int:bus_id>", methods=["GET"])
def get_bus(bus_id):
	bus = Bus.query.get(bus_id)
	create_passenger_booking_form = CreatePassengerBookingForm(bus=bus)
	return render_template("bus/bus.html", bus=bus, create_passenger_booking_form=create_passenger_booking_form)


@bus_bp.route("/<int:bus_id>/passenger", methods=["GET"])
def get_passenger_bus(bus_id):
	bus = Bus.query.get(bus_id)
	create_passenger_booking_form_data = None
	if current_user.is_authenticated:
		passenger = current_user.profile
		create_passenger_booking_form_data = CreatePassengerBookingFormData(passenger)
	
	create_passenger_booking_form = CreatePassengerBookingForm(obj=create_passenger_booking_form_data, bus=bus)
	return render_template("bus/passenger-bus.html", bus=bus, create_passenger_booking_form=create_passenger_booking_form)


@bus_bp.route("/create/<int:company_id>", methods=["POST"])
def create_bus(company_id):
	company = Company.query.get(company_id)
	create_bus_form = CreateBusForm(company=company)
	if create_bus_form.validate_on_submit():
		# create bus
		number = create_bus_form.number.data
		status_id = create_bus_form.status_id.data
		columns = create_bus_form.columns.data
		rows = create_bus_form.rows.data
		bus = Bus(number=number, columns=columns, rows=rows, status_id=status_id, company=company)
		set_bus_layout(bus, columns, rows)
		db.session.commit()
		flash("Bus created.", "success")
		return redirect(url_for('company.get_company_bus', company_id=company.id, bus_id=bus.id))
	flash(str(create_bus_form.errors), "danger")
	return redirect(url_for('company.get_company_buses', company_id=company.id))


@bus_bp.route("/<int:bus_id>/update/layout", methods=["POST"])
def update_bus_layout(bus_id):
	bus = Bus.query.get(bus_id)
	update_bus_layout_form = UpdateBusLayoutForm()
	if update_bus_layout_form.validate_on_submit():
		rows = update_bus_layout_form.rows.data
		columns = update_bus_layout_form.columns.data
		layout = update_bus_layout_form.layout.data
		bus.columns = columns
		bus.rows = rows
		change_bus_layout(bus, json.loads(layout))
		db.session.commit()
		flash("Bus layout updated.", "success")
	else:
		flash(str(update_bus_layout_form.errors), "danger")
	return redirect(request.referrer)


@bus_bp.route("/<int:bus_id>/delete", methods=["POST"])
def delete_bus(bus_id):
	bus = Bus.query.get(bus_id)
	company = bus.company
	delete_bus_form = DeleteBusForm()
	if delete_bus_form.validate():
		db.session.delete(bus)
		db.session.commit()
		flash("Bus deleted.", "success")
		return redirect(url_for('company.get_company_buses', company_id=company.id))
	flash(f"{delete_bus_form.errors}", "danger")
	print(delete_bus_form.errors)
	return redirect(request.referrer)

	

@bus_bp.route("/<int:bus_id>/schedule/update", methods=["POST"])
def update_bus_schedule(bus_id):
	bus = Bus.query.get(bus_id)
	update_bus_schedule_form = UpdateBusScheduleForm()

	if update_bus_schedule_form.validate_on_submit():
		journey_id = update_bus_schedule_form.journey_id.data
		departure_time = update_bus_schedule_form.departure_time.data
		booking_deadline = departure_time - timedelta(minutes=update_bus_schedule_form.booking_deadline.data)
		free_bus_time = departure_time + timedelta(minutes=update_bus_schedule_form.free_bus_time.data)
		broadcast = update_bus_schedule_form.broadcast.data
		UTC = update_bus_schedule_form.UTC_offset.data
		bus.journey_id = journey_id
		bus.departure_time = departure_time
		bus.booking_deadline = booking_deadline
		bus.free_bus_time = free_bus_time
		bus.broadcast = broadcast
		bus.branch = get_current_branch()
		db.session.commit()
		flash("Bus scheduled.", "success")
	else:
		flash(str(update_bus_schedule_form.errors), "danger")
	return redirect(request.referrer)
	

@bus_bp.route("/<int:bus_id>/schedule/delete", methods=["POST", "GET"])
def delete_bus_schedule(bus_id):
	bus = Bus.query.get(bus_id)
	delete_bus_schedule_form = DeleteBusScheduleForm(obj=bus)
	if request.method == "POST":
		if delete_bus_schedule_form.validate_on_submit():
			schedule_cancelled_reason = delete_bus_schedule_form.data.get("schedule_cancelled_reason")
			delete_bookings = delete_bus_schedule_form.data.get("delete_bookings")
			bus.journey_id = None
			bus.departure_time = None
			bus.booking_deadline = None
			bus.free_bus_time = None
			bus.broadcast = None
			bus.branch = None
			bus.schedule_cancelled_reason = schedule_cancelled_reason

			if delete_bookings:
				# delete all bus bookings
				grids = [grid.id for grid in Grid.query.filter_by(bus_id=bus_id).all()]
				bookings = Booking.query.filter(Booking.grid_id.in_(grids)).delete(synchronize_session=False)
			
			db.session.commit()
			flash("Schedule cancelled.", "success")
		else:
			flash(str(delete_bus_schedule_form.errors), "danger")
		return redirect(request.referrer)
	else:
		delete_bus_schedule_patch_template = render_template('bus/delete-bus-schedule-patch.html', delete_bus_schedule_form=delete_bus_schedule_form, bus=bus)
		
		data = {
            "form_templates": {
                "#deleteBusSchedulePatch": delete_bus_schedule_patch_template
            }
        };return data
	

@bus_bp.route("/<int:bus_id>/free", methods=["GET"])
def free_bus(bus_id):
	bus = Bus.query.filter_by(id=bus_id).first()
	if bus:
		set_bus_free(bus)
		db.session.commit()
		flash("Bus freed.", "success")
	else:
		flash("Bus not found.", "danger")
	return redirect(request.referrer)


