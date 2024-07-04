from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed  
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from lifegiver.models import Donor, Hospital
from flask_login import current_user




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

