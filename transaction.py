import threading
from multiprocessing import Queue
from xml.dom import ValidationErr
from Models import Transaction
from flask import render_template, url_for, redirect, Blueprint, request
from flask_login import login_required, current_user
from database_functions import get_user, get_payment_card, get_online_account
from forms import SendFundsToAnotherAccount, SendFundsToMyAccount, ValidateAccount
from time import sleep
from __init__ import db

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
    form = ValidateAccount()
    payment_card = get_payment_card(card_num)
    if payment_card.balance >= amount:
        payment_card.balance -= amount
        return True
    else:
        error_message = 'Nemate dovoljan iznos na vasem racunu. Neuspesna verifikacija.'
        return render_template('accountVerification.html',error_message =  error_message, form = form)
      

    # TODO else throw error that he doesn't have that amount od money


def add_funds_to_online_account(amount, acc_number):
    online_account = get_online_account(acc_number)
    online_account.balance += amount
    db.session.commit()  # save changes to db


def send_funds_to_online_account(amount):
    user = get_user(current_user.username)

    if payoff_from_payment_card(amount, user.cardNumber):
        add_funds_to_online_account(amount, user.onlineCardNumber)

@transactions.route('/sendMoney', methods=['GET', 'POST'])
@login_required
def sendMoney():
    form = SendFundsToAnotherAccount()
    user = get_user(current_user.username)
    online_account = get_online_account(user.onlineCardNumber)
    payment_card = get_payment_card(user.cardNumber)
    return render_template('sendMoney.html',acc_balance=online_account.balance,
                           payment_card_balance=payment_card.balance, form = form )


# ####### not impl yet #########
# @transactions.route('/transactions', methods=['POST'])
# def initTransaction():
#     content = request.json
#     _id = getLastTransactionIndex()
#     _sender = content['sender']
#     _receiver = content['receiver']
#     _amount = content['amount']
#     _transaction_currecny = content['transactionCurrency']
#     _date = content['date']
#     _state = content['state']
#     _rsdEquivalent = content['rsdEquivalent']
#
#     addTransaction(_id, _sender, _receiver, _amount, _date, _transaction_currecny, _state)
#
#     thread = threading.Thread(target=transactionThread, args=(_id, _sender, _receiver, _amount, _date,
#                                                               _transaction_currecny, _state, _rsdEquivalent))
#     thread.start()
#
#     return_value = {'message': 'Transaction successfully initialized'}, 200
#     return return_value
#
#
# def addTransaction(id : int, sender : str, receiver : str, amount : float, date : Date, currency : str, state : str):
#     cursor = mysql.connection.cursor()
#     cursor.execute(''' INSERT INTO transaction VALUES (%s, %s, %s, %s, %s, %s, %s)''', (id, sender, receiver, amount, date, currency, state))
#     mysql.connection.commit()
#     cursor.close()
#
# def transactionThread(id, sender, receiver, amount, date, transaction_currecny, state, rsdEquivalent):
#     print('Transaction ', id, ' thread started ')
#     sleep(120)  # TODO
#
#     transaction = Transaction(id, sender, receiver, amount, date, transaction_currecny, state, rsdEquivalent)
#     transactions_queue.put(transaction)
#

# def transactionProcess(queue: Queue):
#     while (1):
#         transaction = queue.get()
#
#         print('Transaction ', transaction.id, ' process started ')
#
#         # otvaranje nove konekcije u threadu
#         mydb1 = MySQLdb.connect(host="localhost",
#                                 user="root",
#                                 passwd="",
#                                 db="bank")
#         cursor = mydb1.cursor()
#
#         cursor.execute(''' SELECT balance FROM user WHERE email = %s ''', (transaction.sender,))
#         response = cursor.fetchone()
#         cursor.close()
#         senderAccountBalance = float(response[0])
#
#         cursor = mydb1.cursor()
#         if senderAccountBalance < transaction.rsdEquivalent:
#             # Transaction Fail (Has no money)
#             cursor.execute(''' UPDATE transaction SET state = %s WHERE ID = %s''', ('FAIL', transaction.id,))
#             print('\nTransaction ', transaction.id, 'process Fail')
#         else:
#             # Transcation Success (Has money)
#             cursor.execute(''' UPDATE transaction SET state = %s WHERE ID = %s''', ('SUCCESS', transaction.id,))
#             cursor.execute(''' UPDATE user SET balance = balance - %s WHERE email = %s''',
#                            (transaction.rsdEquivalent, transaction.sender,))
#             cursor.execute(''' UPDATE user SET balance = balance + %s WHERE email = %s OR accountNum = %s''',
#                            (transaction.rsdEquivalent, transaction.receiver, transaction.receiver,))
#             print('\nTransaction ', transaction.id, 'process Success')
#         mydb1.commit()
#         cursor.close()