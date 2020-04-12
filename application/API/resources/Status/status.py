from flask import request
from flask_restful import Resource, fields, marshal_with
from application.database.models import Status, Company, db

pricing_fields = {
    "id": fields.Integer,
    "category_name": fields.String,
    "price": fields.Integer,
}

status_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "pricing": fields.Nested(pricing_fields)
}


class StatusListAPI(Resource):

    @marshal_with(status_fields)
    def get(self):
        statuses = Status.query.all()
        return statuses

    @marshal_with(status_fields)
    def post(self):
        name = request.json["name"]
        company_id = request.json["company_id"]
        company_ = Company.query.get(id=company_id)
        status = Status(name, company_)
        db.session.add(status)
        db.session.commit()
        statuses = Status.query.all()
        return statuses


class StatusAPI(Resource):

    @marshal_with(status_fields)
    def get(self, id):
        status = Status.query.get(id)
        return status

    @marshal_with(status_fields)
    def delete(self, id):
        company = Status.query.get(id)
        db.session.delete(company)
        db.session.commit()
        statuses = Status.query.all()
        return statuses

    @marshal_with(status_fields)
    def put(self, id):
        name = request.json["name"]
        status = Status.query.get(id)
        status.update(name)
        db.session.commit()
        return status
