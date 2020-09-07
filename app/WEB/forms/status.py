from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from wtforms.widgets import HiddenInput, Select
from app.models import Status


# validators
def unique_create_name(form, field):
    if Status.query.filter_by(name=field.data, company_id=form.company.id).first():
        raise ValidationError(f"The status '{field.data}' already exists.")

def unique_update_name(form, field):
    if Status.query.filter(Status.id!=form.id.data).filter_by(name=field.data, company_id=form.company.id).first():
        raise ValidationError(f"The status '{field.data}' already exists.")


class CreateStatusForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), unique_create_name])
    submit = SubmitField('Save')

    def __init__(self, company, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.company=company


class UpdateStatusForm(FlaskForm):
    id = IntegerField(validators=[DataRequired()], widget=HiddenInput())
    name = StringField("Name", validators=[DataRequired(), unique_update_name])
    submit = SubmitField('Save')

    def __init__(self, company, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.company=company


class DeleteStatusForm(FlaskForm):
    id = IntegerField(validators=[DataRequired()], widget=HiddenInput())
    submit = SubmitField('Confirm')

    def __init__(self, *args, **kwargs):
    	super().__init__(*args, **kwargs)