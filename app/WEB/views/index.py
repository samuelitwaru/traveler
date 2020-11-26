from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import login_user, logout_user, current_user
from app.utils import authenticate_user
from app.models import User
from ..forms import LoginForm, SearchBusesForm, CreateProfileForm, SignupForm
from .. guards import check_branch_journeys

index_bp = Blueprint('index', __name__, url_prefix='/')

@check_branch_journeys
@index_bp.route('/')
def index():
	user = current_user
	if user.is_authenticated:
		profile = user.profile
		if profile.is_admin:
			return redirect(url_for('company.get_companies'))
		elif profile.is_manager or profile.is_cashier:
			return redirect(url_for('bus.get_buses'))
		elif profile.is_passenger:
			search_buses_form = SearchBusesForm()
			return redirect(url_for('bus.search_buses'))
		else:
			return redirect(url_for('index.logout'))

	search_buses_form = SearchBusesForm()
	signup_form = SignupForm()

	return render_template('index/index.html', search_buses_form=search_buses_form, signup_form=signup_form)





@index_bp.route('login', methods=["POST", "GET"])
def login():
	user = current_user
	if user.is_authenticated:
		return redirect(url_for('index.index'))

	login_form = LoginForm()
	if login_form.validate_on_submit():
		username = login_form.email.data
		password = login_form.password.data
		user = authenticate_user(username, password)
		if user and user.is_active:
			login_user(user)
			return redirect(url_for('index.index'))
		else:
			user = User.query.filter_by(username=username, recovery_password=password).first()
			if user and user.token:
				flash("You have used a recovery password. Please set a new password to login.", "info")
				return redirect(url_for('auth.set_password', token=user.token.token))
			flash("User not found", "danger")
	return render_template("index/login.html", login_form=login_form)


@index_bp.route('logout', methods=["GET"])
def logout():
	logout_user()
	return redirect(url_for('index.index'))