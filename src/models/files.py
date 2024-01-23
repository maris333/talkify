from src import db


class Files(db.Model):
    """
    Files model representing files associated with users in the database.

    Attributes:
    - id (int): Primary key for the file.
    - filename (str): Name of the file.
    - user_id (int): Foreign key referencing the User model.

    Relationships:
    - user: Relationship to the User model.

    """

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
