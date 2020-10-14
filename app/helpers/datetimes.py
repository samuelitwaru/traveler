import datetime
import pytz
from app import app

timezone = pytz.timezone(app.config.get("TIMEZONE"))

def now():
	return datetime.datetime.now().astimezone(timezone)