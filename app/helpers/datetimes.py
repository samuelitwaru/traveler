import datetime
import pytz

timezone = pytz.timezone("UTC")

def now():
	return datetime.datetime.now().astimezone(timezone)