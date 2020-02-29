from application import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from datetime import datetime
from random import choice


# admin - CRUD
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    logo = db.Column(db.String)  # todo => storing image in flask_sqlalchemy

    branches = db.relationship("Branch", backref="company")
    payments = db.relationship("Payment", backref="company")
    buses = db.relationship("Buses", backref="company")

    def __init__(self, name, logo):
        self.name = name
        self.logo = logo


class Branch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    location = db.Column(db.String)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))

    staff = db.relationship("Staff", backref="branch")
    payments = db.relationship("Payment", backref="branch")
    journeys = db.relationship("Journey", backref="branch")

    def __init__(self, name, location, company_):
        self.name = name
        self.location = location
        company_.branches.append(self)


class Journey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    _from = db.Column(db.String)
    to = db.Column(db.String)
    branch_id = db.Column(db.Integer, db.ForeignKey("branch.id"))

    buses = db.relationship("Bus", backref="journey")
    pickups = db.relationship("Pickup", backref="journey")
    stops = db.relationship("Stop", backref="journey")

    def __init__(self, _from, to, branch_):
        self._from = _from
        self.to = to
        branch_.journeys.append(self)


class Stop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    journey_id = db.Column(db.Integer, db.ForeignKey("journey.id"))

    pricing = db.relationship("Pricing", backref="stop")

    def __init__(self, name):
        self.name = name


class Pricing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status_id = db.Column(db.Integer, db.ForeignKey("status.id"))
    price = db.Column(db.Integer)

    def __init__(self, price, status_):
        self.price = price
        status_.pricing.append(self)


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    pricing = db.relationship("Pricing", backref="status")

    def __init__(self, name):
        self.name = name


class Pickup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    journey_id = db.Column(db.Integer, db.ForeignKey("journey.id"))

    def __init__(self, name, journey_):
        self.name = name
        journey_.pickups.append(self)


class Bus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String)
    columns = db.Column(db.Integer)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))
    departure_time = db.Column(db.DateTime)  # nullable
    journey_id = db.Column(db.Integer, db.ForeignKey("journey.id"))  # nullable

    seats = db.relationship("Seat", backref="bus")
    payments = db.relationship("Payment", backref="payments")

    def __init__(self, number, columns, company_):
        self.number = number
        self.columns = columns
        company_.buses.append(self)


class Seat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String)
    grid_x = db.Column(db.Integer)
    grid_y = db.Column(db.Integer)
    bus_id = db.Column(db.Integer, db.ForeignKey("bus.id"))
    booked = db.Column(db.Boolean, default=False)
    payment_id = db.Column(db.Integer, db.ForeignKey("payment.id"))  # nullable

    def __init__(self, number, grid_x, grid_y, bus_):
        self.number = number
        self.grid_x = grid_x
        self.grid_y = grid_y
        bus_.seats.append(self)


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String)
    amount = db.Column(db.Integer)
    method = db.Column(db.String)
    time = db.Column(db.DateTime, default=datetime.utcnow)  # TODO: Find out about time zones
    app = db.Column(db.String)
    company_name = db.Column(db.String)
    branch_name = db.Column(db.String)
    bus_number = db.Column(db.String)
    seat_number = db.Column(db.String)
    passenger_name = db.Column(db.String)

    seat_id = db.Column(db.Integer, db.ForeignKey("seat.id"))
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))
    branch_id = db.Column(db.Integer, db.ForeignKey("branch.id"))
    bus_id = db.Column(db.Integer, db.ForeignKey("bus.id"))
    passenger_id = db.Column(db.Integer, db.ForeignKey("passenger.id"))  # nullable

    def __init__(self, amount, method, app, passenger_name, seat_, company_, branch_, bus_):
        self.amount = amount
        self.method = method
        self.app = app
        self.passenger_name = passenger_name
        seat_.payments.append(self)
        company_.payments.append(self)
        branch_.payments.append(self)
        bus_.payments.append(self)
        self.company_name = company_.name
        self.branch_name = branch_.name
        self.bus_number = bus_.number
        self.seat_number = seat_.number
        self.reference = "-".join([self.company_name, self.branch_name, self.bus_number, self.seat_number, str(choice(range(100, 999)))]).replace(" ", "").upper()


class Passenger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    telephone = db.Column(db.String)
    password = db.Column(db.String)

    payments = db.relationship("Payment", backref="passenger")

    def __init__(self, first_name, last_name, email, telephone, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.telephone = telephone
        self.password = generate_password_hash(password)


class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    branch_id = db.Column(db.Integer, db.ForeignKey("branch.id"))

    user = db.relationship("User", backref="staff", uselist=True)

    def __init__(self, first_name, last_name, _user):
        self.first_name = first_name
        self.last_name = last_name


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)

    user = db.relationship("User", backref="admin", uselist=False)

    def __init__(self, first_name, last_name, _user):
        self.first_name = first_name
        self.last_name = last_name
        self.user = _user


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    staff_id = db.Column(db.Integer, db.ForeignKey("staff.id"))
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"))

    def __init__(self, email, username, password, **profiles):
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)
        if profiles.get("staff_"):
            self.staff = profiles.get("staff_")
        elif profiles.get("admin_"):
            self.admin = profiles.get("admin_")


# DESKTOP USER
# - add/delete/update bus {add:[], delete:[], update:[]}
# - add/delete/update bus schedule {add:[], delete:[], update:[]}
# - add/delete/update journey {add:[], delete:[], update:[]}
# - add/delete/update staff {add:[], delete:[], update:[]}
# - add/delete/update user {add:[], delete:[], update:[]}
# - update seat {add:[], delete:[], update:[]}
# - update payment {add:[], delete:[], update:[]}


# MOBILE USER
# - update seat {add:[], delete:[], update:[]}
# - update payment {add:[], delete:[], update:[]}
# - update passenger {add:[], delete:[], update:[]}


# ADMIN USER
# - add/delete/update company {add:[], delete:[], update:[]}
# - add/delete/update branch {add:[], delete:[], update:[]}
# - add/delete/update admin {add:[], delete:[], update:[]}
