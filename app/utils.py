import uuid
from PIL import Image
import os
import json
import urllib
import time
from datetime import timedelta 
import uuid
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import check_password_hash
import flask_sqlalchemy
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_login import current_user
from app import app
from .models import Company, Status, Grid, User, Token, Payment, db
from .helpers import now


logos = UploadSet('logos', IMAGES)

configure_uploads(app, (logos,))

def crop_image(image_path, crop_path, x,y,w,h):
	im = Image.open(image_path)
	im1 = im.crop((x, y, x+w, y+h)) 
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


def generate_reference():
	return str(uuid.uuid4())


def parse_query_string(query_string):
	result = urllib.parse.parse_qs(query_string)
	for k, v in result.items():
		if isinstance(v, list) and len(v) == 1:
			result[k] = v[0]
	return result


def join_telephone(code, telephone):
	return f"{code}-{telephone}"


def split_telephone(telephone):
	return telephone.split("-")


