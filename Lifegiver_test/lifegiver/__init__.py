from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from lifegiver.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
# the redirection view for the login requied when trying to acces the /donor_dashboard or /hospital_dashboard 
login_manager.login_view = 'main.home'
# to improve the form of the message displayed when trying to access the account without being logged in
login_manager.login_message_category = 'info'
mail = Mail()






def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from lifegiver.donationrequests.route import donationrequests
    from lifegiver.donors.route import donors
    from lifegiver.hospitals.route import hospitals
    from lifegiver.urgentrequests.route import urgentrequests
    from lifegiver.userdonations.route import userdonations
    from lifegiver.main.route import main
    from lifegiver.errors.handelers import errors
    app.register_blueprint(donationrequests)
    app.register_blueprint(donors)
    app.register_blueprint(hospitals)
    app.register_blueprint(urgentrequests)
    app.register_blueprint(userdonations)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app