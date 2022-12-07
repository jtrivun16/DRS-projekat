from flask import render_template, url_for, redirect, Blueprint
from flask_login import login_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, EmailField
from wtforms.validators import InputRequired, Length
from __init__ import db, bcrypt, login_manager
from models import User

auth = Blueprint('auth', __name__)


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})
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
        min=4, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Register")


@login_manager.user_loader  # reload user obj from the user id stored in the session
def load_user(user_id):
    return User.query.get(user_id)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                load_user(user.id)

                login_user(user)
                return redirect(url_for('views.dashboard'))
    else:
        return render_template('login.html', form=form)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    print("Hey Yo")
    if form.validate_on_submit():
        print("Hey  Yooooo")
        hashed_password = bcrypt.generate_password_hash(form.password.data)

        new_user = User(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data,
                        address=form.address.data, town=form.town.data,   country=form.country.data,
                        phone_number=form.phone_number.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))

    print(form.errors)
    return render_template('auth.register.html', form=form)
