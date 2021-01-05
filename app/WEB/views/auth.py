from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import login_user, current_user, logout_user, login_required
from app.utils import authenticate_user, create_user_token
from werkzeug.security import gen_salt
from app.helpers import send_auth_mail
from app.models import Token, User, db
from ..forms import SetPasswordForm, ResetPasswordForm

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
        logout_user()
        flash("Password set. Login with your new password.", "success")
        return redirect(url_for("index.login"))

    
    context = {"target_user":user, "set_password_form": set_password_form}
    return render_template("auth/set-password.html", target_user=user, set_password_form=set_password_form) 


@auth_bp.route('password/reset', methods=["GET", "POST"])
def reset_password():
    reset_password_form = ResetPasswordForm()
    if reset_password_form.validate_on_submit():
        email = reset_password_form.email.data
        user = User.query.filter_by(email=email).first()
        if user:
            create_user_token(user)
            db.session.commit()
            send_auth_mail(user.username, user.token.token)
            flash(f"An email with password reset instructions has been sent to '{email}'. Login to your this email to continue.", "info")
        else:
            flash(f"User with email '{email}' was not found.", "danger")
        return redirect(url_for('auth.reset_password'))
    return render_template('auth/reset-password.html', reset_password_form=reset_password_form)


@auth_bp.route('token/<int:user_id>/set')
@login_required
def set_token(user_id):
    user = User.query.get(user_id)
    token = user.token
    if user.token:
        db.session.delete(token)
    create_user_token(user)
    db.session.commit()
    send_auth_mail(user.username, user.token.token)
    flash("Token created.", "success")
    return redirect(request.referrer)


@auth_bp.route('recovery-password/<int:user_id>/set')
def set_recovery_password(user_id):
    user = User.query.get(user_id)
    create_user_token(user)
    recovery_password = gen_salt(10) 
    user.recovery_password = recovery_password
    db.session.commit()
    flash(f"Recovery password set to '{recovery_password}'", "success")
    return redirect(request.referrer)

