from datetime import datetime, timedelta
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# from itsdangerous import Serializer, BadSignature, SignatureExpired
# from itsdangerous import TimedSerializer as Serializer
#from itsdangerous import URLSafeTimedSerializer as Serializer
from lifegiver import db, login_manager
from flask_login import UserMixin
from flask import session, current_app
import json

@login_manager.user_loader
def load_user(user_id):
    user_type = session.get('user_type')  # Assuming 'user_type' is stored in the session
    if user_type == 'donor':
        return Donor.query.get(int(user_id))
    elif user_type == 'hospital':
        return Hospital.query.get(int(user_id))
    return None


class Donor(db.Model, UserMixin):
    __tablename__ = 'donor'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    age = db.Column(db.Integer, nullable=False)
    
    # make the nullables True

    phone_number = db.Column(db.String(45), nullable=False)
    blood_type = db.Column(db.Enum('O-', 'O+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+'), nullable=False)
    street = db.Column(db.String(500), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    province = db.Column(db.String(100), nullable=False)
    zip_code = db.Column(db.String(45), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    registration_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    national_id = db.Column(db.String(45), unique=True, nullable=False)
    # Tobe able to usr Google Maps APIs
    lat = db.Column(db.Float, nullable=True)
    lng = db.Column(db.Float, nullable=True)
    # Implemet the method to increment the count later
    donation_count = db.Column(db.Integer, default=0)
    # add an attribute for the coordinates as a dictionary

    # One Donor has many UserDonations
    donor_donations = db.relationship('UserDonation', backref='donor', lazy=True)

    # method to increment the donation count:
    def increment_donation_count(self):
        self.donation_count += 1
        db.session.commit()

    # method that creates tokens 
    def get_reset_token(self, expires_sec=1800):
        # Debugging: Print the type and value of app.config['SECRET_KEY']
        print(f"SECRET_KEY type: {type(current_app.config['SECRET_KEY'])}")
        print(f"SECRET_KEY value: {current_app.config['SECRET_KEY']}")


        s = Serializer(current_app.config['SECRET_KEY'], expires_sec) # passing the expiration time and our secret key set in the __init__ file  
        # For debbuging : explicitly encode the payload as bytes
        payload = {'user_id': self.id}
        token = s.dumps(payload)
        return token.decode('utf-8')
#        token = s.dumps({'user_id': self.id}).decode('utf-8') # getting our token that contains a payload of the current user id
#        return token
#        return s.dumps({'user_id': self.id}, salt=app.config['SECURITY_PASSWORD_SALT']).decode('utf-8')
        
    # method to verify the token , we will use it in the reset_token route
    @staticmethod # since this method deosnt do anything with the instance of this user
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Donor.query.get(user_id)

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.email}', '{self.image_file}')"
    def __repr__(self):
        return f"Donor(id={self.id}, first_name='{self.first_name}', last_name='{self.last_name}', email='{self.email}', image_file='{self.image_file}', blood_type='{self.blood_type}', donation_count={self.donation_count}, )"

class Hospital(db.Model, UserMixin):
    __tablename__ = 'hospital'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(225), nullable=False)
#    address = db.Column(db.String(500), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default1.png')
    street = db.Column(db.String(500), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    province = db.Column(db.String(100), nullable=True)
    zip_code = db.Column(db.String(45), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    phone_number = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(125), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    barcode = db.Column(db.String(100), unique=True, nullable=False)

    # Tobe able to usr Google Maps APIs
    lat = db.Column(db.Float, nullable=True)
    lng = db.Column(db.Float, nullable=True)

    
    # One hospital can have many UserDonations
    hospital_donations = db.relationship('UserDonation', backref='hospital_donation', lazy=True)
    
    # One hospital can have multiple DonationRequests
    hospital_requests = db.relationship('DonationRequest', backref='hospital_request', lazy=True)
    
    # One hospital can have many urgentrequests
    urgent_requests = db.relationship('UrgentRequest', backref='hospital_urgent_request', lazy=True)

    def __repr__(self):
        return f"Hospital(id={self.id}, barcode='{self.barcode}', email='{self.email}')"

class UserDonation(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    donation_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    donor_id = db.Column(db.Integer, db.ForeignKey('donor.id'), nullable=False)
    request_id = db.Column(db.Integer, db.ForeignKey('donation_request.id'), nullable=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)

    def __repr__(self):
        return f"Donation(id={self.id}, donation_date='{self.donation_date}', donor_id={self.donor_id}, hospital_id={self.hospital_id})"
    
class DonationRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)
    blood_type = db.Column(db.Enum('O-', 'O+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+'), nullable=False)
    request_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    status = db.Column(db.Enum('pending', 'fulfilled', 'failed'), nullable=False)
#   expiration_date = db.Column(db.DateTime, nullable=True)
# Search how to change it to a calendar
    expiration_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now() + timedelta(days=90))
    
    # many UserDonation entries can belong to one DonationRequest
    request_donations = db.relationship('UserDonation', backref='donation_request', lazy=True)

#   def __init__(self, hospital_id, blood_type, status):
#        self.hospital_id = hospital_id
#        self.blood_type = blood_type
#        self.status = status
#         self.expiration_date = datetime.now() + timedelta(days=60)
    
    def __repr__(self):
        return f"Request(id={self.id}, hospital_id={self.hospital_id}, blood_type='{self.blood_type}', status='{self.status}', request_date='{self.request_date}', expiration_date='{self.expiration_date}')"
    

class UrgentRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)
    blood_type = db.Column(db.Enum('O-', 'O+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+'), nullable=False)
    request_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    expiration_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now() + timedelta(days=15))

    
    def __repr__(self):
        return f"EmergencyRequest(id={self.id}, hospital_id={self.hospital_id}, blood_type='{self.blood_type}', start_date='{self.start_date}', end_date='{self.end_date}')"


 