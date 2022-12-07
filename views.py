from flask import Blueprint, render_template
from flask_login import login_required

views = Blueprint('views', __name__)


@views.route('/')  # paste url of our app
def index():
    return render_template('index.html')


@views.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')
