from src.forms.auth import RegistrationForm
from src import db
from src.forms.auth import LoginForm
from src.models.auth import User
from flask_login import login_required, login_user, logout_user
from flask import render_template, Blueprint, redirect, url_for

register_blueprint: Blueprint = Blueprint("register", __name__)
login_blueprint: Blueprint = Blueprint("login", __name__)
logout_blueprint: Blueprint = Blueprint("logout", __name__)


@register_blueprint.route("/register", methods=["GET", "POST"])
def register():
    """
    Route for user registration.

    Returns:
    - str or redirect: Either a redirect to the login page on successful registration,
      or the registration form if the form is not validated.
    """
    form = RegistrationForm()

    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login.login"))

    return render_template("register.html", form=form)


@login_blueprint.route("/login", methods=["GET", "POST"])
def login():
    """
    Route for user login.

    Returns:
    - str or redirect: Either a redirect to the translation page on successful login,
      or the login form with an error message if the credentials are invalid.
    """
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for("translate.translate"))
        return render_template("login.html", form=form, error="Invalid credentials")

    return render_template("login.html", form=form, error=None)


@logout_blueprint.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    """
    Route for user logout.

    Returns:
    - str: The rendered HTML for the logout page.
    """
    logout_user()
    return render_template("logout.html")
