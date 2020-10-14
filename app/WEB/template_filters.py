from jinja2 import filters
from app import app


def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
	return value.strftime(format)


def currency(value):
	if isinstance(value, int):
		return f'{value:,} {app.config.get("DEFAULT_CURRENCY", "")}'
	return value





filters.FILTERS['datetimeformat'] = datetimeformat
filters.FILTERS['currency'] = currency
