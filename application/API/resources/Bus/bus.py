from flask import request
from flask_restful import Resource, fields, marshal_with
from application.database.models import Bus, Branch, Grid, db

journey_fields = {
    "id": fields.Integer,
    "_from": fields.String,
    "to": fields.String
}

branch_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "location": fields.String,
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
    "number": fields.String,
    "grid_x": fields.Integer,
    "grid_y": fields.Integer,
    "booked": fields.Boolean,
    "payment": fields.Nested(payment_fields),
}

bus_fields = {
    "id": fields.Integer,
    "number": fields.String,
    "columns": fields.Integer,
    "departure_time": fields.DateTime,
    "journey": fields.Nested(journey_fields),
    "branch": fields.Nested(branch_fields),
    "grids": fields.Nested(grid_fields)
}


class BusListAPI(Resource):

    @marshal_with(bus_fields)
    def get(self):
        buses = Bus.query.all()
        return buses

    @marshal_with(bus_fields)
    def post(self):
        number = request.json.get("number")
        columns = request.json.get("columns")
        rows = request.json.get("rows")
        company_id = request.json.get("company_id")
        company_ = Branch.query.get(company_id)
        bus = Bus(number, columns, rows, company_)

        grids = request.json.get("grids")
        for grid in grids:
            index = grid.get("index")
            number = grid.get("number")
            label = grid.get("label")
            bus_grid = Grid(index, bus, number, label)
            db.session.add(bus_grid)

        db.session.add(bus)
        db.session.commit()
        buses = Bus.query.all()
        return buses


class BusAPI(Resource):

    @marshal_with(bus_fields)
    def get(self, id):
        bus = Bus.query.get(id)
        return bus

    @marshal_with(bus_fields)
    def delete(self, id):
        bus = Bus.query.get(id)
        db.session.delete(bus)
        db.session.commit()
        buses = Bus.query.all()
        return buses

    @marshal_with(bus_fields)
    def put(self, id):
        number = request.json.get("number")
        bus = Bus.query.get(id)
        bus.update(number)
        db.session.commit()
        return bus
