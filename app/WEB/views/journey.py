from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import login_required
from app.models import Journey, Status, Pricing, db
from app.utils import get_current_branch
from ..forms import CreateJourneyForm, CreatePickupForm, CreatePricingForm, UpdateJourneyForm


journey_bp = Blueprint('journey', __name__, url_prefix='/journey')


@journey_bp.route("")
@login_required
def get_journeys():
	branch = get_current_branch()
	journeys = Journey.query.filter_by(branch_id=branch.id).all()
	create_journey_form = CreateJourneyForm()
	return render_template("journey/journeys.html", journeys=journeys, create_journey_form=create_journey_form)


@journey_bp.route("/<int:journey_id>")
@login_required
def get_journey(journey_id):
	branch = get_current_branch()
	journey = Journey.query.get(journey_id)
	statuses = branch.company.statuses
	create_pickup_form = CreatePickupForm()
	create_pricing_form = CreatePricingForm()
	update_journey_form = UpdateJourneyForm(obj=journey)
	return render_template("journey/journey.html", journey=journey, create_pickup_form=create_pickup_form, create_pricing_form=create_pricing_form, statuses=statuses, update_journey_form=update_journey_form)


@journey_bp.route("/<int:journey_id>/<int:status_id>/pricings", methods=["GET"])
@login_required
def get_journey_pricings(journey_id, status_id):
	journey = Journey.query.get(journey_id)
	status = Status.query.get(status_id)
	branch = get_current_branch()
	statuses = branch.company.statuses
	pricings = Pricing.query.filter_by(journey_id=journey.id, status_id=status.id)
	create_pricing_form = CreatePricingForm()
	pricings_patch_template = render_template('pricing/pricings-patch.html', pricings=pricings, journey=journey, active_status=status, statuses=statuses, create_pricing_form=create_pricing_form)
	data = {
		"form_templates": {
			"#pricingsPatch": pricings_patch_template
	    }
	};return data

@journey_bp.route("/create", methods=["POST"])
@login_required
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
@login_required
def update_journey(journey_id): 
	update_journey_form = UpdateJourneyForm()
	branch = get_current_branch()
	journey = Journey.query.get(journey_id)
	if update_journey_form.validate_on_submit():
		journey_id = update_journey_form.id.data
		journey.to = update_journey_form.to.data
		journey.from_ = update_journey_form.from_.data
		journey.distance = update_journey_form.distance.data
		journey.duration = update_journey_form.duration.data
		db.session.commit()
		flash("Journey updated", "success")
	else:
		flash(f"{update_journey_form.errors}", "danger")

	return redirect(request.referrer)