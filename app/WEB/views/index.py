from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import login_user, logout_user, current_user
from app.utils import authenticate_user
from ..forms import LoginForm
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
		else:
			return redirect(url_for('index.logout'))

	return redirect(url_for('index.login'))


@index_bp.route('login', methods=["POST", "GET"])
def login():
	login_form = LoginForm()
	if login_form.validate_on_submit():
		username = login_form.email.data
		password = login_form.password.data
		user = authenticate_user(username, password)
		if user:
			login_user(user)
			return redirect(url_for('index.index'))
		else:
			flash("User not found", "danger")
	return render_template("index/login.html", login_form=login_form)


@index_bp.route('logout', methods=["GET"])
def logout():
	logout_user()
	return redirect(url_for('index.index'))