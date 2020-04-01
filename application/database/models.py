from application import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from datetime import datetime
from random import choice


# admin - CRUD
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    logo = db.Column(db.String(64))  # todo => storing image in flask_sqlalchemy

    branches = db.relationship("Branch", backref="company")
    payments = db.relationship("Payment", backref="company")
    buses = db.relationship("Bus", backref="company")
    statuses = db.relationship("Status", backref="company")

    def __init__(self, name, logo):
        self.name = name
        self.logo = logo

    def update(self, name, logo):
        if name: self.name = name
        if logo: self.logo = logo


class Branch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))

    staff = db.relationship("Staff", backref="branch")
    payments = db.relationship("Payment", backref="branch")
    journeys = db.relationship("Journey", backref="branch")

    def __init__(self, name, location, company_):
        self.name = name
        self.location = location
        company_.branches.append(self)

    def update(self, name, location, company_id):
        if name: self.name = name
        if location: self.location = location
        if company_id: self.company_id = company_id


class Journey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    _from = db.Column(db.String(64))
    to = db.Column(db.String(64))
    branch_id = db.Column(db.Integer, db.ForeignKey("branch.id"))

    buses = db.relationship("Bus", backref="journey")
    pickups = db.relationship("Pickup", backref="journey")
    stops = db.relationship("Stop", backref="journey")

    def __init__(self, _from, to, branch_):
        self._from = _from
        self.to = to
        branch_.journeys.append(self)

    def update(self, _from, to, branch_id):
        if _from: self._from = _from
        if to: self.to = to
        if branch_id: self.branch_id = branch_id


class Stop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    journey_id = db.Column(db.Integer, db.ForeignKey("journey.id"))

    pricing = db.relationship("Pricing", backref="stop")

    def __init__(self, name, journey_):
        self.name = name
        journey_.stops.append(self)

    def update(self, name, journey_id):
        if name: self.name = name
        if journey_id: self.journey_id = journey_id


class Pricing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    stop_id = db.Column(db.Integer, db.ForeignKey("stop.id"))
    status_id = db.Column(db.Integer, db.ForeignKey("status.id"))

    def __init__(self, price, stop_, status_):
        self.price = price
        stop_.pricing.append(self)
        status_.pricing.append(self)

    def update(self, price):
        if price: self.price = price


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))

    pricing = db.relationship("Pricing", backref="status")

    def __init__(self, name, company_):
        self.name = name
        company_.statuses.append(self)

    def update(self, name):
        if name: self.name = name


class Pickup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    journey_id = db.Column(db.Integer, db.ForeignKey("journey.id"))

    def __init__(self, name, journey_):
        self.name = name
        journey_.pickups.append(self)

    def update(self, name):
        if name: self.name = name


class Bus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(16))
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

    def update(self, number):
        if number: self.number = number


class Seat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(3))
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

    def update(self, number):
        if number: self.number = number


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(64))
    amount = db.Column(db.Integer)
    method = db.Column(db.String(64))
    time = db.Column(db.DateTime, default=datetime.utcnow)  # TODO: Find out about time zones
    app = db.Column(db.String(64))
    company_name = db.Column(db.String(64))
    branch_name = db.Column(db.String(64))
    bus_number = db.Column(db.String(16))
    seat_number = db.Column(db.String(3))
    passenger_name = db.Column(db.String(64))

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

    def update(self, amount, method, app, passenger_name):
        if amount: self.amount = amount
        if method: self.method = method
        if app: self.app = app
        if passenger_name: self.passenger_name = passenger_name


class Passenger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    email = db.Column(db.String(64))
    telephone = db.Column(db.String(12))
    password = db.Column(db.String(128))

    payments = db.relationship("Payment", backref="passenger")

    def __init__(self, first_name, last_name, email, telephone, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.telephone = telephone
        self.password = generate_password_hash(password)

    def update(self, first_name, last_name, email, telephone):
        if first_name: self.first_name = first_name
        if last_name: self.last_name = last_name
        if email: self.email = email
        if telephone: self.telephone = telephone


class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    branch_id = db.Column(db.Integer, db.ForeignKey("branch.id"))

    user = db.relationship("User", backref="staff", uselist=False)

    def __init__(self, first_name, last_name, _user):
        self.first_name = first_name
        self.last_name = last_name
        self.user = _user

    def update(self, first_name, last_name):
        if first_name: self.first_name = first_name
        if last_name: self.last_name = last_name


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))

    user = db.relationship("User", backref="admin", uselist=False)

    def __init__(self, first_name, last_name, _user):
        self.first_name = first_name
        self.last_name = last_name
        self.user = _user

    def update(self, first_name, last_name):
        if first_name: self.first_name = first_name
        if last_name: self.last_name = last_name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))
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

    def update(self, email, username):
        if email: self.email = email
        if username: self.email = username


class Connection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.String(64), primary_key=True, nullable=False)
    connect_time = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    disconnect_time = db.Column(db.DateTime)
    client_type = db.Column(db.String(32))
    client_name = db.Column(db.String(128))

    def __init__(self, sid, client_type, client_name):
        self.sid = sid
        self.client_type = client_type
        self.client_name = client_name


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
