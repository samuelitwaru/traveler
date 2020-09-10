import json
from datetime import timedelta
from flask import Blueprint, render_template, url_for, request, redirect, flash, session
from app.models import Bus, Company, db
from app.utils import  get_current_branch, set_bus_layout, change_bus_layout
from ..forms import CreateBusForm, UpdateBusLayoutForm, UpdateBusScheduleForm


bus_bp = Blueprint('bus', __name__, url_prefix='/bus')


@bus_bp.route("/", methods=["GET"])
def get_buses():
	company = get_current_branch().company
	buses = Bus.query.filter_by(company_id=company.id)
	return render_template("bus/buses.html", buses=buses)


@bus_bp.route("/<int:bus_id>", methods=["GET"])
def get_bus(bus_id):
	company = get_current_branch().company
	bus = Bus.query.get(bus_id)
	update_bus_schedule_form = UpdateBusScheduleForm()
	update_bus_layout_form = UpdateBusLayoutForm()
	return render_template("bus/bus.html", bus=bus, update_bus_schedule_form=update_bus_schedule_form, update_bus_layout_form=update_bus_layout_form)



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
	

@bus_bp.route("/<int:bus_id>/update/schedule", methods=["POST"])
def update_bus_schedule(bus_id):
	bus = Bus.query.get(bus_id)
	update_bus_schedule_form = UpdateBusScheduleForm()

	if update_bus_schedule_form.validate_on_submit():
		journey_id = update_bus_schedule_form.journey_id.data
		departure_time = update_bus_schedule_form.departure_time.data
		booking_deadline = departure_time + timedelta(minutes=update_bus_schedule_form.booking_deadline.data)
		broadcast = update_bus_schedule_form.broadcast.data
		UTC = update_bus_schedule_form.UTC_offset.data
		bus.journey_id = journey_id
		bus.departure_time = departure_time
		bus.booking_deadline = booking_deadline
		bus.broadcast = broadcast
		db.session.commit()
		flash("Bus scheduled.", "success")
	else:
		flash(str(update_bus_schedule_form.errors), "danger")
	return redirect(request.referrer)
	