from app import app
from flask import request
from flask_login import current_user


@app.context_processor
def application():
	return  {
		"HOST": app.config.get("HOST_ADDRESS")
	}

@app.context_processor
def company():
	context = dict()
	if current_user.is_authenticated:
		context["profile"] = current_user.profile
		branch = current_user.profile.branch
		if branch:
			context["branch"] = branch
			context["company"] = branch.company
	return context



