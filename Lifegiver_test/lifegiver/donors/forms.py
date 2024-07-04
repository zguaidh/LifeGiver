from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed  
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from lifegiver.models import Donor

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

