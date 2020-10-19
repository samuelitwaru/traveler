from flask import request
from flask_restful import Resource, marshal_with, reqparse
from ..fields import Fields
from app.models.models import User, db
from app.utils import authenticate_user

user_fields = Fields().user_fields()

class UserListAPI(Resource):
    auth_user_parser = reqparse.RequestParser()

    def __init__(self):
        self.auth_user_parser.add_argument('username', type=str, help='Invalid username', location="json", required=True)
        self.auth_user_parser.add_argument('password', type=str, help='Invalid password', location="json", required=True)
    
    @marshal_with(user_fields)
    def get(self):
        users = User.query.all()
        return users

    @marshal_with(user_fields)
    def post(self):
        args = self.auth_user_parser.parse_args()
        username = args.get("username")
        password = args.get("password")
        user = authenticate_user(username, password)
        if user:
            return user
        return None


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