from flask import request
from flask_restful import Resource, fields, marshal_with
from application.database.models import Admin, User, db

user_fields = {
    "id": fields.Integer,
    "email": fields.String,
    "username": fields.String
}

admin_fields = {
    "id": fields.Integer,
    "first_name": fields.String,
    "last_name": fields.String,
    "user": fields.Nested(user_fields)
}


class AdminListAPI(Resource):

    @marshal_with(admin_fields)
    def get(self):
        admins = Admin.query.all()
        return admins

    @marshal_with(admin_fields)
    def post(self):
        first_name = request.json["first_name"]
        last_name = request.json["last_name"]
        user = request.json["user"]
        user_ = User(user["email"], user["username"], user["password"])
        db.session.add(user_)
        admin = Admin(first_name, last_name, user_)
        db.session.add(admin)
        db.session.commit()
        admins = Admin.query.all()
        return admins


class AdminAPI(Resource):

    @marshal_with(admin_fields)
    def get(self, id):
        admin = Admin.query.get(id)
        return admin

    @marshal_with(admin_fields)
    def delete(self, id):
        admin = Admin.query.get(id)
        db.session.delete(admin)
        db.session.commit()
        admins = Admin.query.all()
        return admins

    @marshal_with(admin_fields)
    def put(self, id):
        first_name = request.json.get("first_name")
        last_name = request.json.get("last_name")
        admin = Admin.query.get(id)
        admin.update(first_name, last_name)
        db.session.commit()
        return admin
