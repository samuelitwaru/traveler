from flask import Blueprint, render_template, url_for, request, redirect, flash
from application.database.models import Company, db
from application.utilities import crop_image

company_bp = Blueprint('company_bp', __name__, url_prefix="/companies")


# COMPANY
@company_bp.route("/", methods=["GET"])
def get_companies():
    companies = Company.query.all()
    return render_template("transport-companies.html", companies=companies)


@company_bp.route("/add", methods=["GET", "POST"])
def add_company():
    if request.method == "GET":
        return render_template("add-transport-company.html")
    elif request.method == "POST":
        # get values
        name = request.form.get("company")
        logo = request.files.get("logo")
        h = request.form.get("h")
        w = request.form.get("w")
        x = request.form.get("x")
        y = request.form.get("y")
        # add company
        company = Company(name, "1.png")
        db.session.add(company)
        db.session.commit()

        #  save image
        logo.save("application/database/media/1.png")
        crop_image("application/database/media/1.png", "application/database/media/cropped/1.png", round(float(x)), round(float(y)), round(float(w)), round(float(h)))
        return redirect(url_for('company_bp.get_companies'))
    

@company_bp.route("/<company_id>", methods=["GET", "POST"])
def get_company(company_id):
    company = Company.query.get(id)
    return render_template("transport-company.html", company=company)


# STATUS
@company_bp.route("/<company_id>/statuses", methods=["GET"])
def get_company_statuses(company_id):
    pass


@company_bp.route("/<company_id>/statuses/add", methods=["POST"])
def add_company_status(company_id):
    pass


@company_bp.route("/<company_id>/statuses/delete/<status_id>", methods=["DELETE"])
def delete_company_status(company_id, status_id):
    pass


# BUS
@company_bp.route("/<company_id>/buses", methods=["GET"])
def get_company_buses(company_id):
    pass


@company_bp.route("/<company_id>/buses/add", methods=["POST"])
def add_company_bus(company_id):
    pass


@company_bp.route("/<company_id>/buses/<bus_id>", methods=["GET", "PUT"])
def update_company_bus(company_id, bus_id):
    pass


# JOURNEY
@company_bp.route("/<company_id>/journeys", methods=["GET"])
def get_company_journeys(company_id):
    pass


@company_bp.route("/<company_id>/journeys/add", methods=["POST"])
def add_company_journey(company_id):
    pass


@company_bp.route("/<company_id>/journeys/delete/<journey_id>", methods=["POST"])
def delete_company_journey(company_id, journey_id):
    pass


# PRICING
@company_bp.route("/<company_id>/journeys/<journey_id>/pricing", methods=["GET"])
def get_journey_pricing(company_id, journey_id):
    pass


@company_bp.route("/<company_id>/journeys/<journey_id>/pricing/add", methods=["POST"])
def add_journey_pricing(company_id, journey_id):
    pass


@company_bp.route("/<company_id>/journeys/<journey_id>/pricing/delete/<pricing_id>", methods=["DELETE"])
def delete_journey_pricing(company_id, journey_id, pricing_id):
    pass


# PICKUP
@company_bp.route("/<company_id>/journeys/<journey_id>/pickups", methods=["GET"])
def get_journey_pickups(company_id, journey_id):
    pass


@company_bp.route("/<company_id>/journeys/<journey_id>/pickup/add", methods=["POST"])
def add_journey_pickup(company_id, journey_id):
    pass


@company_bp.route("/<company_id>/journeys/<journey_id>/pickup/delete/<pickup_id>", methods=["DELETE"])
def delete_journey_pickup(company_id, journey_id, pickup_id):
    pass




