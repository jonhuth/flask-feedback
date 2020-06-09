from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Length, Email, ValidationError


class RegisterUserForm(FlaskForm):
    """Form for adding pet."""
    username = StringField("Username", validators=[InputRequired(), Length(max=20)])
    password = PasswordField("Password", validators=[
        InputRequired(), Length(max=100)])
        # doesn't check email host suffix
    email = EmailField("Email", validators=[
        InputRequired(), Length(max=50)])
    first_name = StringField("First Name", validators=[
        InputRequired(), Length(max=30)])
    last_name = StringField("Last Name", validators=[
        InputRequired(), Length(max=30)])

class LoginUserForm(FlaskForm):
    """Form for adding pet."""
    username = StringField("Username", validators=[InputRequired(), Length(max=20)])
    password = PasswordField("Password", validators=[
        InputRequired(), Length(max=100)])
