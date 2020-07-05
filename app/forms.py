from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from .models import User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Submit")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_passoword = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo(password)]
    )

    submit = SubmitField("Submit")

    def validate_username(self, username):
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            raise ValidationError("Username already Exists")

    def validate_email(self, email):
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            raise ValidationError("Email already exists")

