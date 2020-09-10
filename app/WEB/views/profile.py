from flask import Blueprint, render_template, url_for, request, redirect, flash
from app.models import Profile, User, db
from app.helpers import send_auth_mail
from app.utils import get_current_branch, create_user_token
from ..forms import CreateProfileForm, UpdateProfileForm, DeleteProfileForm


profile_bp = Blueprint('profile', __name__, url_prefix='/profile')


@profile_bp.route("/cashier")
def get_cashier_profiles():
	branch = get_current_branch()
	cashiers = Profile.query.filter_by(branch_id=branch.id, is_cashier=True).all()
	create_profile_form = CreateProfileForm()
	return render_template('profile/cashier-profiles.html', cashiers=cashiers, create_profile_form=create_profile_form)


@profile_bp.route("/cashier/create", methods=["POST"])
def create_cashier_profile(): 
	create_profile_form = CreateProfileForm()
	branch = get_current_branch()
	if create_profile_form.validate_on_submit():
		first_name = create_profile_form.data.get("first_name")
		last_name = create_profile_form.data.get("last_name")
		email = create_profile_form.data.get("email")
		telephone = create_profile_form.data.get("telephone")

		user = User(email=email, username=email)
		profile = Profile(first_name=first_name, last_name=last_name, telephone=telephone, is_cashier=True)
		profile.branch = branch
		profile.user = user
		db.session.add(user)
		db.session.add(profile)
		create_user_token(user)
		db.session.commit()
		send_auth_mail(user)
		flash("Cashier created", "success")
	else:
		flash(f"{create_profile_form.errors}", "danger")

	return redirect(request.referrer)


@profile_bp.route("/cashier/<int:profile_id>")
def get_cashier_profile(profile_id): 
	cashier = Profile.query.get(profile_id)
	update_profile_form = UpdateProfileForm(obj=cashier)
	delete_profile_form = DeleteProfileForm(obj=cashier)
	return render_template("profile/cashier-profile.html", cashier=cashier, update_profile_form=update_profile_form, delete_profile_form=delete_profile_form)


@profile_bp.route("/cashier/<int:profile_id>/update", methods=["POST"])
def update_cashier_profile(profile_id): 
	update_profile_form = UpdateProfileForm()
	branch = get_current_branch()
	cashier_profile = Profile.query.get(profile_id)
	if update_profile_form.validate_on_submit():
		profile_id = update_profile_form.data.get("id")
		profile = Profile.query.get(profile_id)
		if cashier_profile == profile:
			data = update_profile_form.data
			first_name = update_profile_form.data.get("first_name")
			last_name = update_profile_form.data.get("last_name")
			telephone = update_profile_form.data.get("telephone")		
			
			profile.first_name = data.get("first_name")
			profile.last_name = data.get("last_name")
			profile.telephone = data.get("telephone")
			db.session.commit()
			flash("Cashier updated", "success")
		else:
			flash("An error occured!", "danger")

	else:
		flash(f"{create_profile_form.errors}", "danger")

	return redirect(request.referrer)



@profile_bp.route("/cashier/<int:profile_id>/delete", methods=["POST"])
def delete_cashier_profile(profile_id): 
	delete_profile_form = DeleteProfileForm()
	branch = get_current_branch()
	cashier_profile = Profile.query.get(profile_id)
	if delete_profile_form.validate_on_submit():
		profile_id = delete_profile_form.data.get("id")
		profile = Profile.query.get(profile_id)
		if cashier_profile == profile:
			db.session.delete(profile)
			# db.session.delete(profile.user)
			db.session.commit()
			flash("Cashier deleted", "success")
		else:
			flash("An error occured!", "danger")
	else:
		flash(f"{delete_profile_form.errors}", "danger")

	return redirect(url_for('profile.get_cashier_profiles'))



