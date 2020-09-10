from flask import Blueprint, render_template, url_for, request, redirect, flash
from app.models import Journey, db
from app.utils import get_current_branch
from ..forms import CreateJourneyForm, CreatePickupForm, CreatePricingForm, UpdateJourneyForm


journey_bp = Blueprint('journey', __name__, url_prefix='/journey')


@journey_bp.route("")
def get_journeys():
	branch = get_current_branch()
	journeys = Journey.query.filter_by(branch_id=branch.id).all()
	create_journey_form = CreateJourneyForm()
	return render_template("journey/journeys.html", journeys=journeys, create_journey_form=create_journey_form)


@journey_bp.route("/<int:journey_id>")
def get_journey(journey_id):
	branch = get_current_branch()
	journey = Journey.query.get(journey_id)
	statuses = branch.company.statuses
	create_pickup_form = CreatePickupForm()
	create_pricing_form = CreatePricingForm()
	update_journey_form = UpdateJourneyForm(obj=journey)
	return render_template("journey/journey.html", journey=journey, create_pickup_form=create_pickup_form, create_pricing_form=create_pricing_form, statuses=statuses, update_journey_form=update_journey_form)


@journey_bp.route("/create", methods=["POST"])
def create_journey():
	branch = get_current_branch()
	create_journey_form = CreateJourneyForm()
	if create_journey_form.validate_on_submit():
		# create journey
		from_ = create_journey_form.from_.data
		to = create_journey_form.to.data
		distance = create_journey_form.distance.data
		duration = create_journey_form.duration.data
		journey = Journey(from_=from_, to=to, distance=distance, duration=duration, branch=branch)
		db.session.add(journey)
		db.session.commit()
		flash("Journey created.", "success")
		return redirect(url_for('journey.get_journey', journey_id=journey.id))
	flash(str(create_journey_form.errors), "danger")
	return redirect(url_for('company.get_journeys'))


@journey_bp.route("/<int:journey_id>/update", methods=["POST"])
def update_journey(journey_id): 
	update_journey_form = UpdateJourneyForm()
	branch = get_current_branch()
	cashier_profile = Journey.query.get(profile_id)
	if update_journey_form.validate_on_submit():
		journey_id = update_journey_form.id.data
		to = update_journey_form.to.data
		from_ = update_journey_form.from_.data
		distance = update_journey_form.distance.data
		duration = update_journey_form.duration.data
		flash("Journey updated", "success")
	else:
		flash(f"{update_journey_form.errors}", "danger")

	return redirect(request.referrer)