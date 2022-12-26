from __init__ import db
from wtforms.validators import ValidationError
from  Models import User, PaymentCard


# db models
class User(db.Model, User.User):  # if some error occur check User Mixin class
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(35), nullable=False)
    town = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    cardNumber = db.Column(db.Integer, nullable=False, unique=True)
    verified = db.Column(db.Boolean, nullable= False)
    password = db.Column(db.String(255), nullable=False)
    payments_cards = db.relationship('PaymentCard', backref='owner', lazy=True)
    # backref arg - that allows automatic generation of a new relationship
    # that will be automatically added to ORM mapping for the related class
    # lazy arg - sqlalchemy will load data in one go

    @staticmethod
    def validate_username(username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                "That username already exists. Please choose a different one"
            )
            
    @staticmethod
    def validate_cardNumber(cardNumber):
        existing_user_cardNumber = User.query.filter_by(cardNumber=cardNumber.data).first()
        if existing_user_cardNumber:
            raise ValidationError(
                "That card number already exists."
            )


class PaymentCard(db.Model, PaymentCard.PaymentCard):
    id = db.Column(db.Integer, primary_key=True)
    card_number = db.Column(db.Integer, unique=True, nullable=False)
    user_name = db.Column(db.String(20), nullable=False)
    expiry_data = db.Column(db.String(5), nullable=False)
    security_code = db.Column(db.Integer, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # using lower case because we are referencing table
    # foreign key - specify that we have relationship to the user model

    # def __repr__(self):
    # return f"Payment card('{self.user_name}' {self.expiry_data})}"
