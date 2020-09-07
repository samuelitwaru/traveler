from flask_wtf import FlaskForm
import wtforms
from wtforms import validators
from wtforms import widgets


class LoginForm(FlaskForm):
    email = wtforms.StringField("Email", validators=[validators.DataRequired(), validators.Email()])
    password = wtforms.PasswordField("Password", validators=[validators.DataRequired()])
    submit = wtforms.SubmitField('Register')