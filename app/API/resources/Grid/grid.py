from flask import request
from flask_restful import Resource, fields, marshal_with
from app.models.models import Grid, Bus, db


bus_fields = {
    "id": fields.Integer,
    "number": fields.String,
    "columns": fields.Integer,
}

payment_fields = {
    "id": fields.Integer,
    "reference": fields.String,
    "amount": fields.Integer,
    "method": fields.String,
    "time": fields.DateTime,
    "app": fields.String,
    "company_name": fields.String,
    "branch_name": fields.String,
    "bus_number": fields.String,
    "passenger_name": fields.String
}

grid_fields = {
    "id": fields.Integer,
    "index": fields.Integer,
    "grid_type": fields.Integer,
    "number": fields.String,
    "label": fields.String,
    "booked": fields.Boolean,
    "payment": fields.Nested(payment_fields),
    "bus": fields.Nested(bus_fields)
}


class GridListAPI(Resource):

    @marshal_with(grid_fields)
    def get(self):
        grids = Grid.query.all()
        return grids

    @marshal_with(grid_fields)
    def post(self):
        index = request.json.get("index")
        grid_type = request.json.get("grid_type")
        number = request.json.get("number")
        label = request.json.get("label")
        bus_id = request.json.get("bus_id")
        bus_ = Bus.query.get(bus_id)
        grid = Grid(index, grid_type, bus_, number, label)
        db.session.add(grid)
        db.session.commit()
        grid = Grid.query.all()
        return grid


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
        grid_type = request.json.get("grid_type")
        number = request.json.get("number")
        label = request.json.get("label")
        grid = Grid.query.get(id)
        grid.update(grid_type, number, label)
        db.session.commit()
        return grid

