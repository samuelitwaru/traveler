from app import mail
from flask import render_template
from flask_mail import Message


def send_auth_mail(email, token):
	msg = Message(
		"Authentication", 
		sender='samuelitwaru@gmail.com', 
		recipients=[email]
	)
	msg.html = render_template('email/authentication.html', token=token)
	try:
		mail.send(msg)
	except:
		print("ERROR: Email sending failed!")