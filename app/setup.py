from celery import Celery
from flask_login import LoginManager
from app import app
from app.models import User

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(user_id)

login_manager.login_view = "index.login"


def make_celery(app):
        celery = Celery(
                app.import_name, broker=app.config['CELERY_BROKER_URL']
                )
        celery.conf.update(app.config)
        TaskBase = celery.Task
        class ContextTask(TaskBase):
                abstract = True
                def __call__(self, *args, **kwargs):
                        with app.app_context():
                                return TaskBase.__call__(self, *args, **kwargs)
        celery.Task = ContextTask
        return celery


