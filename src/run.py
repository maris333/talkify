from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy()
db.init_app(app)


if __name__ == '__main__':
    from src.views.views import index_blueprint
    app.register_blueprint(index_blueprint)
    app.run(debug=True)
