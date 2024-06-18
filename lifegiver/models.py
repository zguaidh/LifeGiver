from datetime import datetime, timedelta
from lifegiver import db, login_manager
from flask_login import UserMixin
from flask import session

@login_manager.user_loader
def load_user(user_id):
    user_type = session.get('user_type')  # Assuming 'user_type' is stored in the session
    if user_type == 'donor':
        return Donor.query.get(int(user_id))
    elif user_type == 'hospital':
        return Hospital.query.get(int(user_id))
    return None


class Donor(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    age = db.Column(db.Integer, nullable=False)
    
    # make the nullables True

    phone_number = db.Column(db.String(45), nullable=False)
    blood_type = db.Column(db.String(45), nullable=False)
    street = db.Column(db.String(500), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    province = db.Column(db.String(100), nullable=False)
    zip_code = db.Column(db.String(45), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    registration_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    national_id = db.Column(db.String(45), unique=True, nullable=False)
    donation_count = db.Column(db.Integer, default=0)

    # One Donor has many UserDonations
    donor_donations = db.relationship('UserDonation', backref='donor', lazy=True)

    def __repr__(self):
        return f"Donor(id={self.id}, username='{self.username}', email='{self.email}', image_file='{self.image_file}', blood_type='{self.blood_type}', donation_count={self.donation_count})"

class Hospital(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
#   name = db.Column(db.String(225), nullable=False)
#   address = db.Column(db.String(500), nullable=False)
#   phone_number = db.Column(db.String(45), nullable=False)
#   email = db.Column(db.String(125), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    barcode = db.Column(db.String(100), unique=True, nullable=False)
    
    # One hospital can have many UserDonations
    hospital_donations = db.relationship('UserDonation', backref='hospital', lazy=True)
    
    # One hospital can have multiple DonationRequests
    hospital_requests = db.relationship('DonationRequest', backref='hospital', lazy=True)
    
    # One hospital can have many urgentrequests
    emergency_requests = db.relationship('UrgentRequest', backref='hospital', lazy=True)

    def __repr__(self):
        return f"Hospital(id={self.id}, barcode='{self.barcode}')"

class UserDonation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    donation_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    status = db.Column(db.Enum('requested', 'voluntary'), nullable=False)
    donor_id = db.Column(db.Integer, db.ForeignKey('donor.id'), nullable=False)
    request_id = db.Column(db.Integer, db.ForeignKey('donation_request.id'), nullable=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)

    def __repr__(self):
        return f"Donation(id={self.id}, donation_date='{self.donation_date}', status='{self.status}', donor_id={self.donor_id}, hospital_id={self.hospital_id})"
    
class DonationRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)
    blood_type = db.Column(db.String(45), nullable=False)
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
    blood_type = db.Column(db.String(45), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    end_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now() + timedelta(days=15))

    def __repr__(self):
        return f"EmergencyRequest(id={self.id}, hospital_id={self.hospital_id}, blood_type='{self.blood_type}', start_date='{self.start_date}', end_date='{self.end_date}')"


 