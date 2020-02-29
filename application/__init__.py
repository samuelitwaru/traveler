from flask import Flask
from application import configuration
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

app = Flask(__name__)

app.config.from_object(configuration.ProductionConfig)

db = SQLAlchemy(app)
api = Api(app)

from application.database import models

from application.API.resources.Company.company import CompanyAPI, CompanyListAPI
from application.API.resources.Branch.branch import BranchAPI, BranchListAPI

from application.API.resources.Bus.bus import BusAPI, BusListAPI
from application.API.resources.Seat.seat import SeatAPI, SeatListAPI

from application.API.resources.Passenger.passenger import PassengerAPI, PassengerListAPI
from application.API.resources.Payment.payment import PaymentAPI, PaymentListAPI

from application.API.resources.Journey.journey import JourneyAPI, JourneyListAPI
from application.API.resources.Pickup.pickup import PickupAPI, PickupListAPI
from application.API.resources.Status.status import StatusAPI, StatusListAPI
from application.API.resources.Stop.stop import StopAPI, StopListAPI
from application.API.resources.Pricing.pricing import PricingAPI, PricingListAPI

from application.API.resources.User.user import UserAPI, UserListAPI
from application.API.resources.Staff.staff import StaffAPI, StaffListAPI
from application.API.resources.Admin.admin import AdminAPI, AdminListAPI

api.add_resource(CompanyListAPI, '/bus/api/v1.0/companies', endpoint="companies")
api.add_resource(CompanyAPI, '/bus/api/v1.0/companies/<int:id>', endpoint="company")

api.add_resource(BranchListAPI, '/bus/api/v1.0/branches', endpoint="branches")
api.add_resource(BranchAPI, '/bus/api/v1.0/branches/<int:id>', endpoint="branch")

api.add_resource(BusListAPI, '/bus/api/v1.0/buses', endpoint="buses")
api.add_resource(BusAPI, '/bus/api/v1.0/buses/<int:id>', endpoint="bus")

api.add_resource(SeatListAPI, '/bus/api/v1.0/seats', endpoint="seats")
api.add_resource(SeatAPI, '/bus/api/v1.0/seats/<int:id>', endpoint="seat")

api.add_resource(PassengerListAPI, '/bus/api/v1.0/passengers', endpoint="passengers")
api.add_resource(PassengerAPI, '/bus/api/v1.0/passengers/<int:id>', endpoint="passenger")

api.add_resource(PaymentListAPI, '/bus/api/v1.0/payments', endpoint="payments")
api.add_resource(PaymentAPI, '/bus/api/v1.0/payments/<int:id>', endpoint="payment")

api.add_resource(JourneyListAPI, '/bus/api/v1.0/journeys', endpoint="journeys")
api.add_resource(JourneyAPI, '/bus/api/v1.0/journeys/<int:id>', endpoint="journey")

api.add_resource(PickupListAPI, '/bus/api/v1.0/pickups', endpoint="pickups")
api.add_resource(PickupAPI, '/bus/api/v1.0/pickups/<int:id>', endpoint="pickup")

api.add_resource(StatusListAPI, '/bus/api/v1.0/status', endpoint="statuses")
api.add_resource(StatusAPI, '/bus/api/v1.0/status/<int:id>', endpoint="status")

api.add_resource(StopListAPI, '/bus/api/v1.0/stops', endpoint="stops")
api.add_resource(StopAPI, '/bus/api/v1.0/stops/<int:id>', endpoint="stop")

api.add_resource(PricingListAPI, '/bus/api/v1.0/pricing', endpoint="pricing_list")
api.add_resource(PricingAPI, '/bus/api/v1.0/pricing/<int:id>', endpoint="pricing")

api.add_resource(UserListAPI, '/bus/api/v1.0/users', endpoint="users")
api.add_resource(UserAPI, '/bus/api/v1.0/users/<int:id>', endpoint="user")

api.add_resource(StaffListAPI, '/bus/api/v1.0/staff', endpoint="staff_list")
api.add_resource(StaffAPI, '/bus/api/v1.0/staff/<int:id>', endpoint="staff")

api.add_resource(AdminListAPI, '/bus/api/v1.0/admins', endpoint="admins")
api.add_resource(AdminAPI, '/bus/api/v1.0/admins/<int:id>', endpoint="admin")
