from flask import request
from flask_restful import Resource, marshal_with
from ..fields import Fields
from app.models.models import Grid, db

grid_fields = Fields().grid_fields()

class GridListAPI(Resource):

    @marshal_with(grid_fields)
    def get(self):
        grids = Grid.query.all()
        return grids

    @marshal_with(grid_fields)
    def post(self):
        return {}


class GridAPI(Resource):

    @marshal_with(grid_fields)
    def get(self, id):
        grid = Grid.query.get(id)
        return grid

    @marshal_with(grid_fields)
    def delete(self, id):
        grid = Grid.query.get(id)
        db.session.delete(grid)
        db.session.commit()
        grids = Grid.query.all()
        return grids

    @marshal_with(grid_fields)
    def put(self, id):
        return {}