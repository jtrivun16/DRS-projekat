from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from datetime import datetime

import Models.User

# set up app
app = Flask(__name__)
# /// relative path and //// is absolute
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # connects app to db
app.config['SECRET_KEY'] = 'admin'  # secret key is used to secure session cookie
db = SQLAlchemy(app)  # creates db instance
bcrypt = Bcrypt(app)

login_manager = LoginManager()  # allow our app and flask to work together, to handle things when logining in ...
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader  # reload user obj from the user id stored in the session
def load_user(user_id):
    return User.query.get(user_id)


# class Todo(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    content = db.Column(db.String(200), nullable=False)
#    date_created = db.Column(db.DateTime, default=datetime.utcnow)

#   def __repr__(self):
#      return '<Task %r>' % self.id


class User(db.Model, Models.User.User):  # if some error occur check User Mixin class
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


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})

    first_name = StringField(validators=[InputRequired(), Length(
        min=3, max=20)], render_kw={"placeholder": "FirstName"})

    last_name = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "LastName"})

    address = StringField(validators=[InputRequired(), Length(
        min=4, max=35)], render_kw={"placeholder": "Address"})

    town = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Town"})

    country = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Country"})

    phone_number = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Phone number"})

    email = EmailField(validators=[InputRequired()], render_kw={'placeholder': "example@gmail.com"})

    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Register")

    @staticmethod
    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                "That username already exists. Please choose a different one"
            )


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")


# create index route
@app.route('/')  # paste url of our app
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                load_user(user.id)

                login_user(user)
                return redirect(url_for('dashboard'))
                # return render_template('dashboard.html')
    else:
        return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    print("Hey Yo")
    if form.validate_on_submit():
        print("Hey  Yooooo")
        hashed_password = bcrypt.generate_password_hash(form.password.data)

        new_user = User(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data,
                        address=form.address.data, town=form.town.data,   country=form.country.data,
                        phone_number=form.phone_number.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    print(form.errors)
    return render_template('register.html', form=form)


if __name__ == "__main__":
    app.run(port=8000, debug=True)


