import os
from app import db
from app.models import User, Profile


def init_admin(first_name, last_name, email, password):
	user = User(username=email, password=password, email=email)
	profile = Profile(first_name=first_name, last_name=last_name, user=user, is_admin=True)
	db.session.add(user)
	db.session.add(profile)
	db.session.commit()


def delete_and_create_media():
	os.system('rm -rf app/models/media; mkdir app/models/media')

        
def delete_and_create_db():
        os.system('rm -rf migrations; bash drop_db.sh root bratz123 traveler;')
        db.create_all()

        
def reset():
        delete_and_create_media()
        delete_and_create_db()
        init_admin("Sam", "It", "samit@gmail.com", "123")

