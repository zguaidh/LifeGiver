from flask import Blueprint
from flask import render_template, redirect, url_for
from lifegiver.models  import UrgentRequest
from flask_login import logout_user

main = Blueprint('main', __name__)

@main.route('/', methods=['POST', 'GET'], strict_slashes=False)
@main.route('/home', methods=['POST', 'GET'], strict_slashes=False)
def home():
    requests = UrgentRequest.query.all()
    return render_template('home.html', title='Home page', requests=requests)

# to check later if we gonna keep it
@main.route("/about", methods=['GET'], strict_slashes=False)
def about():
    return render_template('about.html', title='About page')


@main.route("/login", methods=['GET'], strict_slashes=False)
def login():
    return render_template('login_user_type.html', title='Login')


@main.route("/register", methods=['GET'], strict_slashes=False)
def register():
    return render_template('register_user_type.html', title='Registration')




@main.route("/logout")
def logout():

    logout_user()
    return redirect(url_for('main.home'))

