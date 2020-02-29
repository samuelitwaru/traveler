from flask import request
from flask_restful import Resource, fields, marshal_with
from application.database.models import Branch, Company, db

company_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "logo": fields.String,
}

staff_fields = {
    "id": fields.Integer,
    "first_name": fields.String,
    "last_name": fields.String,
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

journey_fields = {
    "id": fields.Integer,
    "_from": fields.String,
    "to": fields.String
}

branch_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "location": fields.String,
    "company": fields.Nested(company_fields),
    "staff": fields.Nested(staff_fields),
    "payments": fields.Nested(payment_fields),
    "journeys": fields.Nested(journey_fields)
}


class BranchListAPI(Resource):

    @marshal_with(branch_fields)
    def get(self):
        branches = Branch.query.all()
        return branches

    @marshal_with(branch_fields)
    def post(self):
        name = request.json["name"]
        location = request.json["location"]
        company_id = request.json["company_id"]
        company_ = Company.query.get(company_id)
        branch = Branch(name, location, company_)
        db.session.add(branch)
        db.session.commit()
        branches = Branch.query.all()
        return branches


class BranchAPI(Resource):

    @marshal_with(branch_fields)
    def get(self, id):
        branch = Branch.query.get(id)
        return branch

    @marshal_with(branch_fields)
    def delete(self, id):
        branch = Branch.query.get(id)
        db.session.delete(branch)
        db.session.commit()
        branch = Branch.query.all()
        return branch

    @marshal_with(branch_fields)
    def put(self, id):  # TODO: See how put requests are done ie, dealing with update of specific columns
        pass
