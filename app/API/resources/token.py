from flask import request
from flask_restful import Resource, marshal_with
from ..fields import Fields
from app.models.models import Token, db

token_fields = Fields().token_fields()

class TokenListAPI(Resource):

    @marshal_with(token_fields)
    def get(self):
        tokens = Token.query.all()
        return tokens

    @marshal_with(token_fields)
    def post(self):
        return {}


class TokenAPI(Resource):

    @marshal_with(token_fields)
    def get(self, id):
        token = Token.query.get(id)
        return token

    @marshal_with(token_fields)
    def delete(self, id):
        token = Token.query.get(id)
        db.session.delete(token)
        db.session.commit()
        tokens = Token.query.all()
        return tokens

    @marshal_with(token_fields)
    def put(self, id):
        return {}