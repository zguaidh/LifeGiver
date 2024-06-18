from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# the redirection view for the login requied when trying to acces the /donor_dashboard or /hospital_dashboard 
login_manager.login_view = 'home'
# to improve the form of the message displayed when trying to access the account without being logged in
login_manager.login_message_category = 'info'


"""
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/db_name'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
"""

from lifegiver import route

