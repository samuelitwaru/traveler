from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.widgets import HiddenInput


class SetPasswordForm(FlaskForm):
	password = PasswordField("Password", validators=[DataRequired()])
	confirm_password = PasswordField("Confirm password", validators=[DataRequired(), EqualTo("password")])
	submit = SubmitField("Submit")

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)


class ForgotPasswordForm(FlaskForm):
	email = StringField("Email", validators=[DataRequired(), Email()])
	submit = SubmitField("Submit")


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
