"""
This module initializes a Flask application and sets up essential components
such as database, login manager, and blueprints for various views.
"""

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app: Flask = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db: SQLAlchemy = SQLAlchemy()
login_manager: LoginManager = LoginManager(app)
login_manager.login_view = "login"
migrate: Migrate = Migrate(app, db)


@login_manager.user_loader
def load_user(user_id: str):
    """
    A callback function for Flask-Login to reload the user object from the user ID stored in the session.

    Parameters:
    - user_id (str): The user ID to load.

    Returns:
    - User: The user object associated with the given user ID.
    """
    from src.models.auth import User

    return User.get(user_id)


def create_app() -> Flask:
    """
    Factory function to create and configure the Flask application.

    Returns:
    - Flask: The configured Flask application.
    """
    from src.views.main import (
        index_blueprint,
        translate_blueprint,
        download_blueprint,
        download_file_blueprint,
    )
    from src.views.auth import register_blueprint, login_blueprint, logout_blueprint

    with app.app_context():
        app.register_blueprint(index_blueprint)
        app.register_blueprint(register_blueprint)
        app.register_blueprint(login_blueprint)
        app.register_blueprint(logout_blueprint)
        app.register_blueprint(translate_blueprint)
        app.register_blueprint(download_blueprint)
        app.register_blueprint(download_file_blueprint)
        db.init_app(app)
        db.create_all()

    return app
