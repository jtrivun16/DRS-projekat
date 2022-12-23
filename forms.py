from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired, Email

from models import User


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=5, max=255)], render_kw={"placeholder": "Password"})
    remember = BooleanField('Remember Me')
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})

    first_name = StringField(validators=[InputRequired(), Length(
        min=3, max=20)], render_kw={"placeholder": "FirstName"})

    last_name = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "LastName"})

    address = StringField(validators=[InputRequired(), Length(
        min=4, max=35)], render_kw={"placeholder": "Address"})

    town = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Town"})

    country = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Country"})

    phone_number = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Phone number"})

    email = EmailField(validators=[InputRequired()], render_kw={'placeholder': "example@gmail.com"})

    password = PasswordField(validators=[InputRequired(), Length(
        min=5, max=255)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class UpdateAccountForm(FlaskForm):
    first_name = StringField('Ime', validators=[DataRequired(), Length(min=2, max=20)])

    last_name = StringField('Prezime', validators=[DataRequired(), Length(min=2, max=20)])

    address = StringField('Addresa', validators=[DataRequired(), Length(min=2, max=35)])

    town = StringField('Grad', validators=[DataRequired(), Length(min=2, max=20)])

    country = StringField('Drzava', validators=[DataRequired(), Length(min=2, max=20)])

    phone_number = IntegerField(validators=[DataRequired()])

    password = PasswordField(validators=[DataRequired(), Length( min=5, max=255)])

    username = StringField('Korisniko ime', validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('E-mail', validators=[DataRequired(), Email()])

    # picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Izmeni')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')



