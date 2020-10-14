from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, EqualTo
from wtforms.widgets import HiddenInput, Select
from app.models import User, Profile
from app.utils import authenticate_user


class UpdateUserPasswordForm(FlaskForm):
    current_password = PasswordField("Current Password", validators=[DataRequired()])
    new_password = PasswordField("New Password", validators=[DataRequired()])
    repeat_password = PasswordField("Repeat Password", validators=[EqualTo('new_password', message="Passwords do not match.")])

    def __init__(self, current_user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = current_user

    def validate_current_password(form, field):
        user = authenticate_user(form.user.username, field.data)
        if not user:
            raise ValidationError(f"Incorrect Current Password.")
