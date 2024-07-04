from flask_wtf import FlaskForm
from datetime import datetime 
from wtforms import StringField, SubmitField, SelectField, DateTimeField
from wtforms.validators import DataRequired


    
# Form for the CRUD operations of donation requests
class CRUDRequestForm(FlaskForm):
    hospital_id = StringField('Hospital ID', validators=[DataRequired()])
    # to change later to be a selectfield later
    blood_type = SelectField('Blood Type', choices=[('O-', 'O-'), ('O+', 'O+'), ('A-', 'A-'), ('A+', 'A+'), ('B-', 'B-'), ('B+', 'B+'), ('AB-', 'AB-'), ('AB+', 'AB+')], validators=[DataRequired()])
    request_date = DateTimeField('Request Date', default=datetime.now, validators=[DataRequired()])
    status = SelectField('Status', choices=[('pending', 'Pending'), ('fulfilled', 'Fulfilled'), ('failed', 'Failed')], validators=[DataRequired()])
    expiration_date = DateTimeField('Expiration Date', validators=[DataRequired()])
    submit = SubmitField('Submit Request')

