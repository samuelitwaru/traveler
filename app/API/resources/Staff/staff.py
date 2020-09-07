from flask import request
from flask_restful import Resource, fields, marshal_with
from app.models.models import Staff, User, db

user_fields = {
    "id": fields.Integer,
    "email": fields.String,
    "username": fields.String
}

staff_fields = {
    "id": fields.Integer,
    "first_name": fields.String,
    "last_name": fields.String,
    "user": fields.Nested(user_fields)
}


class StaffListAPI(Resource):

    @marshal_with(staff_fields)
    def get(self):
        admins = Staff.query.all()
        return admins

    @marshal_with(staff_fields)
    def post(self):
        first_name = request.json["first_name"]
        last_name = request.json["last_name"]
        user = request.json["user"]
        user_ = User(user["email"], user["username"], user["password"])
        db.session.add(user_)
        staff = Staff(first_name, last_name, user_)
        db.session.add(staff)
        db.session.commit()
        admins = Staff.query.all()
        return admins


class StaffAPI(Resource):

    @marshal_with(staff_fields)
    def get(self, id):
        staff = Staff.query.get(id)
        return staff

    @marshal_with(staff_fields)
    def delete(self, id):
        admin = Staff.query.get(id)
        db.session.delete(admin)
        db.session.commit()
        staff = Staff.query.all()
        return staff

    @marshal_with(staff_fields)
    def put(self, id):
        first_name = request.json["first_name"]
        last_name = request.json["last_name"]
        staff = Staff.query.get(id)
        staff.update(first_name, last_name)
        db.session.commit()
        return staff
