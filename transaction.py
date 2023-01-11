from flask import render_template, url_for, redirect, Blueprint, request
from flask_login import login_required, current_user
from database_functions import get_user, get_payment_card, get_online_account
from forms import SendFundsToMyAccount
from __init__ import db

transactions = Blueprint('transactions', __name__)


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

    user = get_user(current_user.username)
    online_account = get_online_account(user.onlineCardNumber)
    payment_card = get_payment_card(user.cardNumber)
    return render_template('payIn.html', acc_balance=online_account.balance,
                           payment_card_balance=payment_card.balance, form=form)


@transactions.route('/history')
@login_required
def history():
    return render_template('history.html')


def payoff_from_payment_card(amount, card_num):
    payment_card = get_payment_card(card_num)
    if payment_card.balance >= amount:
        payment_card.balance -= amount
        return True

    # TODO else throw error that he doesn't have that amount od money


def add_funds_to_online_account(amount, acc_number):
    online_account = get_online_account(acc_number)
    online_account.balance += amount
    db.session.commit()  # save changes to db


def send_funds_to_online_account(amount):
    user = get_user(current_user.username)

    if payoff_from_payment_card(amount, user.cardNumber):
        add_funds_to_online_account(amount, user.onlineCardNumber)
