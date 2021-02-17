from functools import wraps
from flask import redirect, url_for, request, flash
from flask_login import current_user
from app.utils import get_current_branch
from app.models import Bus


def check_branch_journeys(func):

	'''Checks if a branch has atleast 1 journey and the journey has atleast 1 pickup and pricing'''
	
	@wraps(func)
	def wrapper(*args, **kwargs):
		branch = get_current_branch()
		if branch:
			journeys = branch.journeys
			if len(journeys):
				for journey in journeys:
					if len(journey.pickups) and len(journey.pricings):
						return func(*args, **kwargs)
					else:
						flash(f"The journey {journey} has not been setup properly.", "warning")
						return func(*args, **kwargs)
			else:
				flash("Setup atleast one journey.", "warning")
				return func(*args, **kwargs)
		else:
			return func(*args, **kwargs)

	return wrapper


def only_bus_with_no_bookings(func):
	
	@wraps(func)
	def wrapper(*args, **kwargs):
		return func(*args, **kwargs)
	return wrapper


def only_admin(func):
	
	@wraps(func)
	def wrapper(*args, **kwargs):
		if current_user.is_authenticated:
			if current_user.profile.is_admin:
				return func(*args, **kwargs)
		flash("Action Not Allowed!", "danger")
		return redirect(request.referrer)
	return wrapper


def only_manager(func):
	
	@wraps(func)
	def wrapper(*args, **kwargs):
		if current_user.is_authenticated:
			if current_user.profile.is_manager:
				return func(*args, **kwargs)
		flash("Action Not Allowed!", "danger")
		return redirect(request.referrer)
	return wrapper


def only_cashier(func):
	
	@wraps(func)
	def wrapper(*args, **kwargs):
		if current_user.is_authenticated:
			if current_user.profile.is_cashier:
				return func(*args, **kwargs)
		flash("Action Not Allowed!", "danger")
		return redirect(request.referrer)
	return wrapper


def only_passenger(func):
	
	@wraps(func)
	def wrapper(*args, **kwargs):
		if current_user.is_authenticated:
			if current_user.profile.is_passenger:
				return func(*args, **kwargs)
		flash("Action Not Allowed!", "danger")
		return redirect(request.referrer)
	return wrapper


def only_unschduled_bus(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		bus_id = kwargs.get("bus_id")
		bus = Bus.query.get(bus_id)
		if bus.journey:
			flash("Action Not Allowed!", "danger")
			return redirect(request.referrer)
		return func(*args, **kwargs)
	return wrapper