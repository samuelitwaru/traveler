from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from wtforms.widgets import HiddenInput, Select
from app.models import Pickup


class CreatePickupForm(FlaskForm):
    name = StringField("Add Pickup", validators=[DataRequired()])
    submit = SubmitField('Save')

    def __init__(self, *args, **kwargs):
    	super().__init__(*args, **kwargs)



class DeletePickupForm(FlaskForm):
    id = StringField(validators=[DataRequired()], widget=HiddenInput())
    submit = SubmitField('Confirm')

    def __init__(self, *args, **kwargs):
    	super().__init__(*args, **kwargs)