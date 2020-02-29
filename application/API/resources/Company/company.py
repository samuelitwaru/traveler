from flask import request
from flask_restful import Resource, fields, marshal_with
from application.database.models import Company, db

branch_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "location": fields.String,
}

payment_fields = {
    "id": fields.Integer,
    "reference": fields.String,
    "amount": fields.Integer,
    "method": fields.String,
    "time": fields.DateTime,
    "app": fields.String,
    "company_name": fields.String,
    "branch_name": fields.String,
    "bus_number": fields.String,
    "passenger_name": fields.String
}

bus_fields = {
    "id": fields.Integer,
    "number": fields.String,
    "columns": fields.Integer,
    "departure_time": fields.DateTime,
}

company_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "logo": fields.String,
    "branches": fields.Nested(branch_fields),
    "payments": fields.Nested(payment_fields),
    "buses": fields.Nested(bus_fields)
}


class CompanyListAPI(Resource):

    @marshal_with(company_fields)
    def get(self):
        companies = Company.query.all()
        return companies

    @marshal_with(company_fields)
    def post(self):
        name = request.json["name"]
        logo = request.json["logo"]  # TODO: GET FILE
        company = Company(name, logo)
        db.session.add(company)
        db.session.commit()
        companies = Company.query.all()
        return companies


class CompanyAPI(Resource):

    @marshal_with(company_fields)
    def get(self, id):
        company = Company.query.get(id)
        return company

    @marshal_with(company_fields)
    def delete(self, id):
        company = Company.query.get(id)
        db.session.delete(company)
        db.session.commit()
        companies = Company.query.all()
        return companies

    def put(self, id):  # TODO: See how put requests are done ie, dealing with update of specific columns
        pass
