from jinja2 import filters
from app import app
from datetime import datetime


def datetimeformat(value, format='%d/%m/%Y %H:%M'):
	if isinstance(value, datetime):
		return value.strftime(format)


def currency(value):
	if isinstance(value, int):
		return f'{value:,} {app.config.get("DEFAULT_CURRENCY", "")}'
	return value




filters.FILTERS['datetimeformat'] = datetimeformat
filters.FILTERS['currency'] = currency
