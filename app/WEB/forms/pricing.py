from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from wtforms.widgets import HiddenInput, Select
from app.models import Pricing


class CreatePricingForm(FlaskForm):
    stop = StringField("Stop Station", validators=[DataRequired()])
    price = IntegerField("Price / Fare", validators=[DataRequired()])
    submit = SubmitField('Add')

    def __init__(self, *args, **kwargs):
    	super().__init__(*args, **kwargs)



class DeletePricingForm(FlaskForm):
    id = StringField(validators=[DataRequired()], widget=HiddenInput())
    submit = SubmitField('Confirm')

    def __init__(self, *args, **kwargs):
    	super().__init__(*args, **kwargs)