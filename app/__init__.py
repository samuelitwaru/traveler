from flask import Flask, request
from app import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_socketio import SocketIO

app = Flask(__name__)

app.config.from_object(config.DevelopmentConfig)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
socketio = SocketIO(app)


# load database models
from app.models import models

# setup
from app.setup import *

# load content processors
from app.WEB.context_processors import *

# load api resources
# from app.API.resources.Company.company import CompanyAPI, CompanyListAPI
# from app.API.resources.Branch.branch import BranchAPI, BranchListAPI

# from app.API.resources.Bus.bus import BusAPI, BusListAPI
# from app.API.resources.Grid.grid import GridAPI, GridListAPI

# from app.API.resources.Passenger.passenger import PassengerAPI, PassengerListAPI
# from app.API.resources.Payment.payment import PaymentAPI, PaymentListAPI

# from app.API.resources.Journey.journey import JourneyAPI, JourneyListAPI
# from app.API.resources.Pickup.pickup import PickupAPI, PickupListAPI
# from app.API.resources.Status.status import StatusAPI, StatusListAPI
# from app.API.resources.Stop.stop import StopAPI, StopListAPI
# from app.API.resources.Pricing.pricing import PricingAPI, PricingListAPI

# from app.API.resources.User.user import UserAPI, UserListAPI
# from app.API.resources.Staff.staff import StaffAPI, StaffListAPI
# from app.API.resources.Admin.admin import AdminAPI, AdminListAPI

# api.add_resource(CompanyListAPI, '/bus/api/v1.0/companies', endpoint="companies")
# api.add_resource(CompanyAPI, '/bus/api/v1.0/companies/<int:id>', endpoint="company")

# api.add_resource(BranchListAPI, '/bus/api/v1.0/branches', endpoint="branches")
# api.add_resource(BranchAPI, '/bus/api/v1.0/branches/<int:id>', endpoint="branch")

# api.add_resource(BusListAPI, '/bus/api/v1.0/buses', endpoint="buses")
# api.add_resource(BusAPI, '/bus/api/v1.0/buses/<int:id>', endpoint="bus")

# api.add_resource(GridListAPI, '/bus/api/v1.0/grids', endpoint="grids")
# api.add_resource(GridAPI, '/bus/api/v1.0/grids/<int:id>', endpoint="grid")

# api.add_resource(PassengerListAPI, '/bus/api/v1.0/passengers', endpoint="passengers")
# api.add_resource(PassengerAPI, '/bus/api/v1.0/passengers/<int:id>', endpoint="passenger")

# api.add_resource(PaymentListAPI, '/bus/api/v1.0/payments', endpoint="payments")
# api.add_resource(PaymentAPI, '/bus/api/v1.0/payments/<int:id>', endpoint="payment")

# api.add_resource(JourneyListAPI, '/bus/api/v1.0/journeys', endpoint="journeys")
# api.add_resource(JourneyAPI, '/bus/api/v1.0/journeys/<int:id>', endpoint="journey")

# api.add_resource(PickupListAPI, '/bus/api/v1.0/pickups', endpoint="pickups")
# api.add_resource(PickupAPI, '/bus/api/v1.0/pickups/<int:id>', endpoint="pickup")

# api.add_resource(StatusListAPI, '/bus/api/v1.0/status', endpoint="statuses")
# api.add_resource(StatusAPI, '/bus/api/v1.0/status/<int:id>', endpoint="status")

# api.add_resource(StopListAPI, '/bus/api/v1.0/stops', endpoint="stops")
# api.add_resource(StopAPI, '/bus/api/v1.0/stops/<int:id>', endpoint="stop")

# api.add_resource(PricingListAPI, '/bus/api/v1.0/pricing', endpoint="pricing_list")
# api.add_resource(PricingAPI, '/bus/api/v1.0/pricing/<int:id>', endpoint="pricing")

# api.add_resource(UserListAPI, '/bus/api/v1.0/users', endpoint="users")
# api.add_resource(UserAPI, '/bus/api/v1.0/users/<int:id>', endpoint="user")

# api.add_resource(StaffListAPI, '/bus/api/v1.0/staff', endpoint="staff_list")
# api.add_resource(StaffAPI, '/bus/api/v1.0/staff/<int:id>', endpoint="staff")

# api.add_resource(AdminListAPI, '/bus/api/v1.0/admins', endpoint="admins")
# api.add_resource(AdminAPI, '/bus/api/v1.0/admins/<int:id>', endpoint="admin")


# load web socket namespaces
# from app.API.web_socket.default import DefaultNamespace
# from app.API.web_socket.mobile import MobileNamespace
# from app.API.web_socket.desktop import DesktopNamespace

# socketio.on_namespace(DefaultNamespace('/'))
# socketio.on_namespace(MobileNamespace('/mobile'))
# socketio.on_namespace(DesktopNamespace('/desktop'))


# load web app views
from app.WEB.views.index import index_bp
from app.WEB.views.auth import auth_bp
from app.WEB.views.company import company_bp
from app.WEB.views.bus import bus_bp
from app.WEB.views.status import status_bp
from app.WEB.views.branch import branch_bp
from app.WEB.views.profile import profile_bp
from app.WEB.views.journey import journey_bp
from app.WEB.views.pickup import pickup_bp
from app.WEB.views.pricing import pricing_bp
from app.WEB.views.booking import booking_bp

app.register_blueprint(index_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(company_bp)
app.register_blueprint(bus_bp)
app.register_blueprint(status_bp)
app.register_blueprint(branch_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(journey_bp)
app.register_blueprint(pickup_bp)
app.register_blueprint(pricing_bp)
app.register_blueprint(booking_bp)
