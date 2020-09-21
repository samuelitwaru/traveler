from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from wtforms.widgets import HiddenInput, Select


class CreateJourneyForm(FlaskForm):
    from_ = StringField("From", validators=[DataRequired()])
    to = StringField("To", validators=[DataRequired()])
    distance = FloatField("Distance (Kilometers)")
    duration = FloatField("Duration (Hours)")
    submit = SubmitField('Save')

    def __init__(self, *args, **kwargs):
    	super().__init__(*args, **kwargs)
    	

class UpdateJourneyForm(FlaskForm):
	id = IntegerField(validators=[DataRequired()], widget=HiddenInput())
	from_ = StringField("From", validators=[DataRequired()])
	to = StringField("To", validators=[DataRequired()])
	distance = FloatField("Distance (Kilometers)")
	duration = FloatField("Duration (Hours)")
	submit = SubmitField('Save')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
    	