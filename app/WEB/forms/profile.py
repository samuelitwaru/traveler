from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.widgets import HiddenInput, Select
from app.models import User, Profile

telephone_code_choices = [("256", "+256")]

# validators
def unique_create_email(form, field):
    if User.query.filter_by(email=field.data).first():
        raise ValidationError(f"A user with email '{field.data}' already exists.")

def unique_create_telephone(form, field):
    if Profile.query.filter_by(telephone=field.data).first():
        raise ValidationError(f"A user with telephone '{field.data}' already exists.")

def unique_update_telephone(form, field):
    if Profile.query.filter(Profile.id!=form.id.data).filter_by(telephone=field.data).first():
        raise ValidationError(f"A user with telephone '{field.data}' already exists.")

def validate_telephone(form, field):
    telephone_code = form.data.get("telephone_code")
    telephone = field.data
    if not (telephone_code and telephone):
        raise ValidationError(f"Invalid Telephone.")


class CreateProfileForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), unique_create_email])
    telephone_code = SelectField(choices=telephone_code_choices)
    telephone = StringField("Telephone", validators=[DataRequired(), validate_telephone, unique_create_telephone])
    submit = SubmitField('Save')

    def __init__(self, *args, **kwargs):
    	super().__init__(*args, **kwargs)

class UpdateProfileForm(FlaskForm):
    id = IntegerField(validators=[DataRequired()], widget=HiddenInput())
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    telephone_code = SelectField(choices=telephone_code_choices)
    telephone = StringField("Telephone", validators=[DataRequired(), validate_telephone, unique_update_telephone])
    submit = SubmitField('Save')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate_telephone(form, field):
        telephone_code = form.data.get("telephone_code")
        telephone = field.data
        if not (telephone_code and telephone):
            raise ValidationError(f"Invalid Telephone.")
        

class DeleteProfileForm(FlaskForm):
    id = IntegerField(validators=[DataRequired()], widget=HiddenInput())
    submit = SubmitField('Confirm')

    def __init__(self, *args, **kwargs):
    	super().__init__(*args, **kwargs)


class SignupForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), unique_create_email])
    telephone_code = SelectField(choices=telephone_code_choices)
    telephone = StringField("Telephone", validators=[DataRequired(), validate_telephone, unique_create_telephone])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField('Save')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)