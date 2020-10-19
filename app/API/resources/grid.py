from flask import request
from flask_restful import Resource, marshal_with, reqparse
from ..fields import Fields
from app.models.models import Grid, db

grid_fields = Fields().grid_fields()

class GridListAPI(Resource):

    get_grids_parser = reqparse.RequestParser()

    def __init__(self):
        self.get_grids_parser.add_argument("bus_id", type=int, help="Invalid bus_id", location="args")

    @marshal_with(grid_fields)
    def get(self):
        args = self.get_grids_parser.parse_args()
        bus_id = args.get("bus_id")
        grids_query = Grid.query
        if bus_id:
            grids_query = grids_query.filter_by(bus_id=bus_id)
        grids = grids_query.all()
        return grids


class GridAPI(Resource):

    @marshal_with(grid_fields)
    def get(self, id):
        grid = Grid.query.get(id)
        return grid