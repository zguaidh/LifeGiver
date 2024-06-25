from flask_wtf import FlaskForm
from datetime import datetime
from flask_wtf.file import FileField, FileAllowed  
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from lifegiver.models import Donor, Hospital
from flask_login import current_user

class DonorRegistrationForm(FlaskForm):
    first_name = StringField('First Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
   
    # Move this part to the dashboard

    age = IntegerField('Age', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=45)])
    blood_type = SelectField('Blood Type', choices=[('O-', 'O-'), ('O+', 'O+'), ('A-', 'A-'), ('A+', 'A+'), ('B-', 'B-'), ('B+', 'B+'), ('AB-', 'AB-'), ('AB+', 'AB+')], validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired(), Length(max=500)])
    city = StringField('City', validators=[DataRequired(), Length(max=100)])
    province = StringField('Province', validators=[DataRequired(), Length(max=100)])
    zip_code = StringField('Zip Code', validators=[DataRequired(), Length(max=45)])
    country = StringField('Country', validators=[DataRequired(), Length(max=100)])
    national_id = StringField('National ID', validators=[DataRequired(), Length(max=45)])

    submit = SubmitField('Sign Up')

    def validate_national_id(self, national_id):
        donor = Donor.query.filter_by(national_id=national_id.data).first()
        if donor:
            raise ValidationError('This National ID is already in use. Please verify for any errors')

    def validate_email(self, email):
        donor = Donor.query.filter_by(email=email.data).first()
        if donor:
            raise ValidationError('That email is taken. Please choose a different one.')

class DonorLoginForm(FlaskForm):

    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class HospitalLoginForm(FlaskForm):


    barcode = StringField('Barcode',
                           validators=[DataRequired(), Length(min=2, max=120)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    def validate_username(self, barcode):
        hospital = Hospital.query.filter_by(barcode=hospital.data).first()
        if not hospital:
            raise ValidationError('Please check your barcode')
        

class HospitalRegistrationForm(FlaskForm):

    name = StringField('Name',
                           validators=[DataRequired(), Length(min=2, max=120)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=45)])
    street = StringField('Street', validators=[DataRequired(), Length(max=500)])
    city = StringField('City', validators=[DataRequired(), Length(max=100)])
    province = StringField('Province', validators=[DataRequired(), Length(max=100)])
    zip_code = StringField('Zip Code', validators=[DataRequired(), Length(max=45)])
    country = StringField('Country', validators=[DataRequired(), Length(max=100)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Register')
    
# to prevent the "IntegrityError" when trying to log with an existing name or email:
    def validate_username(self, username):
        donor = Hospital.query.filter_by(name=username.data).first()
        if donor:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        donor = Hospital.query.filter_by(email=email.data).first()
        if donor:
            raise ValidationError('That email is taken. Please choose a different one.')



class DonorUpdatingForm(FlaskForm):
    first_name = StringField('First Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    age = IntegerField('Age', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=45)])
    blood_type = SelectField('Blood Type', choices=[('O-', 'O-'), ('O+', 'O+'), ('A-', 'A-'), ('A+', 'A+'), ('B-', 'B-'), ('B+', 'B+'), ('AB-', 'AB-'), ('AB+', 'AB+')], validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired(), Length(max=500)])
    city = StringField('City', validators=[DataRequired(), Length(max=100)])
    province = StringField('Province', validators=[DataRequired(), Length(max=100)])
    zip_code = StringField('Zip Code', validators=[DataRequired(), Length(max=45)])
    country = StringField('Country', validators=[DataRequired(), Length(max=100)])
    national_id = StringField('National ID', validators=[DataRequired(), Length(max=45)])
    picture = FileField('Update Account Picture', validators=[FileAllowed(['jpg', 'png'])])
    

    submit = SubmitField('Update')

class HospitalUpdatingForm(FlaskForm):
    name = StringField('Name',
                            validators=[DataRequired(), Length(min=2, max=225)])
    email = StringField('Email',
                            validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=45)])
    street = StringField('Street', validators=[DataRequired(), Length(max=500)])
    city = StringField('City', validators=[DataRequired(), Length(max=100)])
    province = StringField('Province', validators=[DataRequired(), Length(max=100)])
    zip_code = StringField('Zip Code', validators=[DataRequired(), Length(max=45)])
    country = StringField('Country', validators=[DataRequired(), Length(max=100)])
    picture = FileField('Update Account Picture', validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update')



    def validate_username(self, username):
        # check if the updated username is different than the current username
        if username.data != current_user.name:
            # check if the name is already used
            hospital = Hospital.query.filter_by(name=username.data).first()
            if hospital:
                raise ValidationError('That Name is taken. Please choose a different one.')

    def validate_email(self, email):
        # check if the updated username is different than the current username
        if email.data != current_user.email:
            # check if the mail is already used
            hospital = Hospital.query.filter_by(email=email.data).first()
            if hospital:
                raise ValidationError('That email is taken. Please choose a different one.')
            
# Form for the CRUD operations of donation requests
class CRUDRequestForm(FlaskForm):
    hospital_id = StringField('Hospital ID', validators=[DataRequired()])
    # to change later to be a selectfield later
    blood_type = SelectField('Blood Type', choices=[('O-', 'O-'), ('O+', 'O+'), ('A-', 'A-'), ('A+', 'A+'), ('B-', 'B-'), ('B+', 'B+'), ('AB-', 'AB-'), ('AB+', 'AB+')], validators=[DataRequired()])
    request_date = DateTimeField('Request Date', default=datetime.now, validators=[DataRequired()])
    status = SelectField('Status', choices=[('pending', 'Pending'), ('fulfilled', 'Fulfilled'), ('failed', 'Failed')], validators=[DataRequired()])
    expiration_date = DateTimeField('Expiration Date', validators=[DataRequired()])
    submit = SubmitField('Submit Request')

# Form for the CRUD operations of urgent donation requests
class CRUDUrgentRequestForm(FlaskForm):
    hospital_id = StringField('Hospital ID', validators=[DataRequired()])
    # to change later to be a selectfield later
    blood_type = SelectField('Blood Type', choices=[('O-', 'O-'), ('O+', 'O+'), ('A-', 'A-'), ('A+', 'A+'), ('B-', 'B-'), ('B+', 'B+'), ('AB-', 'AB-'), ('AB+', 'AB+')], validators=[DataRequired()])
    request_date = DateTimeField('Request Date', default=datetime.now, validators=[DataRequired()])
    expiration_date = DateTimeField('Expiration Date', validators=[DataRequired()])
    submit = SubmitField('Submit  Urgent Request')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = Donor.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class UserDonationForm(FlaskForm):
    donation_date = DateTimeField('Donation Date', default=datetime.now, validators=[DataRequired()])
    submit = SubmitField('Donate Now')

    