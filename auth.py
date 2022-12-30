from flask import render_template, url_for, redirect, Blueprint, request
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, EmailField, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError
from __init__ import db, bcrypt, login_manager
from forms import RegisterForm, LoginForm, UpdateAccountForm, ValidateAccount
from models import User

auth = Blueprint('auth', __name__)


def save_user_data(form): # used to save user data into db
    hashed_password = bcrypt.generate_password_hash(form.password.data)

    new_user = User(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data,
                    address=form.address.data, town=form.town.data, country=form.country.data,
                    phone_number=form.phone_number.data, cardNumber=form.cardNumber.data, email=form.email.data,
                    verified=False, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()



def update_user_data(form):  # used to save user data into db
    hashed_password = bcrypt.generate_password_hash(form.password.data)

    user = User.query.filter_by(username=form.username.data).first()
    user.username = form.username.data
    user.first_name = form.first_name.data
    user.last_name = form.last_name.data
    user.address = form.address.data
    user.town = form.town.data
    user.country = form.country.data
    user.phone_number = form.phone_number.data
    user.cardNumber = form.cardNumber.data
    user.email = form.email.data
    user.password = hashed_password
    db.session.commit()

def update_user_data(user):  # used to save user data into db
    hashed_password = bcrypt.generate_password_hash(user.password)

    loaded_user = User.query.filter_by(username=user.username).first()
    loaded_user.username = user.username
    loaded_user.first_name = user.first_name
    loaded_user.last_name = user.last_name
    loaded_user.address = user.address
    loaded_user.town = user.town
    loaded_user.country = user.country
    loaded_user.phone_number = user.phone_number
    loaded_user.cardNumber = user.cardNumber
    loaded_user.email = user.email
    loaded_user.password = hashed_password
    db.session.commit()
    print(user.verified)



@login_manager.user_loader  # reload user obj from the user id stored in the session
def load_user(user_id):
    return User.query.get(user_id)


@auth.route('/login', methods=['GET', 'POST'])
def login(login_error=None):
    form = LoginForm()
    if not form.validate_on_submit():
        return render_template('login.html', form=form)
    else:
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            load_user(user.id)
            login_user(user, remember=form.remember.data)
            return redirect(url_for('views.dashboard'))
        else:
            raise ValidationError('wrong username or password')


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/status')
@login_required
def status():
    user = current_user
    if user.is_verified:
        return render_template('statusCheck.html', visibility="hidden")
    else:
        return render_template('statusCheck.html', visibility="visible")


@auth.route('/account_verification', methods=['GET', 'POST'])
@login_required
def account_verification():
    form = ValidateAccount()
    if request.method == 'GET':
        return render_template('accountVerification.html', form=form)
    else:
        card_number = form.card_number
        print(card_number)
        # TODO check card number if ok than and message
        if current_user.validate_cardNumber(card_number):
            current_user.verified = True;
            update_user_data(current_user)
            db.session.commit()
            return render_template('statusCheck.html')
        #else return render_template('accountVerification.html')



@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        save_user_data(form)
        return redirect(url_for('auth.login'))

    print(form.errors)
    return render_template('register.html', form=form)


@auth.route('/editProfile', methods=['GET', 'POST'])
@login_required
def update_profile():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        update_user_data(form)
        return redirect(url_for('views.dashboard'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.address.data = current_user.address
        form.town.data = current_user.town
        form.country.data = current_user.country
        form.phone_number.data = current_user.phone_number
        form.email.data = current_user.email
        form.cardNumber.data = current_user.cardNumber
        form.password.data = current_user.password  # TODO

    return render_template('editProfile.html', form=form)

@auth.route('/dashboard', methods=['GET', 'POST'])
@login_required
def back():
    return redirect(url_for('views.dashboard'))

@auth.route('/pay_in')
@login_required
def pay_in():
    return render_template('payIn.html')

@auth.route('/history')
@login_required
def history():
    return render_template('history.html')