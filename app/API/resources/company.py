from flask import request
from flask_restful import Resource, marshal_with
from ..fields import Fields
from app.models.models import Company, db

company_fields = Fields().company_fields()

class CompanyListAPI(Resource):

    @marshal_with(company_fields)
    def get(self):
        companys = Company.query.all()
        return companys

    @marshal_with(company_fields)
    def post(self):
        return {}


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
        companys = Company.query.all()
        return companys

    @marshal_with(company_fields)
    def put(self, id):
        return {}