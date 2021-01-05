from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import current_user, login_required
from app.models import Profile, User, db
from app.helpers import send_auth_mail
from app.utils import get_current_branch, create_user_token, join_telephone, split_telephone, update_profile_email_and_telephone, process_momo_pay
from ..forms import CreateProfileForm, UpdateProfileForm, DeleteProfileForm, SignupForm, SearchBusesForm, UpdateUserPasswordForm, UpdateProfileCreditForm


profile_bp = Blueprint('profile', __name__, url_prefix='/profile')


@profile_bp.route("/cashier")
@login_required
def get_cashier_profiles():
	branch = get_current_branch()
	cashiers = Profile.query.filter_by(branch_id=branch.id, is_cashier=True).all()
	create_profile_form = CreateProfileForm()
	return render_template('profile/cashier-profiles.html', cashiers=cashiers, create_profile_form=create_profile_form)


@profile_bp.route("/cashier/create", methods=["POST"])
@login_required
def create_cashier_profile(): 
	create_profile_form = CreateProfileForm()
	branch = get_current_branch()
	if create_profile_form.validate_on_submit():
		first_name = create_profile_form.data.get("first_name")
		last_name = create_profile_form.data.get("last_name")
		email = create_profile_form.data.get("email")
		telephone_code = create_profile_form.data.get("telephone_code")
		telephone = create_profile_form.data.get("telephone")

		user = User(username=email)
		profile = Profile(first_name=first_name, last_name=last_name, telephone=join_telephone(telephone_code, telephone), email=email, is_cashier=True)
		profile.branch = branch
		profile.user = user
		db.session.add(user)
		db.session.add(profile)
		create_user_token(user)
		db.session.commit()
		send_auth_mail(user.username, user.token.token)
		flash("Cashier created", "success")
	else:
		flash(f"{create_profile_form.errors}", "danger")

	return redirect(request.referrer)


@profile_bp.route("/cashier/<int:profile_id>")
@login_required
def get_cashier_profile(profile_id): 
	cashier = Profile.query.get(profile_id)
	if cashier:
		code, telephone = split_telephone(cashier.telephone)
		cashier.telephone = telephone
		cashier.telephone_code = code
	update_profile_form = UpdateProfileForm(obj=cashier)
	delete_profile_form = DeleteProfileForm(obj=cashier)
	return render_template("profile/cashier-profile.html", cashier=cashier, update_profile_form=update_profile_form, delete_profile_form=delete_profile_form)



@profile_bp.route("/cashier/<int:profile_id>/update", methods=["POST"])
@login_required
def update_cashier_profile(profile_id): 
	update_profile_form = UpdateProfileForm()
	branch = get_current_branch()
	cashier_profile = Profile.query.get(profile_id)
	if update_profile_form.validate_on_submit():
		profile_id = update_profile_form.data.get("id")
		profile = Profile.query.get(profile_id)
		if cashier_profile == profile:
			data = update_profile_form.data
			first_name = data.get("first_name")
			last_name = data.get("last_name")
			email = data.get("email")
			telephone_code = data.get("telephone_code")		
			telephone = data.get("telephone")		
			profile.first_name = first_name
			profile.last_name = last_name
			new_email = email
			new_telephone = join_telephone(telephone_code, telephone)
			update_profile_email_and_telephone(profile, new_email, new_telephone)
			db.session.commit()
			flash("Cashier updated", "success")
		else:
			flash("An error occured!", "danger")
	else:
		flash(f"{update_profile_form.errors}", "danger")

	return redirect(request.referrer)
	

@profile_bp.route("/manager/<int:profile_id>/update", methods=["POST"])
@login_required
def update_manager_profile(profile_id): 
	update_profile_form = UpdateProfileForm()
	branch = get_current_branch()
	manager_profile = Profile.query.get(profile_id)
	if update_profile_form.validate_on_submit():
		profile_id = update_profile_form.data.get("id")
		profile = Profile.query.get(profile_id)
		if manager_profile == profile:
			data = update_profile_form.data
			first_name = data.get("first_name")
			last_name = data.get("last_name")
			email = data.get("email")
			telephone_code = data.get("telephone_code")		
			telephone = data.get("telephone")		
			profile.first_name = first_name
			profile.last_name = last_name
			new_email = email
			new_telephone = join_telephone(telephone_code, telephone)
			update_profile_email_and_telephone(profile, new_email, new_telephone)
			db.session.commit()
			flash("Manager updated", "success")
		else:
			flash("An error occured!", "danger")

	else:
		flash(f"{update_profile_form.errors}", "danger")

	return redirect(request.referrer)



