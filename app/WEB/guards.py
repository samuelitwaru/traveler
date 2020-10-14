from functools import wraps
from flask import redirect, url_for
from flask import request, flash
from app.utils import get_current_branch


def check_branch_journeys(func):
	'''Checks if a branch has atleast 1 journey and the jounrey has atleast 1 pickup and pricing'''
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
