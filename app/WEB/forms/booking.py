import json
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from wtforms.widgets import HiddenInput, Select
from app.utils import get_current_branch
from app.models import Pricing


class CreateBookingForm(FlaskForm):
    grid_id = IntegerField(validators=[DataRequired()], widget=HiddenInput())
    pricing_id = SelectField("Select Fare", validators=[DataRequired()], coerce=int)
    passenger_name = StringField("Passenger Name", validators=[DataRequired()])
    passenger_telephone = StringField("Passenger Telephone")
    pickup = SelectField("Pickup Station")
    paid = BooleanField("Paid ?", default=True)
    submit = SubmitField('Book')

    def __init__(self, grid, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bus = grid.bus
        journey = bus.journey
        pricings = journey.pricings
        pickups = journey.pickups
        self.pricing_id.choices = [(pricing.id, pricing) for pricing in pricings]
        self.pickup.choices = [(pickup.name, pickup.name) for pickup in pickups]