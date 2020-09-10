from flask_restful import fields

class Fields:

	def company_fields(self):
		return { 
			"id": fields.Integer,
			"name": fields.String,
			"logo": fields.String,
			"branches": fields.Nested(self.branch_fields_min()),
			"buses": fields.Nested(self.bus_fields_min()),
			"statuses": fields.Nested(self.status_fields_min()),
		}

	def company_fields_min(self):
		return { 
			"id": fields.Integer,
			"name": fields.String,
			"logo": fields.String,
		}



	def branch_fields(self):
		return { 
			"id": fields.Integer,
			"name": fields.String,
			"location": fields.String,
			"company": fields.Nested(self.company_fields_min()),
			"journeys": fields.Nested(self.journey_fields_min()),
			"members": fields.Nested(self.profile_fields_min()),
		}

	def branch_fields_min(self):
		return { 
			"id": fields.Integer,
			"name": fields.String,
			"location": fields.String,
		}



	def journey_fields(self):
		return { 
			"id": fields.Integer,
			"from_": fields.String,
			"to": fields.String,
			"distance": fields.Float,
			"duration": fields.Float,
			"branch": fields.Nested(self.branch_fields_min()),
			"buses": fields.Nested(self.bus_fields_min()),
			"pickups": fields.Nested(self.pickup_fields_min()),
			"pricings": fields.Nested(self.pricing_fields_min()),
		}

	def journey_fields_min(self):
		return { 
			"id": fields.Integer,
			"from_": fields.String,
			"to": fields.String,
			"distance": fields.Float,
			"duration": fields.Float,
		}



	def pricing_fields(self):
		return { 
			"id": fields.Integer,
			"stop": fields.String,
			"price": fields.Integer,
			"status": fields.Nested(self.status_fields_min()),
			"journey": fields.Nested(self.journey_fields_min()),
		}

	def pricing_fields_min(self):
		return { 
			"id": fields.Integer,
			"stop": fields.String,
			"price": fields.Integer,
		}



	def status_fields(self):
		return { 
			"id": fields.Integer,
			"name": fields.String,
			"default": fields.Boolean,
			"company": fields.Nested(self.company_fields_min()),
			"pricings": fields.Nested(self.pricing_fields_min()),
			"buses": fields.Nested(self.bus_fields_min()),
		}

	def status_fields_min(self):
		return { 
			"id": fields.Integer,
			"name": fields.String,
			"default": fields.Boolean,
		}



	def pickup_fields(self):
		return { 
			"id": fields.Integer,
			"name": fields.String,
			"journey": fields.Nested(self.journey_fields_min()),
		}

	def pickup_fields_min(self):
		return { 
			"id": fields.Integer,
			"name": fields.String,
		}



	def bus_fields(self):
		return { 
			"id": fields.Integer,
			"number": fields.String,
			"columns": fields.Integer,
			"rows": fields.Integer,
			"broadcast": fields.Boolean,
			"departure_time": fields.DateTime,
			"company": fields.Nested(self.company_fields_min()),
			"status": fields.Nested(self.status_fields_min()),
			"journey": fields.Nested(self.journey_fields_min()),
			"grids": fields.Nested(self.grid_fields_min()),
		}

	def bus_fields_min(self):
		return { 
			"id": fields.Integer,
			"number": fields.String,
			"columns": fields.Integer,
			"rows": fields.Integer,
			"broadcast": fields.Boolean,
			"departure_time": fields.DateTime,
		}



	def grid_fields(self):
		return { 
			"id": fields.Integer,
			"index": fields.Integer,
			"grid_type": fields.Integer,
			"number": fields.String,
			"label": fields.String,
			"booking": fields.Nested(self.booking_fields_min()),
			"bus": fields.Nested(self.bus_fields_min()),
			"bookings": fields.Nested(self.booking_fields_min()),
			"booking": fields.Nested(self.booking_fields_min()),
		}

	def grid_fields_min(self):
		return { 
			"id": fields.Integer,
			"index": fields.Integer,
			"grid_type": fields.Integer,
			"number": fields.String,
			"label": fields.String,
			"booking": fields.Nested(self.booking_fields_min()),
		}



	def booking_fields(self):
		return { 
			"id": fields.Integer,
			"passenger_name": fields.String,
			"passenger_telephone": fields.String,
			"pickup": fields.String,
			"fare": fields.Integer,
			"paid": fields.Boolean,
			"grid": fields.Nested(self.grid_fields_min()),
			"pricing": fields.Nested(self.pricing_fields_min()),
			"payment": fields.Nested(self.payment_fields_min()),
			"payment": fields.Nested(self.payment_fields_min()),
		}

	def booking_fields_min(self):
		return { 
			"id": fields.Integer,
			"passenger_name": fields.String,
			"passenger_telephone": fields.String,
			"pickup": fields.String,
			"fare": fields.Integer,
			"paid": fields.Boolean,
		}



	def payment_fields(self):
		return { 
			"id": fields.Integer,
			"reference": fields.String,
			"amount": fields.Integer,
			"method": fields.String,
			"time": fields.DateTime,
			"app": fields.String,
			"company_name": fields.String,
			"branch_name": fields.String,
			"bus_number": fields.String,
			"grid_number": fields.String,
			"passenger_name": fields.String,
			"passenger_telephone": fields.String,
			"grid": fields.Nested(self.grid_fields_min()),
			"passenger": fields.Nested(self.passenger_fields_min()),
		}

	def payment_fields_min(self):
		return { 
			"id": fields.Integer,
			"reference": fields.String,
			"amount": fields.Integer,
			"method": fields.String,
			"time": fields.DateTime,
			"app": fields.String,
			"company_name": fields.String,
			"branch_name": fields.String,
			"bus_number": fields.String,
			"grid_number": fields.String,
			"passenger_name": fields.String,
			"passenger_telephone": fields.String,
		}



	def passenger_fields(self):
		return { 
			"id": fields.Integer,
			"first_name": fields.String,
			"last_name": fields.String,
			"email": fields.String,
			"telephone": fields.String,
			"password": fields.String,
			"payments": fields.Nested(self.payment_fields_min()),
		}

	def passenger_fields_min(self):
		return { 
			"id": fields.Integer,
			"first_name": fields.String,
			"last_name": fields.String,
			"email": fields.String,
			"telephone": fields.String,
			"password": fields.String,
		}



	def user_fields(self):
		return { 
			"id": fields.Integer,
			"email": fields.String,
			"username": fields.String,
			"password": fields.String,
			"profile": fields.Nested(self.profile_fields_min()),
			"token": fields.Nested(self.token_fields_min()),
		}

	def user_fields_min(self):
		return { 
			"id": fields.Integer,
			"email": fields.String,
			"username": fields.String,
			"password": fields.String,
		}



	def profile_fields(self):
		return { 
			"id": fields.Integer,
			"first_name": fields.String,
			"last_name": fields.String,
			"telephone": fields.String,
			"is_admin": fields.Boolean,
			"is_manager": fields.Boolean,
			"is_cashier": fields.Boolean,
			"branch": fields.Nested(self.branch_fields_min()),
			"user": fields.Nested(self.user_fields_min()),
		}

	def profile_fields_min(self):
		return { 
			"id": fields.Integer,
			"first_name": fields.String,
			"last_name": fields.String,
			"telephone": fields.String,
			"is_admin": fields.Boolean,
			"is_manager": fields.Boolean,
			"is_cashier": fields.Boolean,
		}



	def token_fields(self):
		return { 
			"id": fields.Integer,
			"token": fields.String,
			"expiry": fields.DateTime,
			"user": fields.Nested(self.user_fields_min()),
		}

	def token_fields_min(self):
		return { 
			"id": fields.Integer,
			"token": fields.String,
			"expiry": fields.DateTime,
		}



	def connection_fields(self):
		return { 
			"id": fields.Integer,
			"sid": fields.String,
			"connect_time": fields.DateTime,
			"disconnect_time": fields.DateTime,
			"client_type": fields.String,
		}

	def connection_fields_min(self):
		return { 
			"id": fields.Integer,
			"sid": fields.String,
			"connect_time": fields.DateTime,
			"disconnect_time": fields.DateTime,
			"client_type": fields.String,
		}


