from flask import Blueprint, render_template, url_for, request, redirect, flash
from app.models import Journey, Pickup, db
from ..forms import CreatePickupForm, DeletePickupForm

pickup_bp = Blueprint('pickup', __name__, url_prefix='/pickup')


@pickup_bp.route("/", methods=["GET"])
def get_pickups():
    pickups = Pickup.query.all()
    return render_template("pickup/pickups.html", pickups=pickups)


@pickup_bp.route("/create/<int:journey_id>", methods=["POST"])
def create_pickup(journey_id):
	journey = Journey.query.get(journey_id)
	create_pickup_form = CreatePickupForm()
	if create_pickup_form.validate_on_submit():
		# create pickup
		name = create_pickup_form.name.data
		pickup = Pickup(name=name, journey=journey)
		db.session.commit()
		flash("Pickup created.", "success")
	else:
		flash(str(create_pickup_form.errors), "danger")
	return redirect(url_for('journey.get_journey', journey_id=journey.id))


@pickup_bp.route("/<int:pickup_id>/delete", methods=["GET", "POST"])
def delete_pickup(pickup_id):
	pickup = Pickup.query.get(pickup_id)
	journey = pickup.journey
	if request.method == "POST":
		db.session.delete(pickup)
		db.session.commit()
		flash("Deleted pickup", "success")
		return redirect(url_for('journey.get_journey', journey_id=journey.id))
	else:
		delete_pickup_form = DeletePickupForm(obj=pickup)
		delete_pickup_patch_template = render_template('pickup/delete-pickup-patch.html', pickup=pickup, delete_pickup_form=delete_pickup_form)
		data = {
            "form_templates": {
                "#deletePickupPatch": delete_pickup_patch_template
            }
        };return data
