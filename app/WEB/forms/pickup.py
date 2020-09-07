from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from wtforms.widgets import HiddenInput, Select
from app.models import Pickup


# validators
def unique_create_name(form, field):
    if Pickup.query.filter_by(name=field.data).first():
        raise ValidationError(f"The status '{field.data}' already exists.")


class CreatePickupForm(FlaskForm):
    name = StringField("Add Pickup", validators=[DataRequired(), unique_create_name])
    submit = SubmitField('Save')

    def __init__(self, *args, **kwargs):
    	super().__init__(*args, **kwargs)



class DeletePickupForm(FlaskForm):
    id = StringField(validators=[DataRequired()], widget=HiddenInput())
    submit = SubmitField('Confirm')

    def __init__(self, *args, **kwargs):
    	super().__init__(*args, **kwargs)