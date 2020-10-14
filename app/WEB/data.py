from app import app


class BusSchedule:
	
	def __init__(self, bus):
		if bus.departure_time:
			self.departure_time = bus.departure_time.strftime(app.config.get("TIME_FORMAT"))
			self.broadcast = bus.broadcast
			self.journey = bus.journey