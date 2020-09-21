import uuid
from app.models import Payment, db
from app.utils import get_current_branch

def create_payment(booking):
	grid = booking.booked_grid
	bus = grid.bus
	company = bus.company
	branch = get_current_branch()
	payment = Payment(reference=generate_reference(), amount=booking.fare, 
		method="CASH", passenger_name=booking.passenger_name, 
		passenger_telephone=booking.passenger_telephone, branch_name=branch.name,
		company_name=company.name, grid_number=grid.number, bus_number=bus.number,
		grid_id=grid.id)
	booking.payment = payment
	db.session.add(payment)


def update_payment(booking):
	payment = booking.payment
	payment.amount = booking.fare
	payment.passenger_name = booking.passenger_name
	payment.passenger_telephone = booking.passenger_telephone



def generate_reference():
	return str(uuid.uuid4())