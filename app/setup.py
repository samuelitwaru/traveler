from flask_login import LoginManager
from app import app
from app.models import User

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(user_id)


login_manager.login_view = "index.login"