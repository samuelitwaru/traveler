from flask import request
from flask_restful import Resource, fields, marshal_with
from application.database.models import User, Staff, Admin, db

staff_fields = {
    "id": fields.Integer,
    "first_name": fields.String,
    "last_name": fields.String,
}

admin_fields = {
    "id": fields.Integer,
    "first_name": fields.String,
    "last_name": fields.String,
}

user_fields = {
    "id": fields.Integer,
    "username": fields.String,
    "email": fields.String,
    "staff": fields.Nested(staff_fields),
    "admin": fields.Nested(admin_fields)
}


class UserListAPI(Resource):

    @marshal_with(user_fields)
    def get(self):
        users = User.query.all()
        return users

    @marshal_with(user_fields)
    def post(self):
        username = request.json["username"]
        email = request.json["email"]
        password = request.json["password"]
        staff_id = request.json["staff_id"]
        admin_id = request.json["admin_id"]
        staff_, admin_ = None, None
        if staff_id:
            staff_ = Staff.query.get(staff_id)
        elif admin_id:
            admin_ = Admin.query.get(admin_id)
        user = User(email, username, password, staff_=staff_, admin_=admin_)
        db.session.add(user)
        db.session.commit()
        users = User.query.all()
        return users


class UserAPI(Resource):

    @marshal_with(user_fields)
    def get(self, id):
        user = User.query.get(id)
        return user

    @marshal_with(user_fields)
    def delete(self, id):
        seat = User.query.get(id)
        db.session.delete(seat)
        db.session.commit()
        seats = User.query.all()
        return seats

    @marshal_with(user_fields)
    def put(self, id):  # TODO: See how put requests are done ie, dealing with update of specific columns
        pass
