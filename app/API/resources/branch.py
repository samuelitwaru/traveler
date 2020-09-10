from flask import request
from flask_restful import Resource, marshal_with
from ..fields import Fields
from app.models.models import Branch, db

branch_fields = Fields().branch_fields()

class BranchListAPI(Resource):

    @marshal_with(branch_fields)
    def get(self):
        branchs = Branch.query.all()
        return branchs

    @marshal_with(branch_fields)
    def post(self):
        return {}


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
        branchs = Branch.query.all()
        return branchs

    @marshal_with(branch_fields)
    def put(self, id):
        return {}