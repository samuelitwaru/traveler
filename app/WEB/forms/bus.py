from datetime import datetime
import json
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from wtforms.widgets import HiddenInput, Select, TextArea
from app import app
from app.utils import get_current_branch
from app.helpers import timezone, now
from app.models import Journey, Status, Bus


columns_choices = [(i,i) for i in range(3,8)]
rows_choices = [(i,i) for i in range(5,16)]
booking_deadline_choices = [
	(30,"30 Minutes before departure"), (60,"1 Hour before departure"), 
	(120,"2 Hours before departure"), (180,"3 Hours before departure")
]

free_bus_time_choices = [
	(30,"30 Minutes after departure"), (60,"1 Hour after departure"), 
	(120,"2 Hours after departure"), (180,"3 Hours after departure")
]


def unique_create_number(form, field):
    if Bus.query.filter_by(number=field.data).first():
        raise ValidationError(f"Bus with number '{field.data}' already exists.")

def unique_update_number(form, field):
    if Bus.query.filter(Bus.id!=form.id.data).filter_by(number=field.data).first():
        raise ValidationError(f"Bus with number '{field.data}' already exists.")


class SearchBusesForm(FlaskForm):
	UTC_offset = StringField(widget=HiddenInput())
	from_ = StringField("Departing From?", validators=[])
	to = StringField("Going To?", validators=[])
	departure_time = StringField("When?", validators=[])
	submit = SubmitField('Find Bus')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.datetime_format = app.config.get("TIME_FORMAT")

	def validate_departure_time(form, field):
		departure_time = field.data
		if departure_time:
			UTC_offset = form.UTC_offset.data
			departure_time = datetime.strptime(f"{departure_time} {UTC_offset}", form.datetime_format)
			departure_time_as_tz = departure_time.astimezone(timezone)
			if departure_time_as_tz < now():
				raise ValidationError(f"The departure time {field.data} has already passed.")
			form.departure_time.data = departure_time_as_tz


class CreateBusForm(FlaskForm):
    number = StringField("Bus number", validators=[DataRequired(), unique_create_number])
    status_id = SelectField("Bus status", validators=[DataRequired()], coerce=int)
    columns = SelectField("Seat columns", validators=[DataRequired()], coerce=int)
    rows = SelectField("Seat rows", validators=[DataRequired()], coerce=int)
    submit = SubmitField('Save')

    def __init__(self, company, *args, **kwargs):
    	super().__init__(*args, **kwargs)
    	self.company=company
    	self.columns.choices = columns_choices
    	self.rows.choices = rows_choices
    	self.status_id.choices = [(status.id, status) for status in Status.query.filter_by(company_id=self.company.id)]


class DeleteBusForm(FlaskForm):
    id = IntegerField(validators=[DataRequired()], widget=HiddenInput())
    submit = SubmitField('Delete')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UpdateBusLayoutForm(FlaskForm):
	layout = StringField(validators=[DataRequired()], widget=HiddenInput())
	columns = SelectField("Columns", validators=[DataRequired()], coerce=int)
	rows = SelectField("Rows", validators=[DataRequired()], coerce=int)
	submit = SubmitField('Save')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.columns.choices = columns_choices
		self.rows.choices = rows_choices  

	def validate_layout(form, field):
		layout = field.data
		columns = form.columns.data
		rows = form.rows.data
		try:
			layout_list = json.loads(layout)
			if not isinstance(layout_list, list) or (columns*rows) != len(layout_list):
				raise ValidationError(f"Data submitted does not match the one required")
		except Exception as e:
			raise ValidationError(f"{e}")


class UpdateBusScheduleForm(FlaskForm):
	UTC_offset = StringField(widget=HiddenInput())
	departure_time = StringField("Departure Time", validators=[DataRequired()])
	booking_deadline = RadioField("Booking deadline", validators=[DataRequired()], coerce=int)
	free_bus_time = RadioField("Free bus", validators=[DataRequired()], coerce=int)
	journey_id = SelectField("Journey", validators=[DataRequired()], coerce=int)
	broadcast = BooleanField("Broadcast")
	submit = SubmitField('Save')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.datetime_format = app.config.get("TIME_FORMAT")
		self.booking_deadline.choices = booking_deadline_choices
		self.free_bus_time.choices = free_bus_time_choices
		branch = get_current_branch()
		self.journey_id.choices = [
				(journey.id, journey) for journey in 
				list(filter(
					lambda journey: len(journey.pricings) and len(journey.pickups), 
					Journey.query.filter_by(branch_id=branch.id)
					)
				)
			]

	def validate_UTC_offset(form, field):
		pass

	def validate_departure_time(form, field):
		departure_time = field.data
		UTC_offset = form.UTC_offset.data
		departure_time = datetime.strptime(f"{departure_time} {UTC_offset}", form.datetime_format)
		departure_time_as_tz = departure_time.astimezone(timezone)
		if departure_time_as_tz < now():
			raise ValidationError(f"The departure time {field.data} has already passed.")
		form.departure_time.data = departure_time_as_tz


class DeleteBusScheduleForm(FlaskForm):
    id = IntegerField(validators=[DataRequired()], widget=HiddenInput())
    schedule_cancelled_reason = StringField("Enter reason for cancelling the schedule", widget=TextArea(), validators=[DataRequired()])
    delete_bookings = BooleanField("Delete all bookings made.")
    submit = SubmitField('Yes, proceed')
