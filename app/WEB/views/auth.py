from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import login_user, current_user
from app.utils import authenticate_user
from app.models import Token, db
from ..forms import SetPasswordForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('password/set/<token>', methods=["POST", "GET"])
def set_password(token):
    token = Token.query.filter_by(token=token).first()
    if not token or token.is_expired():
        flash("Your token is invalid or has expired", "danger")
        # resend another
        return redirect(url_for("index.index"))

    user = token.user
    set_password_form = SetPasswordForm()
    if set_password_form.validate_on_submit():
        password = set_password_form.data.get("password")
        user.set_password(password)
        db.session.delete(token)
        db.session.commit()
        flash("Password set. Login with your new password.", "success")
        return redirect(url_for("index.index"))

    
    context = {"target_user":user, "set_password_form": set_password_form}
    return render_template("auth/set-password.html", target_user=user, set_password_form=set_password_form) 


@auth_bp.route('password/reset')
def reset_password():
	return render_template('auth/reset-password.html')


