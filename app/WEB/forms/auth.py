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


class ResetPasswordForm(FlaskForm):
	email = StringField("Please enter your email address to continue.", validators=[DataRequired(), Email()])
	submit = SubmitField("Continue")


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
