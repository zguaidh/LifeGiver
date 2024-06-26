import os
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
# load it to an environment variable later
# app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

# export it to an envirenment variable later
app.config['GOOGLE_MAPS_API_KEY'] = 'AIzaSyAckhaG8lpWrO3lI8shmnOBrTQzeQCV-ew'
app.config['SECRET_KEY'] = '28b95654638c2558741386d9c6649456b49fcdee5de3616da207cc86f52c2f34'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# the redirection view for the login requied when trying to acces the /donor_dashboard or /hospital_dashboard 
login_manager.login_view = 'home'
# to improve the form of the message displayed when trying to access the account without being logged in
login_manager.login_message_category = 'info'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] =  587
app.config['MAIL_USE_TLS'] = True
# hidding the email and password in an environement variable
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
app.config['MAIL_DEFAULT_CHARSET'] = 'utf-8'
# we should initialize the extension after setting the five configurations
mail = Mail(app)



"""
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/db_name'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
"""

from lifegiver import route

