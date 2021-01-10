import uuid
from PIL import Image
import os
import json
import urllib
import time
from datetime import timedelta
import datetime
import uuid
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import check_password_hash
import flask_sqlalchemy
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_login import current_user
from app import app
from .models import Company, Status, Grid, User, Token, Payment, Bus, Journey, db
from .helpers import now


logos = UploadSet('logos', IMAGES)

configure_uploads(app, (logos,))

def crop_image(image_path, crop_path, x,y,w,h):
	im = Image.open(image_path)
	im1 = im.crop((x, y, x+w, y+h))
	im1 = im1.resize(size=(200,200)) 
	im1.save(crop_path)


def save_logo(logo, x, y, w, h):
	# give image a name
	split = logo.filename.split('.')
	ext = split[-1]
	filename = f"{str(uuid.uuid1().int)}.{ext}"
	# save original the image
	origianl_filename = logos.save(logo, name=f'tmp_{filename}')
	# crop and save original saved image
	crop_image(f"{app.config['UPLOADED_LOGOS_DEST']}{origianl_filename}", f"{app.config['UPLOADED_LOGOS_DEST']}{filename}", x, y, w, h)
	# delete original image
	os.remove(f"{app.config['UPLOADED_LOGOS_DEST']}tmp_{filename}")
	# return logo name
	return filename


def authenticate_user(username, password):
	user = User.query.filter_by(username=username).first()
	if user and user.password and check_password_hash(user.password, password):
		return user
	return None
	


def create_user_token(user, token_period=3600):
	s = Serializer(app.config['SECRET_KEY'], expires_in=token_period)
	token = s.dumps({ 'confirm': 23 }).decode()
	expiry = now() + timedelta(seconds=token_period)
	token = Token(token=token, expiry=expiry)
	token.user = user
	db.session.add(token)


def create_default_status(company):
	status = Status(name="Ordinary", default=True, company=company)
	db.session.add(status)


def set_bus_layout(bus, columns, rows):
	count = columns * rows
	db.session.add_all([ Grid(index=i, grid_type=0, bus=bus) for i in range(count) ])

def set_bus_grids_from_layout(bus, layout):
	index = 0
	for item in layout:
		grid = Grid(index=index, grid_type=item["grid_type"], number=item["number"], label=item["label"], bus=bus)
		db.session.add(grid)
		index += 1
	db.session.commit()

def change_bus_layout(bus, layout):
	new_grid_ids = []
	for item in layout:
		grid_id = item.get("id", 0)
		grid = Grid.query.filter_by(id=grid_id, bus_id=bus.id).first() 
		if grid:
			grid.index = item["index"]
			grid.grid_type = item["grid_type"]
			grid.number = item.get("number", None)
			grid.label = item.get("number", None)
		else:
			grid = Grid(index=item["index"], grid_type=item["grid_type"], bus=bus)
			db.session.add(grid)
			db.session.commit()
		new_grid_ids.append(grid.id)

	grids_to_delete = Grid.query.filter(
				flask_sqlalchemy.sqlalchemy.not_(Grid.id.in_(new_grid_ids))
			).filter_by(bus_id=bus.id)
	
	grids_to_delete.delete(synchronize_session=False)


def find_buses(from_=None, to=None, departure_time=None, company_id=None):
	journeys_query = Journey.query
	if from_:
	    journeys_query = journeys_query.filter(Journey.from_==from_)
	if to:
	    journeys_query = journeys_query.filter(Journey.to==to)

	journeys = journeys_query.all()
	buses_query = Bus.query.filter(Bus.journey_id.in_([journey.id for journey in journeys]), Bus.booking_deadline > now())
	if departure_time:
	    departure_time_range = datetime.timedelta(days=1)
	    departure_time_upper_limit = departure_time + departure_time_range
	    departure_time_lower_limit = departure_time - departure_time_range
	    buses_query = buses_query.filter(
	        (Bus.departure_time > departure_time_lower_limit) & 
	        (Bus.departure_time < departure_time_upper_limit)
	    )
	if company_id:
	    buses_query = buses_query.filter_by(company_id=company_id)

	return buses_query.all()


def set_bus_free(bus):
	# unschedule bus
	unschedule_bus(bus)
	# update bus grid.booking_ids to None
	bus_grids_query = Grid.query.filter_by(bus_id=bus.id)
	bus_grids_query.update({"booking_id": None})


def unschedule_bus(bus):
	bus.journey_id = None
	bus.departure_time = None
	bus.booking_deadline = None
	bus.free_bus_time = None
	bus.broadcast = None
	bus.branch = None
	return bus


def get_current_branch():
	return  current_user.profile.branch


def create_payment(booking):
	grid = booking.booked_grid
	bus = grid.bus
	company = bus.company
	branch = get_current_branch()
	payment = Payment(reference=generate_reference(), amount=booking.fare, 
		method="CASH", passenger_name=booking.passenger_name, 
		passenger_telephone=booking.passenger_telephone, branch_name=branch.name,
		company_name=company.name, grid_number=grid.number, bus_number=bus.number,
		grid_id=grid.id)
	booking.payment = payment
	db.session.add(payment)


def update_payment(booking):
	payment = booking.payment
	payment.amount = booking.fare
	payment.passenger_name = booking.passenger_name
	payment.passenger_telephone = booking.passenger_telephone


def update_profile_email_and_telephone(profile, new_email, new_telephone):
	if profile.email != new_email:
		profile.email = new_email
		profile.email_valid = False
	if profile.telephone != new_telephone:
		profile.telephone = new_telephone
		profile.telephone_valid = False


def generate_reference():
	return str(uuid.uuid4())


def parse_query_string(query_string):
	result = urllib.parse.parse_qs(query_string)
	for k, v in result.items():
		if isinstance(v, list) and len(v) == 1:
			result[k] = v[0]
	return result


def parse_json_string(json_string):
	return json.loads(json_string)


def join_telephone(code, telephone, joiner="-"):
	return f"{code}{joiner}{telephone}"


def split_telephone(telephone, splitter="-"):
	return telephone.split(splitter)


def prezeros(number, length):
	if isinstance(number, int):
		nstr = str(number)
		nlen = len(nstr)
		if len(nstr) < length:
			return ('0'*(length - nlen)) + nstr
		return nstr
	raise ValueError("(number) argument must be Integer.")


def process_momo_pay(telephone, amount):
	return False