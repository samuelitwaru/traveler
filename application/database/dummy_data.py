from application.database.models import *

# company
company1 = Company("Gagga", logo="logo_1.png")

# branch
branch1 = Branch("Arua", "Arua", company1)

# journey
journey1 = Journey("Arua", "Kampala", branch1)

# status
status1 = Status("Ordinary", company1)
status2 = Status("Luxury", company1)

# bus
bus1 = Bus("UBB777B", 6, company1)

# seats
seat1 = Seat("01", 0, 0, bus1)
seat2 = Seat("02", 0, 1, bus1)
seat3 = Seat("03", 0, 3, bus1)
seat4 = Seat("04", 0, 4, bus1)
seat5 = Seat("05", 0, 5, bus1)

# stops
stop1 = Stop("Nebbi", journey1)
stop2 = Stop("Pakwach", journey1)
stop3 = Stop("Karuma", journey1)

# pricing
pricing1 = Pricing(10000, stop1, status1)
pricing2 = Pricing(20000, stop1, status2)
pricing3 = Pricing(15000, stop2, status1)
pricing4 = Pricing(30000, stop2, status2)
pricing5 = Pricing(20000, stop3, status1)
pricing6 = Pricing(40000, stop3, status2)

# users
user1 = User("samuelitwaru@gmail.com", "samuelitwaru", "123")
user2 = User("joshuabyenkya@gmail.com", "joshuabyenkya", "123")

# staff
staff1 = Staff("Samuel", "Itwaru", user1)
staff2 = Staff("Joshua", "Byenkya", user2)

# GROUP ALL OBJECTS IN LISTS
companies = [company1]
branches = [branch1]
journeys = [journey1]
statuses = [status1, status2]
buses = [bus1]
seats = [seat1, seat2, seat3, seat4, seat5]
stops = [stop1, stop2, stop3]
pricing = [pricing1, pricing2, pricing3, pricing4, pricing5, pricing6]
users = [user1, user2]
staff = [staff1, staff2]

# ADD ALL OBJECTS TO DATABASE
db.session.add_all(companies)
db.session.add_all(branches)
db.session.add_all(journeys)
db.session.add_all(statuses)
db.session.add_all(buses)
db.session.add_all(seats)
db.session.add_all(stops)
db.session.add_all(pricing)
db.session.add_all(users)
db.session.add_all(staff)

# SAVE ALL OBJECTS
db.session.commit()
