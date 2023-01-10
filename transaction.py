from flask import render_template, url_for, redirect, Blueprint, request
from flask_login import login_user, logout_user, login_required, current_user
from database_functions import get_user, get_payment_card, get_online_account

transactions = Blueprint('transactions', __name__)


@transactions.route('/dashboard', methods=['GET', 'POST'])
@login_required
def back():
    return redirect(url_for('views.dashboard'))


@transactions.route('/pay_in')
@login_required
def pay_in():
    user = get_user(current_user.username)
    online_account = get_online_account(user.onlineCardNumber)
    payment_card = get_payment_card(user.cardNumber)
    return render_template('payIn.html', acc_balance=online_account.balance, payment_card_balance=payment_card.balance)


@transactions.route('/history')
@login_required
def history():
    return render_template('history.html')


def payoff(amount, card_num):
    payment_card = get_payment_card(card_num)
    if payment_card.balance >= amount:
        payment_card.balance -= amount
        return True

    # TODO else throw error


def add_funds(amount, card_num):
    payment_card = get_payment_card(card_num)
    payment_card.balance += amount



