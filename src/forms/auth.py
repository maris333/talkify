from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo

from src.models.auth import User


class LoginForm(FlaskForm):
    """
    Form for user login.

    Attributes:
    - username (StringField): Input field for username.
    - password (PasswordField): Input field for password.
    - submit (SubmitField): Button to submit the form.

    Validators:
    - username (DataRequired): Validates that the username field is not empty.
    - password (DataRequired): Validates that the password field is not empty.
    """

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    """
    Form for user registration.

    Attributes:
    - username (StringField): Input field for username.
    - password (PasswordField): Input field for password.
    - confirm_password (PasswordField): Input field to confirm the password.
    - submit (SubmitField): Button to submit the form.

    Validators:
    - username (DataRequired): Validates that the username field is not empty.
    - password (DataRequired): Validates that the password field is not empty.
    - confirm_password (DataRequired, EqualTo): Validates that the confirm_password
      field is not empty and matches the password field.

    Custom Validator:
    - validate_username: Checks if the username is already taken in the database.

    """

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        """
        Validates that the chosen username is not already taken.

        Parameters:
        - username (StringField): The username to be validated.

        Raises:
        - ValidationError: If the username is already taken.
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "Username is already taken. Please choose a different one."
            )
