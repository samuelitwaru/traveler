import json
from random import choice
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from flask_sqlalchemy import Model
from sqlalchemy import Column, DateTime
from app import app, db
from app.helpers import timezone, now
from app.WEB.template_filters import currency


class TimestampedModel(Model):
    created_at = Column(DateTime, default=now())
    updated_at = Column(DateTime)


# admin - CRUD
class Company(db.Model, TimestampedModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    logo = db.Column(db.String(64))

    branches = db.relationship("Branch", backref="company")
    buses = db.relationship("Bus", backref="company")
    statuses = db.relationship("Status", backref="company")
    payments = db.relationship("Payment", backref="company")


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
    bookings = db.relationship("Booking", backref="branch")

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
    payments = db.relationship("Payment", backref="journey")

    def __str__(self):
        return f"{self.from_} to {self.to}"


class Pricing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stop = db.Column(db.String(64))
    price = db.Column(db.Integer)
    status_id = db.Column(db.Integer, db.ForeignKey("status.id"))
    journey_id = db.Column(db.Integer, db.ForeignKey("journey.id"))

    payments = db.relationship("Payment", backref="pricing")


    def __str__(self):
        return f"{self.stop} ({currency(self.price)})"

    def app_pricing_string(self):
        charge = app.config.get("APP_CHARGE")
        return f"{self.stop} | {currency(self.price + round(self.price*charge))}"



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

    grids = db.relationship("Grid", backref="bus", cascade="delete", lazy="dynamic")
    bookings = db.relationship("Booking", backref="bus")
    payments = db.relationship("Payment", backref="bus")    

    def __str__(self):
        return self.number

    def grids_dict(self):
        grids = [grid.grid_dict() for grid in self.grids]
        return json.dumps(grids).replace('"', '')

    def seats(self):
        return list(filter(lambda grid:grid.grid_type==1, self.grids))

    def booked_seats(self):
        return list(filter(lambda grid:(grid.grid_type==1 and grid.booking_id), self.grids))

    def unbooked_seats(self):
        return list(filter(lambda grid:(grid.grid_type==1 and grid.booking_id==None), self.grids))

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
    bus_id = db.Column(db.Integer, db.ForeignKey("bus.id", ondelete='CASCADE'), nullable=False)

    bookings = db.relationship("Booking", backref="grid", foreign_keys=booking_id, uselist=True, lazy='dynamic')
    booking = db.relationship("Booking", backref=db.backref("booked_grid", uselist=False), foreign_keys=booking_id)
    payments = db.relationship("Payment", backref="grid")

    def __str__(self):
        return str(self.number)

    def grid_dict(self):
        return {"id":self.id, "index":self.index, "grid_type":self.grid_type, "number":self.number, "label":self.label, "booking_id":self.booking_id,"booked":bool(self.booking)}


class Booking(db.Model, TimestampedModel):
    id = db.Column(db.Integer, primary_key=True)
    passenger_name = db.Column(db.String(128), nullable=False)
    passenger_telephone = db.Column(db.String(16))
    seat_number = db.Column(db.String(3))
    pickup = db.Column(db.String(64), nullable=False)
    stop = db.Column(db.String(64), nullable=False)
    fare = db.Column(db.Integer, nullable=False)
    paid = db.Column(db.Boolean, nullable=False)

    branch_id = db.Column(db.Integer, db.ForeignKey("branch.id"), nullable=False)
    bus_id = db.Column(db.Integer, db.ForeignKey("bus.id"), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"))


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
    passenger_email = db.Column(db.String(64))
    passenger_telephone = db.Column(db.String(16))

    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))
    bus_id = db.Column(db.Integer, db.ForeignKey("bus.id"))
    grid_id = db.Column(db.Integer, db.ForeignKey("grid.id"))
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))
    journey_id = db.Column(db.Integer, db.ForeignKey("journey.id"))
    pricing_id = db.Column(db.Integer, db.ForeignKey("pricing.id"))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))
    recovery_password = db.Column(db.String(128))
    is_active = db.Column(db.Boolean, default=True)

    profile = db.relationship("Profile", backref="user", cascade="delete", uselist=False)
    token = db.relationship("Token", backref="user", cascade="delete", uselist=False)
    bookings_created = db.relationship("Booking", backref="creator")

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
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    telephone = db.Column(db.String(16), nullable=False)
    email_valid = db.Column(db.Boolean, default=False)
    telephone_valid = db.Column(db.Boolean, default=False)
    credit = db.Column(db.Float, default=0.0)
    is_admin = db.Column(db.Boolean())
    is_manager = db.Column(db.Boolean())
    is_cashier = db.Column(db.Boolean())
    is_passenger = db.Column(db.Boolean())
    branch_id = db.Column(db.Integer, db.ForeignKey("branch.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    payments = db.relationship("Payment", backref="profile")

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
