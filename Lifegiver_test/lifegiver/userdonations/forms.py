from flask_wtf import FlaskForm
from datetime import datetime
from wtforms import SubmitField, DateTimeField
from wtforms.validators import DataRequired

class UserDonationForm(FlaskForm):
    donation_date = DateTimeField('Donation Date', default=datetime.now, validators=[DataRequired()])
    submit = SubmitField('Donate Now')