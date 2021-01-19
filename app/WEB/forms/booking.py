from datetime import datetime, timedelta
import json
import re
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Email
from wtforms.widgets import HiddenInput, Select
from app.utils import get_current_branch
from app.models import Pricing
from app.helpers import now

telephone_code_choices = [("256", "+256")]


def validate_telephone(form, field):
    telephone_code = form.data.get("telephone_code")
    telephone = field.data
    pattern = "^0(7(?:(?:[129][0-9])|(?:0[0-8])|(4[0-1]))[0-9]{6})$"
    matched = bool(re.match(pattern, telephone))
    if not (telephone_code and telephone):
        raise ValidationError(f"Invalid Telephone.")


class CreateBookingForm(FlaskForm):
    grid_id = SelectField("Seat", validators=[DataRequired(message='Select a seat')], coerce=int)
    passenger_name = StringField("Name", validators=[DataRequired()])
    pricing_id = SelectField("Select Destination", validators=[DataRequired()], coerce=int)
    telephone_code = SelectField(choices=telephone_code_choices)
    passenger_telephone = StringField("Telephone Number", validators=[DataRequired(), validate_telephone])
    pickup = SelectField("Pickup Station")

    def __init__(self, bus=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if bus:
            journey = bus.journey
            pricings = journey.pricings
            pickups = journey.pickups
            grids = bus.grids.filter_by(grid_type=1, booking_id=None)
            self.grid_id.choices = [(0, "No Seat Selected")]+[(grid.id, f"Seat {grid}") for grid in grids]
            self.pricing_id.choices = [(pricing.id, pricing) for pricing in pricings]
            self.pickup.choices = [(pickup.name, pickup.name) for pickup in pickups]


class CreatePassengerBookingForm(FlaskForm):
    grid_id = SelectField("Seat", validators=[DataRequired(message='Select a seat')], coerce=int)
    passenger_name = StringField("Your Name", validators=[DataRequired()])
    passenger_email = StringField("Your Email (For Reporting Purposes)", validators=[DataRequired(), Email()])
    pricing_id = SelectField("Select Destination", validators=[DataRequired()], coerce=int)
    telephone_code = SelectField(choices=telephone_code_choices)
    passenger_telephone = StringField("Telephone Number (For Payment Purposes)", validators=[DataRequired(), validate_telephone])
    pickup = SelectField("Pickup Station")

    def __init__(self, bus=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if bus:
            journey = bus.journey
            pricings = journey.pricings
            pickups = journey.pickups
            grids = bus.grids.filter_by(grid_type=1, booking_id=None)
            self.grid_id.choices = [(0, "No Seat Selected")]+[(grid.id, f"Seat {grid}") for grid in grids]
            self.pricing_id.choices = [(pricing.id, pricing.app_pricing_string()) for pricing in pricings]
            self.pickup.choices = [(pickup.name, pickup.name) for pickup in pickups]


class UpdateBookingForm(FlaskForm):
    id = IntegerField(validators=[DataRequired()], widget=HiddenInput())
    grid_id = IntegerField(validators=[DataRequired()], widget=HiddenInput())
    pricing_id = SelectField("Select Fare", validators=[DataRequired()], coerce=int)
    passenger_name = StringField("Passenger Name", validators=[DataRequired()])
    passenger_telephone = StringField("Passenger Telephone")
    pickup = SelectField("Pickup Station")
    paid = BooleanField("Paid ?", id="paid_for_update")
    submit = SubmitField('Save')

    def __init__(self, grid=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bus = grid.bus
        journey = bus.journey
        pricings = journey.pricings
        pickups = journey.pickups
        self.pricing_id.choices = [(pricing.id, pricing) for pricing in pricings]
        self.pickup.choices = [(pickup.name, pickup.name) for pickup in pickups]


class DeleteBookingForm(FlaskForm):
    id = IntegerField(validators=[DataRequired()], widget=HiddenInput())
    submit = SubmitField('Delete')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class FilterBookingsForm(FlaskForm):
    created_on_gte = StringField("From (Date)", default=(now()-timedelta(2)).strftime("%B %d %Y"))
    created_on_lte = StringField("To (Date)", default=(now()+timedelta(2)).strftime("%B %d %Y"))
    bus_id = SelectField("Bus", coerce=int)
    submit = SubmitField('Filter')

    def __init__(self, bus_id_choices=[], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bus_id.choices = [(0, "All")] + bus_id_choices
        self.datetime_format = "%B %d %Y"
        self.created_on_gte.default = "Jan 1 2000"
        self.created_on_lte.default = "Dec 31 3000"

    def validate_created_on_gte(form, field):
        created_on_gte = field.data
        if created_on_gte:
            created_on_gte = datetime.strptime(f"{created_on_gte}", form.datetime_format)
        
        created_on_lte = form.created_on_lte.data
        if created_on_lte:
            created_on_lte = datetime.strptime(f"{created_on_lte}", form.datetime_format)

        
        if (created_on_gte and created_on_lte) and created_on_gte > created_on_lte:
            raise ValidationError(f"'From' date should be before the 'To' date.")



        form.created_on_gte.data = created_on_gte
        form.created_on_lte.data = created_on_lte
