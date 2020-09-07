from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from wtforms.widgets import HiddenInput
from app.models import Company


# validators
def unique_create_name(form, field):
    if Company.query.filter_by(name=field.data).first():
        raise ValidationError(f"The Company '{field.data}' already exists.")


class CreateCompanyForm(FlaskForm):
    name = StringField("Company Name", validators=[DataRequired(), unique_create_name])
    logo = FileField("Company Logo", validators=[DataRequired()])
    h = FloatField(validators=[DataRequired()], widget=HiddenInput())
    w = FloatField(validators=[DataRequired()], widget=HiddenInput())
    x = FloatField(validators=[DataRequired()], widget=HiddenInput())
    y = FloatField(validators=[DataRequired()], widget=HiddenInput())
    submit = SubmitField('Register')


class UpdateCompanyForm(FlaskForm):
    name = StringField("Company Name", validators=[DataRequired()])
    logo = FileField("Company Logo", validators=[DataRequired()])
    h = FloatField(validators=[DataRequired()], widget=HiddenInput())
    w = FloatField(validators=[DataRequired()], widget=HiddenInput())
    x = FloatField(validators=[DataRequired()], widget=HiddenInput())
    y = FloatField(validators=[DataRequired()], widget=HiddenInput())
    submit = SubmitField('Save')