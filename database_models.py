from __init__ import db
from wtforms.validators import ValidationError
from Models import User, PaymentCard, OnlineAccount, Transaction


# db models
class User(db.Model, User.User):  # if some error occur check User Mixin class
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(35), nullable=False)
    town = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    cardNumber = db.Column(db.String(18))
    onlineCardNumber = db.Column(db.String(18))
    verified = db.Column(db.Boolean, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    payments_cards = db.relationship('PaymentCard', backref='owner', lazy=True)
    # backref arg - that allows automatic generation of a new relationship
    # that will be automatically added to ORM mapping for the related class
    # lazy arg - sqlalchemy will load data in one go


    @property
    def is_verified(self):
        return self.verified

    def get_id(self):
        return self.id

    @staticmethod
    def validate_username(username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                "That username already exists. Please choose a different one"
            )

    @staticmethod
    def validate_card_number(card_number):
        existing_user_card_number = User.query.filter_by(cardNumber=card_number.data).first()
        if not existing_user_card_number:
            raise ValidationError(
                "Card is not valid."
            )
            return False
        return True


class PaymentCard(db.Model, PaymentCard.PaymentCard):
    id = db.Column(db.Integer, primary_key=True)
    card_number = db.Column(db.Integer, unique=True, nullable=False)
    user_name = db.Column(db.String(20), nullable=False)
    expiry_data = db.Column(db.String(5), nullable=False)
    security_code = db.Column(db.Integer, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # using lower case because we are referencing table
    balance = db.Column(db.Integer, nullable=False)
    # foreign key - specify that we have relationship to the user model

    # def __repr__(self):
    # return f"Payment card('{self.user_name}' {self.expiry_data})}"

    # @staticmethod
    # def payoff(amount, card_num):
    #     payment_card = PaymentCard.query.filter_by(card_number=card_num).first()
    #     if payment_card.balance >= amount:
    #         payment_card.balance -= amount
    #         return True
    #
    #     # TODO else throw error

    # @property
    # def add_funds(self, amount, card_num):
    #     payment_card = PaymentCard.query.filter_by(card_number=card_num.data)
    #     payment_card.balance += amount
    #


class OnlineAccount(db.Model, OnlineAccount.OnlineAccount):
    id = db.Column(db.Integer, primary_key=True)
    card_number = db.Column(db.Integer, unique=True, nullable=False)
    user_name = db.Column(db.String(20), nullable=False)
    user_email = db.Column(db.String(20), unique=True, nullable=False)
    balance = db.Column(db.Integer, nullable=False)
    # foreign key - specify that we have relationship to the user model

    # def __repr__(self):
    # return f"Payment card('{self.user_name}' {self.expiry_data})}"

    # @staticmethod
    # def payoff(amount, card_num):
    #     payment_card = PaymentCard.query.filter_by(card_number=card_num).first()
    #     if payment_card.balance >= amount:
    #         payment_card.balance -= amount
    #         return True
    #
    #     # TODO else throw error

    # @property
    # def add_funds(self, amount, card_num):
    #     payment_card = PaymentCard.query.filter_by(card_number=card_num.data)
    #     payment_card.balance += amount
    #


class Transaction(db.Model, Transaction.Transaction):
    id = db.Column(db.Integer, primary_key=True)
    transaction_number = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(20), nullable=False)
    receiver = db.Column(db.String(20), nullable=False)
    date = db.Column(db.Date, nullable=False)
    state = db.Column(db.String(20), nullable=False)  # TODO napravi sa enumom
    amount = db.Column(db.Integer, nullable=False)


