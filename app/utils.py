import cv2
import os
import time
from datetime import timedelta 
import uuid
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import check_password_hash
import flask_sqlalchemy
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_login import current_user
from app import app
from .models import Company, Status, Grid, User, Token, db
from .helpers import now


logos = UploadSet('logos', IMAGES)

configure_uploads(app, (logos,))

def crop_image(image_path, crop_path, x,y,w,h):
	img = cv2.imread(image_path)
	crop_img = img[int(y):int(y+h), int(x):int(x+w)]
	cv2.imwrite(crop_path, crop_img)


def save_logo(logo, x, y, w, h):
	# give image a name
	print(logo.filename)
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
			print("updated", item["index"], item["grid_type"])
			grid.index = item["index"]
			grid.grid_type = item["grid_type"]
			grid.number = item.get("number", None)
			grid.label = item.get("number", None)
		else:
			print("created", item["index"], item["grid_type"])
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

