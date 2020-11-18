import os
from flask import Blueprint, render_template, url_for, request, redirect, flash, send_from_directory
from app import app
from app.models import Company, Bus, Status, Branch, db
from app.utils import save_logo, logos, create_default_status, split_telephone, get_current_branch
from ..forms import CreateCompanyForm, UpdateCompanyForm, CreateBusForm, UpdateBusLayoutForm, CreateStatusForm, CreateBranchForm, CreateProfileForm, DeleteProfileForm, UpdateProfileForm, DeleteBusForm


company_bp = Blueprint('company', __name__, url_prefix='/company')



@company_bp.route("/", methods=["GET"])
def get_companies():
    companies = Company.query.all()
    return render_template("company/companies.html", companies=companies)

@company_bp.route("/<int:company_id>", methods=["GET", "POST"])
def get_company(company_id):
    update_company_form = UpdateCompanyForm()
    company = Company.query.get(company_id)
    return render_template("company/company.html", company=company, update_company_form=update_company_form)
    

@company_bp.route("/create", methods=["GET", "POST"])
def create_company():
    create_company_form = CreateCompanyForm()
    if create_company_form.validate_on_submit():
        name = create_company_form.data.get("name")
        logo_file = request.files.get("logo")

        logo = save_logo(logo_file, create_company_form.data.get("x"), create_company_form.data.get("y") , create_company_form.data.get("w") , create_company_form.data.get("h"))
        # save company
        company = Company(name=name, logo=logo)
        create_default_status(company)
        db.session.add(company)
        db.session.commit()
        flash("Company created.", "success")
        return redirect(url_for('company.get_company', company_id=company.id))
    return render_template("company/create-company.html", create_company_form=create_company_form)


@company_bp.route("/<int:company_id>create", methods=["POST"])
def update_company():
    company = Company.query.get(company_id)
    update_company_form = UpdateCompanyForm(request.POST)
    if update_company_form.validate_on_submit():
        name = update_company_form.data.get("name")
        logo_file = request.files.get("logo")

        logo = save_logo(logo_file, update_company_form.data.get("x"), update_company_form.data.get("y") , update_company_form.data.get("w") , update_company_form.data.get("h"))
        # save company
        company.name = name
        company.logo = logo
        db.session.commit()
        flash("Updated company", "danger")
    else:    
        flash(str(update_company_form.errors), "danger")
    return redirect(url_for('company.get_company', company_id=company.id))


@company_bp.route('/logo/<logoname>')
def get_company_logo(logoname):
    return send_from_directory(
        os.path.join(app.config['BASE_DIR'], app.config['UPLOADED_LOGOS_DEST']),
        logoname
        )

@company_bp.route("/<int:company_id>/buses", methods=["GET"])
def get_company_buses(company_id):
    company = Company.query.get(company_id)
    buses = Bus.query.filter_by(company_id=company_id).all()
    create_bus_form = CreateBusForm(company=company)
    return render_template("bus/company-buses.html", buses=buses, company=company, create_bus_form=create_bus_form)

@company_bp.route("/<int:company_id>/buses/<int:bus_id>", methods=["GET"])
def get_company_bus(company_id, bus_id):
    company = Company.query.get(company_id)
    bus = Bus.query.get(bus_id)
    update_bus_layout_form = UpdateBusLayoutForm(obj=bus)
    delete_bus_form = DeleteBusForm(obj=bus)
    return render_template("bus/company-bus.html", bus=bus, company=company, update_bus_layout_form=update_bus_layout_form, delete_bus_form=delete_bus_form)


@company_bp.route("/<int:company_id>/statuses", methods=["GET"])
def get_company_statuses(company_id):
    company = Company.query.get(company_id)
    statuses = Status.query.filter_by(company_id=company_id).all()
    create_status_form = CreateStatusForm(company=company)
    return render_template("status/statuses.html", statuses=statuses, company=company, create_status_form=create_status_form)


@company_bp.route("/<int:company_id>/branches", methods=["GET"])
def get_company_branches(company_id):
    company = Company.query.get(company_id)
    branches = Branch.query.filter_by(company_id=company_id).all()
    create_branch_form = CreateBranchForm()
    return render_template("branch/branches.html", branches=branches, company=company, create_branch_form=create_branch_form)


@company_bp.route("/bookings", methods=["GET"])
def get_company_bookings(bus_id):
    company = get_current_branch().company
    return render_template("company/company-dashboard.html", bookings=[])



@company_bp.route("/<int:company_id>/branches/<int:branch_id>", methods=["GET"])
def get_company_branch(company_id, branch_id):
    company = Company.query.get(company_id)
    branch = Branch.query.get(branch_id)
    create_profile_form = CreateProfileForm()
    manager = branch.manager()
    
    if manager:
        code, telephone = split_telephone(manager.telephone)
        manager.telephone = telephone
        manager.telephone_code = code
    
    update_profile_form = UpdateProfileForm(obj=manager)
    delete_profile_form = DeleteProfileForm(obj=manager)
    
    return render_template("branch/branch.html", branch=branch, company=company, create_profile_form=create_profile_form, delete_profile_form=delete_profile_form, update_profile_form=update_profile_form)
