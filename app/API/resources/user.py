from flask import request
from flask_restful import Resource, marshal_with
from ..fields import Fields
from app.models.models import User, db

user_fields = Fields().user_fields()

class UserListAPI(Resource):

    @marshal_with(user_fields)
    def get(self):
        users = User.query.all()
        return users

    @marshal_with(user_fields)
    def post(self):
        return {}


class UserAPI(Resource):

    @marshal_with(user_fields)
    def get(self, id):
        user = User.query.get(id)
        return user

    @marshal_with(user_fields)
    def delete(self, id):
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        users = User.query.all()
        return users

    @marshal_with(user_fields)
    def put(self, id):
        return {}