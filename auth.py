import datetime
import string
import random

from flask import render_template, url_for, redirect, Blueprint, request
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, EmailField, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError
from __init__ import db, bcrypt, login_manager
from forms import RegisterForm, LoginForm, UpdateAccountForm, ValidateAccount
from database_models import User, PaymentCard, OnlineAccount
from database_functions import get_user, get_payment_card, update_user_data, update_user_data_verification, get_online_account
from transaction import payoff
import uuid

auth = Blueprint('auth', __name__)


# def update_user_data(form):  # used to save user data from form into db
#     hashed_password = bcrypt.generate_password_hash(form.password.data)
#
#     user = get_user(form.username.data)
#     user.username = form.username.data
#     user.first_name = form.first_name.data
#     user.last_name = form.last_name.data
#     user.address = form.address.data
#     user.town = form.town.data
#     user.country = form.country.data
#     user.phone_number = form.phone_number.data
#     user.email = form.email.data
#     user.password = hashed_password
#     db.session.commit()
#
#
# def update_user_data_verification(user):  # used to save user data into db
#     # hashed_password = bcrypt.generate_password_hash(user.password)
#
#     loaded_user = get_user(user.username)
#     loaded_user.username = user.username
#     loaded_user.first_name = user.first_name
#     loaded_user.last_name = user.last_name
#     loaded_user.address = user.address
#     loaded_user.town = user.town
#     loaded_user.country = user.country
#     loaded_user.phone_number = user.phone_number
#     loaded_user.email = user.email
#     loaded_user.password = user.password
#     db.session.commit()
#     print(user.verified)


@login_manager.user_loader  # reload user obj from the user id stored in the session
def load_user(user_id):
    return User.query.get(user_id)


@auth.route('/login', methods=['GET', 'POST'])
def login(login_error=None):
    form = LoginForm()
    if not form.validate_on_submit():
        return render_template('login.html', form=form)
    else:
        user = get_user(form.username.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            load_user(user.id)
            login_user(user)
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
def status():  # this function check if user account is verified
    #user = User.query.get(current_user.id)
    user = get_user(current_user.username)
    online_account = get_online_account(user.onlineCardNumber)
    if user.is_verified:
        return render_template('statusCheck.html', visibility="hidden", balance=online_account.balance)
    else:
        return render_template('statusCheck.html', visibility="visible", balance=0)


@auth.route('/account_verification', methods=['GET', 'POST'])
@login_required
def account_verification():
    form = ValidateAccount()
    if request.method == 'GET':
        return render_template('accountVerification.html', form=form)
    else:
        card_number = form.card_number
        print(card_number.data)
        # TODO check card number if ok than and message
        # PaymentCard.pay_in(1,card_number.data)
        if current_user.validate_card_number(card_number):
            if payoff(1, card_number.data):  # payoff one dollar
                current_user.verified = True
                update_user_data_verification(current_user)
                db.session.commit()
                return redirect(url_for('auth.status'))
            # else  no money error
        # else return render_template('accountVerification.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = save_user_data(form)
        user = User.query.filter_by(username=username).first()
        user.cardNumber = create_payment_card(user.id, user.username)
        user.onlineCardNumber = create_online_account(user.username, user.email)
        db.session.commit()
        return redirect(url_for('auth.login'))

    print(form.errors)
    return render_template('register.html', form=form)


def save_user_data(form):  # used to save user data into db used only for creating new users
    hashed_password = bcrypt.generate_password_hash(form.password.data)

    new_user = User(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data,
                    address=form.address.data, town=form.town.data, country=form.country.data,
                    phone_number=form.phone_number.data, cardNumber=1, onlineCardNumber=1, email=form.email.data,
                    verified=False, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return new_user.username


def create_payment_card(user_id, username):
    payment_card = PaymentCard()
    _accountNum = ''.join(random.choices(string.digits, k=18))
    while account_num_exists(_accountNum):
        _accountNum = ''.join(random.choices(string.digits, k=18))
    _security_code = ''.join(random.choices(string.digits, k=3))
    _expiry_date = datetime.datetime.today() + datetime.timedelta(days=730)

    payment_card.card_number = _accountNum
    payment_card.security_code = _security_code
    payment_card.balance = 0
    payment_card.user_id = user_id
    payment_card.user_name = username
    payment_card.balance = 10  # TODO da li na pocetku dodati malu sumu?
    payment_card.id = id(payment_card)  # unique integer number for every unique value it is used with.
    year = str(_expiry_date.month) + '/' + str(_expiry_date.year)[2:]
    payment_card.expiry_data = year

    db.session.add(payment_card)
    db.session.commit()
    return _accountNum


def create_online_account(username, email):
    online_account = OnlineAccount()
    _accountNum = ''.join(random.choices(string.digits, k=18))
    while account_num_exists(_accountNum):
        _accountNum = ''.join(random.choices(string.digits, k=18))

    online_account.card_number = _accountNum
    online_account.balance = 0
    online_account.user_email = email
    online_account.user_name = username
    online_account.balance = 0
    online_account.id = id(online_account)  # unique integer number for every unique value it is used with.

    db.session.add(online_account)
    db.session.commit()
    return _accountNum


#  Check if user with same account number already exists
#  We do this because account number is randomly generated and must be unique
def account_num_exists(acc_num):
    account = get_payment_card(acc_num)
    if account:
        return True
    else:
        return False


@auth.route('/editProfile', methods=['GET', 'POST'])
@login_required
def update_profile():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        update_user_data(form, current_user)
        return redirect(url_for('views.dashboard'))
    elif request.method == 'GET':
        print(current_user)
        form.username.data = current_user.username
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.address.data = current_user.address
        form.town.data = current_user.town
        form.country.data = current_user.country
        form.phone_number.data = current_user.phone_number
        form.email.data = current_user.email
        form.password.data = current_user.password

    return render_template('editProfile.html', form=form)


@auth.route('/dashboard', methods=['GET', 'POST'])
@login_required
def back():
    return redirect(url_for('views.dashboard'))

# @auth.route('/pay_in')
# @login_required
# def pay_in():
#     return render_template('payIn.html')
#
# @auth.route('/history')
# @login_required
# def history():
#     return render_template('history.html')

#  db access function


