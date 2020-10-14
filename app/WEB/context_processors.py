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
	if current_user.is_authenticated:
		branch = current_user.profile.branch
		if branch:
			return {
				"branch": branch,
				"company": branch.company,
			}

	return {}



