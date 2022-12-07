from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from os import path


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()  # allow our app and flask to work together, to handle things when logining in ...


def create_app():
    app = Flask(__name__)
    # /// relative path and //// is absolute
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # connects app to db
    app.config['SECRET_KEY'] = 'admin'  # secret key is used to secure session cookie
    db .init_app(app)  # creates db instance
    bcrypt.init_app(app)

    from auth import auth
    from views import views

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    login_manager.init_app(app)
    login_manager.login_view = "login"

    return app


