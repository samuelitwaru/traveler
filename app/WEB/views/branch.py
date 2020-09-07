from flask import Blueprint, render_template, url_for, request, redirect, flash
from app.models import Company, Branch, Profile, User, db
from app.helpers import send_auth_mail
from app.utils import create_user_token
from ..forms import CreateBranchForm, CreateProfileForm, DeleteProfileForm

branch_bp = Blueprint('branch', __name__, url_prefix='/branch')


@branch_bp.route("/", methods=["GET"])
def get_branches():
    branches = Branch.query.all()
    return render_template("branch/branches.html", companies=companies)



@branch_bp.route("/create/<int:company_id>", methods=["POST"])
def create_branch(company_id):
	company = Company.query.get(company_id)
	create_branch_form = CreateBranchForm()
	if create_branch_form.validate_on_submit():
		# create branch
		name = create_branch_form.name.data
		location = create_branch_form.location.data
		branch = Branch(name, location, company)
		db.session.commit()
		flash("Branch created.", "success")
		return redirect(url_for('company.get_company_branch', company_id=company.id, branch_id=branch.id))
	flash(str(create_branch_form.errors), "danger")
	return redirect(url_for('company.get_company_branches', company_id=company.id))



@branch_bp.route("/<int:branch_id>/manager/create", methods=["POST"])
def create_branch_manager(branch_id): 
	create_profile_form = CreateProfileForm()
	branch = Branch.query.get(branch_id)
	if create_profile_form.validate_on_submit():
		first_name = create_profile_form.data.get("first_name")
		last_name = create_profile_form.data.get("last_name")
		email = create_profile_form.data.get("email")
		telephone = create_profile_form.data.get("telephone")

		user = User(email=email, username=email)
		profile = Profile(first_name=first_name, last_name=last_name, telephone=telephone, is_manager=True)
		profile.branch = branch
		profile.user = user
		db.session.add(user)
		db.session.add(profile)
		create_user_token(user)
		db.session.commit()
		send_auth_mail(user)
		flash("Profile created", "success")
	else:
		flash(f"{create_profile_form.errors}", "danger")

	return redirect(request.referrer)



@branch_bp.route("/<int:branch_id>/manager/delete", methods=["POST"])
def delete_branch_manager(branch_id): 
	delete_profile_form = DeleteProfileForm()
	branch = Branch.query.get(branch_id)
	if delete_profile_form.validate_on_submit():
		profile_id = delete_profile_form.data.get("id")
		profile = Profile.query.get(profile_id)
		if profile == branch.manager():
			db.session.delete(profile)
			db.session.delete(profile.user)
			db.session.commit()
			flash("Profile deleted", "success")
		else:
			flash("An error occured!", "danger")
	else:
		flash(f"{delete_profile_form.errors}", "danger")

	return redirect(request.referrer)





