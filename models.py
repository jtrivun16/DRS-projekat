from __init__ import db
from wtforms.validators import ValidationError
from  Models import User


# db models
class User(db.Model, User.User):  # if some error occur check User Mixin class
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(35), nullable=False)
    town = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(80), nullable=False)

    @staticmethod
    def validate_username(username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                "That username already exists. Please choose a different one"
            )
