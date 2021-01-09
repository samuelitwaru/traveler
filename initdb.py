import os
from app import db
from app.models import User, Profile
from app.models.dummy_data import main

def init_admin(first_name, last_name, email, password):
	user = User(username=email, password=password)
	profile = Profile(first_name=first_name, last_name=last_name, telephone="256-778959343", user=user, email=email, is_admin=True)
	db.session.add(user)
	db.session.add(profile)
	db.session.commit()


def delete_and_create_media():
	os.system('rm -rf app/models/media; mkdir app/models/media')
	

def delete_and_create_db():
	os.system('rm -rf migrations; rm app/models/database.db; flask db init; flask db migrate -m "First migration"; flask db upgrade')
	db.create_all()

        
def reset():
    delete_and_create_media()
    delete_and_create_db()
    init_admin("Sam", "It", "samit@gmail.com", "123")
    main()

