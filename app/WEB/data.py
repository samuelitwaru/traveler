from app import app
from app.utils import split_telephone

class BusSchedule:
	
	def __init__(self, bus):
		if bus.departure_time:
			self.departure_time = bus.departure_time.strftime(app.config.get("DATETIME_FORMAT"))
			self.broadcast = bus.broadcast
			self.journey = bus.journey
			if bus.booking_deadline:
				self.booking_deadline = (bus.departure_time-bus.booking_deadline).seconds//60
			if bus.free_bus_time:
				self.free_bus_time = (bus.free_bus_time-bus.departure_time).seconds//60


class CreatePassengerBookingFormData:

	def __init__(self, passenger):
		if passenger:
			self.passenger_name = passenger.display_name()
			code, telephone = split_telephone(passenger.telephone)
			self.telephone_code = code
			self.passenger_telephone = telephone




user_categories = {
	"admin": 1,
	"manager": 2,
	"cashier":3,
	"passenger": 4,
}

'''
[
	{'id': 16, 'index': 0, 'grid_type': 1, 'number': 1, 'label': None, 'booking_id': None, 'booked': False}, 
	{'id': 17, 'index': 1, 'grid_type': 1, 'number': 2, 'label': None, 'booking_id': None, 'booked': False}, 
	{'id': 18, 'index': 2, 'grid_type': 0, 'number': None, 'label': None, 'booking_id': None, 'booked': False},
	{'id': 19, 'index': 3, 'grid_type': 1, 'number': 3, 'label': None, 'booking_id': None, 'booked': False}, 
	{'id': 20, 'index': 4, 'grid_type': 1, 'number': 4, 'label': None, 'booking_id': None, 'booked': False}, 
	{'id': 21, 'index': 5, 'grid_type': 1, 'number': 5, 'label': None, 'booking_id': None, 'booked': False}, 
	{'id': 22, 'index': 6, 'grid_type': 1, 'number': 6, 'label': None, 'booking_id': None, 'booked': False}, 
	{'id': 23, 'index': 7, 'grid_type': 1, 'number': 7, 'label': None, 'booking_id': None, 'booked': False}, 
	{'id': 24, 'index': 8, 'grid_type': 1, 'number': 8, 'label': None, 'booking_id': None, 'booked': False}, 
	{'id': 25, 'index': 9, 'grid_type': 1, 'number': 9, 'label': None, 'booking_id': None, 'booked': False}, 
	{'id': 26, 'index': 10, 'grid_type': 1, 'number': 10, 'label': None, 'booking_id': None, 'booked': False},
	{'id': 27, 'index': 11, 'grid_type': 1, 'number': 11, 'label': None, 'booking_id': None, 'booked': False},
	{'id': 28, 'index': 12, 'grid_type': 1, 'number': 12, 'label': None, 'booking_id': None, 'booked': False},
	{'id': 29, 'index': 13, 'grid_type': 1, 'number': 13, 'label': None, 'booking_id': None, 'booked': False},
	{'id': 30, 'index': 14, 'grid_type': 1, 'number': 14, 'label': None, 'booking_id': None, 'booked': False}
]
'''


location_graph = {
	"continents": [
		{
			"Africa" : {

			}
		}
	],

	"countries": [
		{
			"UG": {
				"name": "Uganda",
				"scale": 1,
				"path": "MO,0 L30,0 L30,40 L0,40 Z",
				"nodes": [
					{"id":1, "name":"Arua", "x":1, "y":1},
					{"id":2, "name":"Nebbi", "x":3, "y":4},
					{"id":3, "name":"Pakwack", "x":6, "y":5},
					{"id":4, "name":"Karuma", "x":8, "y":7},
					{"id":5, "name":"Kampala", "x":10, "y":11},
				],

				"graph": {
					0: [1],
					1: [0,2],
					2: [1,3],
					3: [2,4],
					4: [3],

				}
			}
		}
	],
}