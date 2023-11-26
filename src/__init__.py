from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy()
login_manager = LoginManager(app)
login_manager.login_view = 'login'
migrate = Migrate(app, db)


@login_manager.user_loader
def load_user(user_id):
    from src.models.auth import User
    return User.get(user_id)


def create_app():
    from src.views.main import index_blueprint, translate_blueprint
    from src.views.auth import register_blueprint, login_blueprint, logout_blueprint

    with app.app_context():
        app.register_blueprint(index_blueprint)
        app.register_blueprint(register_blueprint)
        app.register_blueprint(login_blueprint)
        app.register_blueprint(logout_blueprint)
        app.register_blueprint(translate_blueprint)
        db.init_app(app)
        db.create_all()
    return app


