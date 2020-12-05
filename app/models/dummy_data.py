from datetime import datetime, timedelta
import random
import json
from app.models.models import *
from app.utils import set_bus_grids_from_layout

bus_layouts_file = open("app/models/bus-layouts.json", "r")
json_string = bus_layouts_file.read()
bus_layouts = json.loads(json_string)

companies = [
	{"name": "ITWA Travelers", "logo": "ITWA.png"},
	{"name": "BYENK Travelers", "logo": "BYENK.png"},
	{"name": "TAYEB Travelers", "logo": "TAYEB.png"}
]

branches = [
	{"name": "Gulu", "location":"Gulu", "company_id":1}, {"name": "Kampala", "location":"Kampala", "company_id":1},
	{"name": "Fort Portal", "location":"Fort Portal", "company_id":2}, {"name": "Kampala", "location":"Kampala", "company_id":2},
	{"name": "Arua", "location":"Arua", "company_id":3}, {"name": "Kampala", "location":"Kampala", "company_id":3},
]

statuses = [
	{"name":"Ordinary", "default": True, "company_id":1},
	{"name":"Ordinary", "default": True, "company_id":2},
	{"name":"Ordinary", "default": True, "company_id":3},
]

journeys = [
	{"from_":"Gulu", "to":"Kampala", "distance":333.0, "duration":5, "branch_id":1, "pricings":[{"stop": "Kampala", "price":40000, "status_id":1}]},
	{"from_":"Kampala", "to":"Gulu", "distance":333.0, "duration":5, "branch_id":2, "pricings":[{"stop": "Gulu", "price":40000, "status_id":1}]},

	{"from_":"Fort Portal", "to":"Kampala", "distance":294.0, "duration":4, "branch_id":3, "pricings":[{"stop": "Kampala", "price":30000, "status_id":2}]},
	{"from_":"Kampala", "to":"Fort Portal", "distance":294.0, "duration":4, "branch_id":4, "pricings":[{"stop": "Fort Portal", "price":30000, "status_id":2}]},
	
	{"from_":"Arua", "to":"Kampala", "distance":498.0, "duration":7, "branch_id":5, "pricings":[{"stop": "Kampala", "price":50000, "status_id":3}]},
	{"from_":"Kampala", "to":"Arua", "distance":498.0, "duration":7, "branch_id":6, "pricings":[{"stop": "Arua", "price":50000, "status_id":3}]},
]


buses = [
	{"number": "ITWA 001", "columns":3, "rows":5, "status_id":1, "journey_id":1, "company_id":1},
	{"number": "ITWA 002", "columns":3, "rows":5, "status_id":1, "journey_id":1, "company_id":1},
	{"number": "ITWA 003", "columns":3, "rows":5, "status_id":1, "journey_id":2, "company_id":1},
	{"number": "ITWA 004", "columns":3, "rows":5, "status_id":1, "journey_id":2, "company_id":1},

	{"number": "BYENK 001", "columns":3, "rows":5, "status_id":2, "journey_id":3, "company_id":2},
	{"number": "BYENK 002", "columns":3, "rows":5, "status_id":2, "journey_id":3, "company_id":2},
	{"number": "BYENK 003", "columns":3, "rows":5, "status_id":2, "journey_id":4, "company_id":2},
	{"number": "BYENK 004", "columns":3, "rows":5, "status_id":2, "journey_id":4, "company_id":2},


	{"number": "TAYEB 001", "columns":3, "rows":5, "status_id":3, "journey_id":5, "company_id":3},
	{"number": "TAYEB 002", "columns":3, "rows":5, "status_id":3, "journey_id":5, "company_id":3},
	{"number": "TAYEB 003", "columns":3, "rows":5, "status_id":3, "journey_id":6, "company_id":3},
	{"number": "TAYEB 004", "columns":3, "rows":5, "status_id":3, "journey_id":6, "company_id":3},	
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
		# db.session.commit()
	db.session.commit()


def create_buses():
	choices = range(30, 50)
	now = datetime.now()
	then = now + timedelta(random.choice(choices))
	for each in buses:
		bus = Bus(number=each["number"], columns=each["columns"], rows=each["rows"], broadcast=True, 
			departure_time=then, booking_deadline=(then-timedelta(minutes=30)), free_bus_time=(then+timedelta(minutes=30)), 
			company_id=each["company_id"], status_id=each["status_id"], journey_id=each["journey_id"])
		db.session.add(bus)
		set_bus_grids_from_layout(bus, bus_layouts.get('A'))
		db.session.commit()




def main():
	create_companies()
	create_branches()
	create_statuses()
	create_journeys()
	create_buses()



# # company
# company1 = Company("Gagga", logo="logo_1.png")

# # branch
# branch1 = Branch("Arua", "Arua", company1)

# # journey
# journey1 = Journey("Arua", "Kampala", branch1)

# # status
# status1 = Status("Ordinary", company1)
# status2 = Status("Luxury", company1)

# # bus
# bus1 = Bus("UBB777B", 3, 2,  company1)

# # grids
# grid1 = Grid(0, 1, bus1, "01", None)
# grid2 = Grid(1, 1, bus1, "02", None)
# grid3 = Grid(2, 1, bus1, "03", None)
# grid4 = Grid(3, 1, bus1, "04", None)
# grid5 = Grid(4, 1, bus1, "05", None)

# # stops
# stop1 = Stop("Nebbi", journey1)
# stop2 = Stop("Pakwach", journey1)
# stop3 = Stop("Karuma", journey1)

# # pricing
# pricing1 = Pricing(10000, stop1, status1)
# pricing2 = Pricing(20000, stop1, status2)
# pricing3 = Pricing(15000, stop2, status1)
# pricing4 = Pricing(30000, stop2, status2)
# pricing5 = Pricing(20000, stop3, status1)
# pricing6 = Pricing(40000, stop3, status2)

# # users
# user1 = User("samuelitwaru@gmail.com", "samuelitwaru", "123")
# user2 = User("joshuabyenkya@gmail.com", "joshuabyenkya", "123")

# # staff
# staff1 = Staff("Samuel", "Itwaru", user1)
# staff2 = Staff("Joshua", "Byenkya", user2)

# # GROUP ALL OBJECTS IN LISTS
# companies = [company1]
# branches = [branch1]
# journeys = [journey1]
# statuses = [status1, status2]
# buses = [bus1]
# grids = [grid1, grid2, grid3, grid4, grid5]
# stops = [stop1, stop2, stop3]
# pricing = [pricing1, pricing2, pricing3, pricing4, pricing5, pricing6]
# users = [user1, user2]
# staff = [staff1, staff2]

# # ADD ALL OBJECTS TO DATABASE
# db.session.add_all(companies)
# db.session.add_all(branches)
# db.session.add_all(journeys)
# db.session.add_all(statuses)
# db.session.add_all(buses)
# db.session.add_all(grids)
# db.session.add_all(stops)
# db.session.add_all(pricing)
# db.session.add_all(users)
# db.session.add_all(staff)

# # SAVE ALL OBJECTS
# db.session.commit()
