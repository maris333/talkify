from flask_login import UserMixin
from src import db


class User(db.Model, UserMixin):
    """
    User model representing the user entity in the database.

    Attributes:
    - id (int): Primary key for the user.
    - username (str): Unique username for the user.
    - password (str): Hashed password for the user.
    - files (relationship): Relationship to the Files model for user's files.

    Methods:
    - __init__: Initializes a new User object.
    - get_id: Returns the string representation of the user's ID.
    - get: Static method to retrieve a user by ID.
    - is_active: Returns True indicating that the user is active.
    - is_authenticated: Returns True indicating that the user is authenticated.
    - is_anonymous: Returns False indicating that the user is not anonymous.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    files = db.relationship("Files", backref="user", lazy=True)

    def __init__(self, username, password, id=None):
        self.username = username
        self.password = password
        if id is not None:
            self.id = id

    def get_id(self):
        return str(self.id)

    @staticmethod
    def get(user_id):
        return User.query.get(int(user_id))

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False
