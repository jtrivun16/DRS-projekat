from datetime import datetime
import string
import threading
from multiprocessing import Queue
from xml.dom import ValidationErr
from flask import render_template, url_for, redirect, Blueprint, request
from flask_login import login_required, current_user
from forms import SendFundsToAnotherAccount, SendFundsToMyAccount, ValidateAccount
from time import sleep
from __init__ import db
import random

from database_models import Transaction
from database_functions import get_user_by_username, get_payment_card, get_online_account, get_user_by_email, get_transaction


transactions = Blueprint('transactions', __name__)
transactions_queue = Queue()

@transactions.route('/dashboard', methods=['GET', 'POST'])
@login_required
def back():
    return redirect(url_for('views.dashboard'))


@transactions.route('/pay_in', methods=['GET', 'POST'])
@login_required
def balance_check():
    form = SendFundsToMyAccount()

    if request.method == 'POST':
        send_funds_to_online_account(form.amount.data)
        return redirect(url_for('auth.status'))

    user = get_user_by_username(current_user.username)
    online_account = get_online_account(user.onlineCardNumber)
    payment_card = get_payment_card(user.cardNumber)
    return render_template('payIn.html', acc_balance=online_account.balance,
                           payment_card_balance=payment_card.balance, form=form)


@transactions.route('/history', methods=['GET', 'POST'])
def history():
    transaction_list = Transaction.query.all()
    return render_template("history.html", data=transaction_list)

def payoff_from_payment_card(amount, card_num):
    payment_card = get_payment_card(card_num)
    if payment_card.balance >= amount:
        payment_card.balance -= amount
        return True
    else:
        error_message = 'Nemate dovoljan iznos na vasem racunu. Neuspesna verifikacija.'
        return render_template('accountVerification.html',error_message=error_message)
      

    # TODO else throw error that he doesn't have that amount od money


def add_funds_to_online_account(amount, acc_number):
    online_account = get_online_account(acc_number)
    online_account.balance += amount
    db.session.commit()  # save changes to db


def send_funds_to_online_account(amount):
    user = get_user_by_username(current_user.username)

    if payoff_from_payment_card(amount, user.cardNumber):
        add_funds_to_online_account(amount, user.onlineCardNumber)

@transactions.route('/sendMoney', methods=['GET', 'POST'])
@login_required
def send_money():
    form = SendFundsToAnotherAccount()

    if request.method == 'POST':
        init_transaction(form)
        return redirect(url_for('transactions.history'))
    else:
        user = get_user_by_username(current_user.username)
        online_account = get_online_account(user.onlineCardNumber)
        payment_card = get_payment_card(user.cardNumber)
        return render_template('sendMoney.html', acc_balance=online_account.balance,
                               payment_card_balance=payment_card.balance, form=form)
# @transactions.route('/transactions', methods=['POST'])
def init_transaction(form):


    sender = current_user.email  # TODO nemas ga
    if form.email.data != "":
        receiver_user = get_user_by_email(form.email.data)
        if not receiver_user.verified:
            return
            #TODO neki error
        if receiver_user is not None:
            card = get_payment_card(receiver_user.cardNumber)
            receiver = str(card.card_number)
    elif form.cardNumber.data is not None:
        receiver = form.cardNumber.data
    # else:
        # TODO handle error

    amount = form.amount.data

    transaction_num = add_transaction(sender, receiver, amount)
    new_transaction = get_transaction(transaction_num)

    thread = threading.Thread(target=transaction_thread, args=(new_transaction,))
    thread.start()

    # return_value = {'message': 'Transaction successfully initialized'}, 200
    # return return_value


# generate data for transaction and inset it into db
def add_transaction(sender: str, receiver: int, amount: float):
    # cursor = mysql.connection.cursor()
    # cursor.execute(''' INSERT INTO transaction VALUES (%s, %s, %s, %s, %s, %s, %s)''', (id, sender, receiver, amount, date, currency, state))
    # mysql.connection.commit()
    # cursor.close()
    date = datetime.now()
    state = "U obradi"

    transaction_number = ''.join(random.choices(string.digits, k=18))
    while transaction_exists(transaction_number):
        transaction_number = ''.join(random.choices(string.digits, k=18))

    transaction = Transaction()
    transaction.receiver = receiver
    transaction.date = date
    transaction.state = state
    transaction.amount = amount
    transaction.sender = sender
    transaction.transaction_number = transaction_number
    transaction.id = id(transaction)
    db.session.add(transaction)
    db.session.commit()
    return transaction_number


# just check if this transaction alredy exists
def transaction_exists(transaction_num):
    transaction = get_transaction(transaction_num)
    if transaction is not None:
        return True
    else:
        return


# insert transaction into a queue
def transaction_thread(transaction):
    print('Transaction ', transaction.id, ' thread started ')
    sleep(5) # TODO stavi na 120
    #TODO satavi refresh

    transactions_queue.put(transaction)


# takes transaction from queue and process them
def transaction_process(queue: Queue):
    while True:
        transaction = queue.get()

        print('Transaction ', transaction.id, ' process started ')
        sender = get_user_by_email(transaction.sender)
        receiver_card = get_payment_card(transaction.receiver)

        from_balance = sender.cardNumber

        tr = get_transaction(transaction_num=transaction.transaction_number)

        if payoff_from_payment_card(transaction.amount, from_balance):
            receiver_card.balance += transaction.amount
            tr.state = "Obradjeno"
            db.session.commit()

        else:
            tr.state = "Odbijeno"
            db.session.commit()