@profile_bp.route("/cashier/<int:profile_id>/delete", methods=["POST"])
@login_required
def delete_cashier_profile(profile_id): 
	delete_profile_form = DeleteProfileForm()
	branch = get_current_branch()
	cashier_profile = Profile.query.get(profile_id)
	if delete_profile_form.validate_on_submit():
		profile_id = delete_profile_form.data.get("id")
		profile = Profile.query.get(profile_id)
		if cashier_profile == profile:
			db.session.delete(profile)
			db.session.delete(profile.user)
			db.session.commit()
			flash("Cashier deleted", "success")
		else:
			flash("An error occured!", "danger")
	else:
		flash(f"{delete_profile_form.errors}", "danger")

	return redirect(url_for('profile.get_cashier_profiles'))



@profile_bp.route("/passenger/create", methods=["POST"])
@login_required
def create_passenger_profile(): 
	signup_form = SignupForm()
	if signup_form.validate_on_submit():
		first_name = signup_form.data.get("first_name")
		last_name = signup_form.data.get("last_name")
		email = signup_form.data.get("email")
		telephone_code = signup_form.data.get("telephone_code")
		telephone = signup_form.data.get("telephone")
		password = signup_form.data.get("password")

		user = User(password=password, username=email)
		profile = Profile(first_name=first_name, last_name=last_name, telephone=join_telephone(telephone_code, telephone), email=email, is_passenger=True)
		profile.user = user
		db.session.add(user)
		db.session.add(profile)
		create_user_token(user)
		db.session.commit()
		send_auth_mail(user.username, user.token.token)
		flash("Registration was successful. Login here.", "success")
		return redirect(url_for('index.login'))

	else:
		flash(f"{signup_form.errors}", "danger")
		search_buses_form = SearchBusesForm()
		return render_template('index/index.html', search_buses_form=search_buses_form, signup_form=signup_form)



@profile_bp.route("/passenger", methods=["GET", "POST"])
@login_required
def update_profile():
	user = current_user
	profile = user.profile
	
	if profile:
		code, telephone = split_telephone(profile.telephone)
		profile.telephone = telephone
		profile.telephone_code = code

	update_profile_form = UpdateProfileForm(obj=user.profile)
	update_user_password_form = UpdateUserPasswordForm(current_user=user)
	if update_profile_form.validate_on_submit():
		data = update_profile_form.data
		first_name = data.get("first_name")
		last_name = data.get("last_name")
		email = data.get("email")
		telephone_code = data.get("telephone_code")		
		telephone = data.get("telephone")		
		profile.first_name = first_name
		profile.last_name = last_name
		new_email = email
		new_telephone = join_telephone(telephone_code, telephone)
		update_profile_email_and_telephone(profile, new_email, new_telephone)
		db.session.commit()
		flash("Profile updated.", "success")
		
	return render_template('profile/passenger-profile.html', update_user_password_form=update_user_password_form, update_profile_form=update_profile_form)


@profile_bp.route("/credit", methods=["POST", "GET"])
@login_required
def get_profile_credit():
	user = current_user
	profile = user.profile
	update_profile_credit_form = UpdateProfileCreditForm(profile=profile)
	if request.method == "POST":
		if update_profile_credit_form.validate_on_submit():
			# get info
			data = update_profile_credit_form.data
			telephone_code = data.get("telephone_code")		
			telephone = data.get("telephone")
			amount = data.get("amount")
			telephone = join_telephone(telephone_code, telephone, joiner="")
			success = process_momo_pay(telephone, amount)
			update_profile_credit_process_patch_template = render_template('profile/update-profile-credit-process-patch.html', success=success)
			data = {
				"form_templates": {
					"#updateProfileCreditFormPatch": update_profile_credit_process_patch_template
				}
			}
			
		else:
			update_profile_credit_patch_template = render_template('profile/update-profile-credit-patch.html', update_profile_credit_form=update_profile_credit_form)
			data = {
				"form_templates": {
					"#updateProfileCreditFormPatch": update_profile_credit_patch_template
				}
			}

		print(data)
		return data
		
	
	return render_template('profile/profile-credit.html', update_profile_credit_form=update_profile_credit_form)
