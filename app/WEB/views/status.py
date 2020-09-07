from flask import Blueprint, render_template, url_for, request, redirect, flash
from app.models import Company, Status, Journey, db
from ..forms import CreateStatusForm, UpdateStatusForm, DeleteStatusForm, CreatePricingForm

status_bp = Blueprint('status', __name__, url_prefix='/status')


@status_bp.route("/", methods=["GET"])
def get_statuses():
    statuses = Status.query.all()
    return render_template("status/statuses.html", statuses=statuses)


@status_bp.route("/<int:status_id>", methods=["GET"])
def get_status(status_id):
	journey_id = request.referrer.split('/')[-1]
	journey = Journey.query.get(journey_id)
	status = Status.query.get(status_id)
	statuses = Status.query.all()
	create_pricing_form = CreatePricingForm()
	status_patch_template = render_template('status/status-patch.html', active_status=status, create_pricing_form=create_pricing_form, statuses=statuses, journey=journey)
	data = {
		"form_templates": {
			"#statusPatch": status_patch_template
	    }
	};return data


@status_bp.route("/create/<int:company_id>", methods=["POST"])
def create_status(company_id):
	company = Company.query.get(company_id)
	create_status_form = CreateStatusForm(company=company)
	if create_status_form.validate_on_submit():
		# create status
		name = create_status_form.name.data
		status = Status(name=name, company=company)
		db.session.commit()
		flash("Status created.", "success")
	else:
		flash(str(create_status_form.errors), "danger")
	return redirect(url_for('company.get_company_statuses', company_id=company.id))


@status_bp.route("/<int:status_id>/update", methods=["GET", "POST"])
def update_status(status_id):
	status = Status.query.get(status_id)
	company = status.company
	update_status_form = UpdateStatusForm(obj=status, company=company)
	if request.method == "POST":
		if update_status_form.validate():
			name = update_status_form.name.data
			status.name = name
			db.session.commit()
			flash("Updated status", "success")
		else:
			flash(str(update_status_form.errors), "danger")
		return redirect(url_for('company.get_company_statuses', company_id=company.id))

	else:
		update_status_form = UpdateStatusForm(obj=status, company=company)
		update_status_patch_template = render_template('status/update-status-patch.html', status=status, update_status_form=update_status_form)
		data = {
            "form_templates": {
                "#updateStatusPatch": update_status_patch_template
            }
        };return data


@status_bp.route("/<int:status_id>/delete", methods=["GET", "POST"])
def delete_status(status_id):
	status = Status.query.get(status_id)
	company = status.company
	if request.method == "POST":
		db.session.delete(status)
		db.session.commit()
		flash("Deleted status", "success")
		return redirect(url_for('company.get_company_statuses', company_id=company.id))
	else:
		delete_status_form = DeleteStatusForm(obj=status)
		delete_status_patch_template = render_template('status/delete-status-patch.html', status=status, delete_status_form=delete_status_form)
		data = {
            "form_templates": {
                "#deleteStatusPatch": delete_status_patch_template
            }
        };return data


