from flask import Blueprint, render_template, url_for, request, redirect, flash
from app.models import Company, Pricing, Journey, Status, db
from app.utils import get_current_branch
from ..forms import CreatePricingForm, DeletePricingForm

pricing_bp = Blueprint('pricing', __name__, url_prefix='/pricing')


@pricing_bp.route("/", methods=["GET"])
def get_pricings():
    pricings = Pricing.query.all()
    return render_template("pricing/pricings.html", pricings=pricings)


@pricing_bp.route("/create/<int:journey_id>/<int:status_id>", methods=["POST"])
def create_pricing(journey_id, status_id):
	journey = Journey.query.get(journey_id)
	status = Status.query.get(status_id)
	create_pricing_form = CreatePricingForm()
	if create_pricing_form.validate_on_submit():
		# create pricing
		stop = create_pricing_form.stop.data
		price = create_pricing_form.price.data
		pricing = Pricing(stop=stop, price=price, journey=journey, status=status)
		db.session.add(pricing)
		db.session.commit()
		flash("Pricing created.", "success")
	else:
		flash(str(create_pricing_form.errors), "danger")
	return redirect(request.referrer)


@pricing_bp.route("/<int:pricing_id>/delete", methods=["GET", "POST"])
def delete_pricing(pricing_id):
	pricing = Pricing.query.get(pricing_id)
	if request.method == "POST":
		db.session.delete(pricing)
		db.session.commit()
		flash("Deleted pricing", "success")
		return redirect(request.referrer)
	else:
		delete_pricing_form = DeletePricingForm(obj=pricing)
		delete_pricing_patch_template = render_template('pricing/delete-pricing-patch.html', pricing=pricing, delete_pricing_form=delete_pricing_form)
		data = {
            "form_templates": {
                "#deletePricingPatch": delete_pricing_patch_template
            }
        };return data


