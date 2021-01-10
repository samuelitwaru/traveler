from datetime import datetime, timedelta
import random
import json
from app.models.models import *
from app.utils import set_bus_grids_from_layout

bus_layouts_file = open("app/models/bus-layouts.json", "r")
json_string = bus_layouts_file.read()
bus_layouts = json.loads(json_string)

companies = [
	{"name": "ITWA Travelers", "logo": "ITWA.jpeg"},
	{"name": "BYENK Travelers", "logo": "BYENK.png"},
	{"name": "TAYEB Travelers", "logo": "TAYEB.jpeg"}
]

branches = [
	{"name": "Gulu", "location":"Gulu", "company_id":1}, {"name": "Kampala", "location":"Kampala", "company_id":1},
	{"name": "Fort Portal", "location":"Fort Portal", "company_id":2}, {"name": "Kampala", "location":"Kampala", "company_id":2},
	{"name": "Arua", "location":"Arua", "company_id":3}, {"name": "Kampala", "location":"Kampala", "company_id":3},
]

managers = [
	{"first_name":"Samuel", "last_name":"Itwaru", "email":"samuelitwaru@gmail.com", "telephone":"256-781902516", "branch_id":1},
	{"first_name":"Samuel", "last_name":"Itwaru", "email":"samuelitwaru2@gmail.com", "telephone":"256-781902512", "branch_id":2},
	{"first_name":"Joshua", "last_name":"Byenkya", "email":"joshuabyenkya@gmail.com", "telephone":"256-775032096", "branch_id":3},
	{"first_name":"Joshua", "last_name":"Byenkya", "email":"joshuabyenkya2@gmail.com", "telephone":"256-775032092", "branch_id":4},
	{"first_name":"Ian", "last_name":"Tayebwa", "email":"iantayebwa@gmail.com", "telephone":"256-785857000", "branch_id":5},
	{"first_name":"Ian", "last_name":"Tayebwa", "email":"iantayebwa2@gmail.com", "telephone":"256-785857002", "branch_id":6}
]

statuses = [
	{"name":"Ordinary", "default": True, "company_id":1},
	{"name":"Ordinary", "default": True, "company_id":2},
	{"name":"Ordinary", "default": True, "company_id":3},
]

journeys = [
	{"from_":"Gulu", "to":"Kampala", "distance":333.0, "duration":5, "branch_id":1, "pickups":["Terminal"], "pricings":[{"stop": "Kampala", "price":40000, "status_id":1}]},
	{"from_":"Kampala", "to":"Gulu", "distance":333.0, "duration":5, "branch_id":2, "pickups":["Terminal"],  "pricings":[{"stop": "Gulu", "price":40000, "status_id":1}]},

	{"from_":"Fort Portal", "to":"Kampala", "distance":294.0, "duration":4, "branch_id":3, "pickups":["Terminal"],  "pricings":[{"stop": "Kampala", "price":30000, "status_id":2}]},
	{"from_":"Kampala", "to":"Fort Portal", "distance":294.0, "duration":4, "branch_id":4, "pickups":["Terminal"],  "pricings":[{"stop": "Fort Portal", "price":30000, "status_id":2}]},
	
	{"from_":"Arua", "to":"Kampala", "distance":498.0, "duration":7, "branch_id":5, "pickups":["Terminal"],  "pricings":[{"stop": "Kampala", "price":50000, "status_id":3}]},
	{"from_":"Kampala", "to":"Arua", "distance":498.0, "duration":7, "branch_id":6, "pickups":["Terminal"],  "pricings":[{"stop": "Arua", "price":50000, "status_id":3}]},
]


buses = [
	{"number": "ITWA 001", "columns":3, "rows":5, "status_id":1, "journey_id":1, "company_id":1, "branch_id":1},
	{"number": "ITWA 002", "columns":3, "rows":5, "status_id":1, "journey_id":1, "company_id":1, "branch_id":1},
	{"number": "ITWA 003", "columns":3, "rows":5, "status_id":1, "journey_id":2, "company_id":1, "branch_id":2},
	{"number": "ITWA 004", "columns":3, "rows":5, "status_id":1, "journey_id":2, "company_id":1, "branch_id":2},

	{"number": "BYENK 001", "columns":3, "rows":5, "status_id":2, "journey_id":3, "company_id":2, "branch_id":3},
	{"number": "BYENK 002", "columns":3, "rows":5, "status_id":2, "journey_id":3, "company_id":2, "branch_id":3},
	{"number": "BYENK 003", "columns":3, "rows":5, "status_id":2, "journey_id":4, "company_id":2, "branch_id":4},
	{"number": "BYENK 004", "columns":3, "rows":5, "status_id":2, "journey_id":4, "company_id":2, "branch_id":4},


	{"number": "TAYEB 001", "columns":3, "rows":5, "status_id":3, "journey_id":5, "company_id":3, "branch_id":5},
	{"number": "TAYEB 002", "columns":3, "rows":5, "status_id":3, "journey_id":5, "company_id":3, "branch_id":5},
	{"number": "TAYEB 003", "columns":3, "rows":5, "status_id":3, "journey_id":6, "company_id":3, "branch_id":6},
	{"number": "TAYEB 004", "columns":3, "rows":5, "status_id":3, "journey_id":6, "company_id":3, "branch_id":6},	
]


def create_companies():
	for each in companies:
		company = Company(name=each["name"], logo=each["logo"])
		db.session.add(company)
		# save logo in media folder
	db.session.commit()

def create_branches():
	for each in branches:
		branch = Branch(name=each["name"], location=each["location"], company_id=each["company_id"])
		db.session.add(branch)
	db.session.commit()

def create_managers():
	for each in managers:
		user = User(username=each["email"], password="123")
		profile = Profile(first_name=each["first_name"], last_name=each["last_name"], telephone=each["telephone"], user=user, email=each["email"], is_manager=True, branch_id=each["branch_id"])
		db.session.add(user)
		db.session.add(profile)
	db.session.commit()

def create_statuses():
	for each in statuses:
		status = Status(name=each["name"], default=each["default"], company_id=each["company_id"])
		db.session.add(status)
	db.session.commit()

def create_journeys():
	for each in journeys:
		journey = Journey(from_=each["from_"], to=each["to"], distance=each["distance"], duration=each["duration"], branch_id=each["branch_id"])
		db.session.add(journey)
		for each2 in each["pricings"]:
			pricing = Pricing(stop=each2["stop"], price=each2["price"], status_id=each2["status_id"], journey=journey)
			db.session.add(pricing)
		for pickup in each["pickups"]:
			pickup = Pickup(name=pickup, journey=journey)
			db.session.add(pickup)
	db.session.commit()


def create_buses():
	choices = range(1, 5)
	now = datetime.now()
	for each in buses:
		then = now + timedelta(random.choice(choices))
		bus = Bus(number=each["number"], columns=each["columns"], rows=each["rows"], broadcast=True, 
			departure_time=then, booking_deadline=(then-timedelta(minutes=30)), free_bus_time=(then+timedelta(minutes=30)), 
			company_id=each["company_id"], status_id=each["status_id"], journey_id=each["journey_id"], branch_id=each["branch_id"])
		db.session.add(bus)
		set_bus_grids_from_layout(bus, bus_layouts.get('A'))
		db.session.commit()




def main():
	create_companies()
	create_branches()
	create_managers()
	create_statuses()
	create_journeys()
	create_buses()