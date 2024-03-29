import uuid
from flask import Blueprint, render_template, url_for, request, redirect, flash, session, make_response
from flask_login import current_user, login_required
from app import app, rave
from rave_python import RaveExceptions
from app.models import Payment, Bus, Grid, Pricing, db
from app.utils import get_current_branch, join_telephone
from ..forms import CreatePassengerBookingForm

payment_bp = Blueprint('payment', __name__, url_prefix='/payment')

@payment_bp.route("checkout/<int:payment_id>")
def get_payment(payment_id):
	payment = Payment.query.get(payment_id)
	return render_template("payment/payment.html", payment=payment)


@payment_bp.route("/checkout/<int:bus_id>/create", methods=["POST"])
def create_payment_checkout(bus_id):
	bus = Bus.query.filter_by(id=bus_id).first()
	create_passenger_booking_form = CreatePassengerBookingForm(data=request.form, bus=bus)
	
	profile = None
	if current_user.is_authenticated:
		profile = current_user.profile

	if create_passenger_booking_form.validate_on_submit():
		# create payment checkout
		data = create_passenger_booking_form.data
		grid_id = data.get("grid_id")
		pricing_id = data.get("pricing_id")
		passenger_name = data.get("passenger_name")
		passenger_email = data.get("passenger_email")
		telephone_code = data.get("telephone_code")
		passenger_telephone = data.get("passenger_telephone")
		telephone = join_telephone(telephone_code, passenger_telephone)

		grid = Grid.query.filter_by(id=grid_id).first()
		pricing = Pricing.query.filter_by(id=pricing_id).first()

		app_charge = round(pricing.price * app.config.get("APP_CHARGE"))

		payment = Payment(amount=pricing.price, app_charge=app_charge, method="ONLINE", 
			passenger_name=passenger_name, passenger_email=passenger_email, passenger_telephone=telephone, 
			grid_number=grid.number, bus_number=bus.number, bus_id=bus.id, grid_id=grid.id,
			company=bus.company, profile=profile, journey=bus.journey, pricing=pricing)
		
		db.session.add(payment)
		db.session.commit()
		return redirect(url_for('payment.get_payment', payment_id=payment.id))

	return render_template("bus/passenger-bus.html", bus=bus, create_passenger_booking_form=create_passenger_booking_form)


@payment_bp.route("checkout/<int:payment_id>/mobile-money")
def pay_with_mobile_money(payment_id):
	payment = Payment.query.get(payment_id)
	profile = None
	if current_user.is_authenticated:
		profile = current_user.profile

	payload = {
		"amount": payment.amount + payment.app_charge, # 500
		"email": payment.passenger_email, # "samuelitwaru@gmail.com"
		"phonenumber": payment.passenger_telephone.replace('-',''), # app.config.get("RAVE_TEST_NUMBER"),
		"redirect_url": f"{app.config.get('HOST_ADDRESS')}/payment/checkout/{payment.id}/rave",
		"IP": request.remote_addr
	}


	try:
		res = rave.UGMobile.charge(payload)
		print(">>>>>>>>>>>>", res)
		return redirect(res["link"], code=307)
		# res = rave.UGMobile.verify(res["link"])
		# print(">>>>>>>>>>>>", res)
		# return res
	except RaveExceptions.TransactionChargeError as e:
		print(e.err)
		print(e.err["flwRef"])
		return e.err
	except RaveExceptions.TransactionVerificationError as e:
		print(e.err["errMsg"])
		print(e.err["txRef"])
		return e.err["errMsg"]


@payment_bp.route("checkout/<int:payment_id>/card")
def pay_with_card(payment_id):
	payment = Payment.query.get(payment_id)
	profile = None
	email = None
	if current_user.is_authenticated:
		profile = current_user.profile
		email = profile.email
	payload = {
		"cardno": "5438898014560229",
		"cvv": "890",
		"expirymonth": "09",
		"expiryyear": "19",
		"amount": "10",
		"email": "samuelitwaru@gmail.com",
		"phonenumber": app.config.get("RAVE_TEST_NUMBER"),
		"firstname": "Samuel",
		"lastname": "Itwaru",
		"IP": "355426087298442",
	}

	try:
		res = rave.Card.charge(payload)
		if res["suggestedAuth"]:
			arg = Misc.getTypeOfArgsRequired(res["suggestedAuth"])
			if arg == "pin":
				Misc.updatePayload(res["suggestedAuth"], payload, pin="3310")
			if arg == "address":
				Misc.updatePayload(res["suggestedAuth"], payload, address={"billingzip":"07205", "billingcity":"Hillside", "billingaddress":"470 Mundet PI", "billingstate":"NJ", "billingcountry":"US"})

		if res["validationRequired"]:
			rave.Card.validate(res["flwRef"], "")

		res = rave.Card.verify(res["txRef"])
		print(res["transaction"])
	except RaveExceptions.CardChargeError as e:
		print(e.err["errMsg"])
		print(e.err["flwRef"])
	except RaveExceptions.TransactionValidationError as e:
		print(e.err)
		print(e.err["flwRef"])
	except RaveExceptions.TransactionVerificationError as e:
		print(e.err["errMsg"])
		print(e.err["txRef"])

def create_payment(booking):
	grid = booking.booked_grid
	bus = grid.bus
	company = bus.company
	branch = get_current_branch()
	payment = Payment(reference=generate_reference(), amount=booking.fare, 
		method="CASH", passenger_name=booking.passenger_name, 
		passenger_telephone=booking.passenger_telephone, branch_name=branch.name,
		company_name=company.name, grid_number=grid.number, bus_number=bus.number,
		company=company, bus=bus, journey=bus.journey, pricing=booking.pricing,
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