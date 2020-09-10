from flask import request
from flask_restful import Resource, marshal_with
from ..fields import Fields
from app.models.models import Profile, db

profile_fields = Fields().profile_fields()

class ProfileListAPI(Resource):

    @marshal_with(profile_fields)
    def get(self):
        profiles = Profile.query.all()
        return profiles

    @marshal_with(profile_fields)
    def post(self):
        return {}


class ProfileAPI(Resource):

    @marshal_with(profile_fields)
    def get(self, id):
        profile = Profile.query.get(id)
        return profile

    @marshal_with(profile_fields)
    def delete(self, id):
        profile = Profile.query.get(id)
        db.session.delete(profile)
        db.session.commit()
        profiles = Profile.query.all()
        return profiles

    @marshal_with(profile_fields)
    def put(self, id):
        return {}