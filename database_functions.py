from database_models import User, PaymentCard, OnlineAccount,Transaction
from __init__ import db, bcrypt


def update_user_data(form, current_user):  # used to save user data from form into db
    hashed_password = bcrypt.generate_password_hash(form.password.data)

    user = get_user_by_username(current_user.username)
    user.username = form.username.data
    user.first_name = form.first_name.data
    user.last_name = form.last_name.data
    user.address = form.address.data
    user.town = form.town.data
    user.country = form.country.data
    user.phone_number = form.phone_number.data
    user.email = form.email.data
    user.password = hashed_password
    db.session.commit()


def update_user_data_verification(user):  # used to save user data into db
    # hashed_password = bcrypt.generate_password_hash(user.password)

    loaded_user = get_user_by_username(user.username)
    loaded_user.username = user.username
    loaded_user.first_name = user.first_name
    loaded_user.last_name = user.last_name
    loaded_user.address = user.address
    loaded_user.town = user.town
    loaded_user.country = user.country
    loaded_user.phone_number = user.phone_number
    loaded_user.email = user.email
    loaded_user.password = user.password
    db.session.commit()
    print(user.verified)


def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return user
    print("Can't get user form db")
    #TODO else


def get_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    if user:
        return user
    print("Can't get user form db")
    # TODO else


def get_payment_card(acc_num):
    payment_card = PaymentCard.query.filter_by(card_number=acc_num).first()
    if payment_card:
        return payment_card
    print("Can't get payment card form db")


def get_online_account(acc_num):
    account = OnlineAccount.query.filter_by(card_number=acc_num).first()
    if account:
        return account
    print("Can't get online account form db")


def get_transaction(transaction_num):
    transaction = Transaction.query.filter_by(transaction_number=transaction_num).first()
    if transaction is not None:
        return transaction
    return None