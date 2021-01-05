import redis
from flask import Flask, request
from app import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_sockets import Sockets
from flask_socketio import SocketIO
from flask_mail import Mail
from rave_python import Rave


app = Flask(__name__)

app.config.from_object(config.ProductionConfig)
app.config.from_object(config.DevelopmentConfig)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
socketio = SocketIO(app)
mail = Mail(app)

sockets = Sockets(app)
redis = redis.from_url(app.config.get("REDIS_URL"))

# initialize rave
rave = Rave(app.config.get("RAVE_PUBLIC_KEY"), 
	app.config.get("RAVE_SECRET_KEY"),
	production=True,
	usingEnv=True) 


# load database models
from app.models import models

# setup
from app.setup import *

# load content processors
from app.WEB.context_processors import *

# load template filters
from app.WEB import template_filters

# load web socket namespaces
# from app.WEB_SOCKET.default import DefaultNamespace
# from app.WEB_SOCKET.mobile import MobileNamespace
# from app.WEB_SOCKET.desktop import DesktopNamespace

# socketio.on_namespace(DefaultNamespace('/'))
# socketio.on_namespace(MobileNamespace('/mobile'))
# socketio.on_namespace(DesktopNamespace('/desktop'))

# load and initialize socket backend
from app.WS.backend import socket_backend
socket_backend.start()

# load api resources
from app.API.resources.bus import BusAPI, BusListAPI
from app.API.resources.grid import GridAPI, GridListAPI
from app.API.resources.booking import BookingAPI, BookingListAPI
from app.API.resources.journey import JourneyAPI, JourneyListAPI
from app.API.resources.payment import PaymentAPI, PaymentListAPI
# from app.API.resources.passenger import PassengerAPI, PassengerListAPI
from app.API.resources.profile import ProfileAPI, ProfileListAPI
from app.API.resources.user import UserAPI, UserListAPI


api.add_resource(BusListAPI, '/bus/api/v1.0/buses', endpoint="buses")
api.add_resource(BusAPI, '/bus/api/v1.0/buses/<int:id>', endpoint="bus")

api.add_resource(GridListAPI, '/bus/api/v1.0/grids', endpoint="grids")
api.add_resource(GridAPI, '/bus/api/v1.0/grids/<int:id>', endpoint="grid")

api.add_resource(BookingListAPI, '/bus/api/v1.0/bookings', endpoint="bookings")
api.add_resource(BookingAPI, '/bus/api/v1.0/bookings/<int:id>', endpoint="booking")

api.add_resource(JourneyListAPI, '/bus/api/v1.0/journeys', endpoint="journeys")
api.add_resource(JourneyAPI, '/bus/api/v1.0/journeys/<int:id>', endpoint="journey")

api.add_resource(PaymentListAPI, '/bus/api/v1.0/payments', endpoint="payments")
api.add_resource(PaymentAPI, '/bus/api/v1.0/payments/<int:id>', endpoint="payment")

# api.add_resource(PassengerListAPI, '/bus/api/v1.0/passengers', endpoint="passengers")
# api.add_resource(PassengerAPI, '/bus/api/v1.0/passengers/<int:id>', endpoint="passenger")

api.add_resource(ProfileListAPI, '/bus/api/v1.0/profiles', endpoint="profiles")
api.add_resource(ProfileAPI, '/bus/api/v1.0/profiles/<int:id>', endpoint="profile")

api.add_resource(UserListAPI, '/bus/api/v1.0/users', endpoint="users")
api.add_resource(UserAPI, '/bus/api/v1.0/users/<int:id>', endpoint="user")


# load web app views
from app.WEB.views.index import index_bp
from app.WEB.views.auth import auth_bp
from app.WEB.views.user import user_bp
from app.WEB.views.company import company_bp
from app.WEB.views.bus import bus_bp
from app.WEB.views.status import status_bp
from app.WEB.views.branch import branch_bp
from app.WEB.views.profile import profile_bp
from app.WEB.views.journey import journey_bp
from app.WEB.views.pickup import pickup_bp
from app.WEB.views.pricing import pricing_bp
from app.WEB.views.booking import booking_bp
from app.WEB.views.payment import payment_bp


app.register_blueprint(index_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(company_bp)
app.register_blueprint(bus_bp)
app.register_blueprint(status_bp)
app.register_blueprint(branch_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(journey_bp)
app.register_blueprint(pickup_bp)
app.register_blueprint(pricing_bp)
app.register_blueprint(booking_bp)
app.register_blueprint(payment_bp)
