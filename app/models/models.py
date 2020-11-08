import json
from random import choice
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db
from app.helpers import timezone, now


# admin - CRUD
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    logo = db.Column(db.String(64))

    branches = db.relationship("Branch", backref="company")
    buses = db.relationship("Bus", backref="company")
    statuses = db.relationship("Status", backref="company")

    def __str__(self):
        return self.name


class Branch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))

    journeys = db.relationship("Journey", backref="branch")
    members = db.relationship("Profile", backref="branch")
    buses = db.relationship("Bus", backref="branch")

    def __init__(self, name, location, company):
        self.name = name
        self.location = location
        company.branches.append(self)

    def __str__(self):
        return self.name

    def manager(self):
        manager_filter = list(filter(lambda memeber: memeber.is_manager, self.members))
        if len(manager_filter):
            return list(manager_filter)[0]
        return None


class Journey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_ = db.Column(db.String(64))
    to = db.Column(db.String(64))
    distance = db.Column(db.Float)
    duration = db.Column(db.Float)
    branch_id = db.Column(db.Integer, db.ForeignKey("branch.id"))

    buses = db.relationship("Bus", backref="journey")
    pickups = db.relationship("Pickup", backref="journey")
    pricings = db.relationship("Pricing", backref="journey")

    def __str__(self):
        return f"{self.from_} to {self.to}"


class Pricing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stop = db.Column(db.String(64))
    price = db.Column(db.Integer)
    status_id = db.Column(db.Integer, db.ForeignKey("status.id"))
    journey_id = db.Column(db.Integer, db.ForeignKey("journey.id"))

    def __str__(self):
        return f"{self.stop} ({self.price})"


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    default = db.Column(db.Boolean, default=False)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))

    pricings = db.relationship("Pricing", backref="status")
    buses = db.relationship("Bus", backref="status")

    def __str__(self):
        return self.name


class Pickup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    journey_id = db.Column(db.Integer, db.ForeignKey("journey.id"))

    def __str__(self):
        return self.name

class Bus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(16))
    columns = db.Column(db.Integer)
    rows = db.Column(db.Integer)
    
    broadcast = db.Column(db.Boolean)
    departure_time = db.Column(db.DateTime)
    schedule_cancelled_reason = db.Column(db.String(1024))
    booking_deadline = db.Column(db.DateTime)
    free_bus_time = db.Column(db.DateTime)
    branch_id = db.Column(db.Integer, db.ForeignKey("branch.id"))
    
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))
    status_id = db.Column(db.Integer, db.ForeignKey("status.id"))
    journey_id = db.Column(db.Integer, db.ForeignKey("journey.id"))

    grids = db.relationship("Grid", backref="bus")

    def __str__(self):
        return self.number

    def grids_dict(self):
        grids = [grid.grid_dict() for grid in self.grids]
        return json.dumps(grids).replace('"', '')

    def seats(self):
        return list(filter(lambda grid:grid.grid_type==1, self.grids))

    def booking_time_expired(self):
        if self.booking_deadline.astimezone(timezone) > now():
            return False
        return True


class Grid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer, nullable=False)
    grid_type = db.Column(db.Integer, nullable=False)
    number = db.Column(db.String(3))
    label = db.Column(db.String(32))
    booking_id = db.Column(db.Integer, db.ForeignKey("booking.id")) # current_booking
    bus_id = db.Column(db.Integer, db.ForeignKey("bus.id"), nullable=False)

    bookings = db.relationship("Booking", backref="grid", foreign_keys=booking_id, uselist=True)
    booking = db.relationship("Booking", backref=db.backref("booked_grid", uselist=False), foreign_keys=booking_id)

    def __str__(self):
        return self.number

    def grid_dict(self):
        return {"id":self.id, "index":self.index, "grid_type":self.grid_type, "number":self.number, "label":self.label, "booking_id":self.booking_id,"booked":bool(self.booking)}


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    passenger_name = db.Column(db.String(128), nullable=False)
    passenger_telephone = db.Column(db.String(16))
    pickup = db.Column(db.String(64), nullable=False)
    stop = db.Column(db.String(64), nullable=False)
    fare = db.Column(db.Integer, nullable=False)
    paid = db.Column(db.Boolean, nullable=False)
    grid_id = db.Column(db.Integer, db.ForeignKey("grid.id"), nullable=False)
    pricing_id = db.Column(db.Integer, db.ForeignKey("pricing.id"), nullable=False)
    payment_id = db.Column(db.Integer, db.ForeignKey("payment.id"))
    
    payment = db.relationship("Payment", backref=db.backref("booking", uselist=False), cascade="delete")


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(64))
    amount = db.Column(db.Integer)
    method = db.Column(db.String(64))
    time = db.Column(db.DateTime, default=now())
    app = db.Column(db.String(64))
    company_name = db.Column(db.String(64))
    branch_name = db.Column(db.String(64))
    bus_number = db.Column(db.String(16))
    grid_number = db.Column(db.String(3))
    passenger_name = db.Column(db.String(64))
    passenger_telephone = db.Column(db.String(16))

    grid_id = db.Column(db.Integer, db.ForeignKey("grid.id"))
    passenger_id = db.Column(db.Integer, db.ForeignKey("passenger.id"))


class Passenger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    email = db.Column(db.String(64))
    telephone = db.Column(db.String(16))
    password = db.Column(db.String(128))

    payments = db.relationship("Payment", backref="passenger")


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))
    recovery_password = db.Column(db.String(128))

    profile = db.relationship("Profile", backref="user", cascade="delete", uselist=False)
    token = db.relationship("Token", backref="user", cascade="delete", uselist=False)

    def __init__(self, *args, **kwargs):
        self.email = kwargs.get("email")
        self.username = kwargs.get("username")
        password = kwargs.get("password")
        if password:
            self.set_password(password)

    def __str__(self):
        return self.profile.display_name()

    def set_password(self, password):
        self.password = generate_password_hash(password)


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)     
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    telephone = db.Column(db.String(16))
    is_admin = db.Column(db.Boolean())
    is_manager = db.Column(db.Boolean())
    is_cashier = db.Column(db.Boolean())
    is_passenger = db.Column(db.Boolean())
    branch_id = db.Column(db.Integer, db.ForeignKey("branch.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))

    def display_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.display_name()


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)     
    token = db.Column(db.String(256))
    expiry = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))

    def __str__(self):
        return self.token

    def is_expired(self):
        if self.expiry.replace(tzinfo=timezone) < now():
            return True
        return False

class Connection(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.String(64), nullable=False)
    connect_time = db.Column(db.DateTime, default=now(), nullable=False)
    disconnect_time = db.Column(db.DateTime)
    client_type = db.Column(db.String(32))
