from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import current_user, login_required
from  ..forms import UpdateUserPasswordForm
from app.models import User, db


user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('password/update', methods=["POST", "GET"])
@login_required
def update_user_password():
	user = current_user
	update_user_password_form = UpdateUserPasswordForm(current_user=user)
	if update_user_password_form.validate_on_submit():
		user.set_password(update_user_password_form.data.get("new_password"))
		db.session.commit()
		flash("Password Changed.", "success")
		return redirect(request.referrer)
	else:
		return render_template('user/update-user-password.html', update_user_password_form=update_user_password_form)


@user_bp.route('/<int:user_id>/active/update', methods=["GET"])
@login_required
def update_user_active_status(user_id):
	user = User.query.filter_by(id=user_id).first()
	if user:
		new_active_state = not user.is_active
		user.is_active = new_active_state
		db.session.commit()
		msg = "User deactivated."
		if user.is_active:
			msg = "User activated."
		flash(msg, "success")
	else:
		flash("User not found.", "danger")
	return redirect(request.referrer)

