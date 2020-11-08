from app import app


class BusSchedule:
	
	def __init__(self, bus):
		if bus.departure_time:
			self.departure_time = bus.departure_time.strftime(app.config.get("TIME_FORMAT"))
			self.broadcast = bus.broadcast
			self.journey = bus.journey
			if bus.booking_deadline:
				self.booking_deadline = (bus.departure_time-bus.booking_deadline).seconds//60
			if bus.free_bus_time:
				self.free_bus_time = (bus.free_bus_time-bus.departure_time).seconds//60