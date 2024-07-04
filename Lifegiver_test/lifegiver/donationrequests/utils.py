from flask import url_for
from lifegiver import mail
from lifegiver.models  import Donor
from flask_mail import Message
from haversine import haversine, Unit

# Method to send notifications to nearby donors
def send_notification_email(donor, message):
    msg = Message('Urgent Blood Donation Request', sender='noreply@demo.com', recipients=[donor.email])
    msg.body = message
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


# method to calculate the distances using the haversine formula
def get_distance(lat1, lng1, lat2, lng2):
    return haversine((lat1, lng1), (lat2, lng2), unit=Unit.KILOMETERS)


def return_match(blood_type):
    matching_types = []
    if blood_type[1] == '+':
        matching_types.extend(('O-', 'O+'))
        if blood_type[0] != 'O':
            matching_types.extend((blood_type[0]+'-', blood_type))
    
    elif blood_type[1] == '-':
        matching_types.append('O-')
        if blood_type[0] != 'O':
            matching_types.append(blood_type)
        
    elif blood_type[2] == '-':
        matching_types.extend(('O-', 'A-', 'B-', 'AB-'))

    else:
        matching_types.extend(('O-', 'A-', 'B-', 'AB-', 'O+', 'A+', 'B+', 'AB+'))
        
    return matching_types

def find_nearby_donors(hospital, blood_type):
    matching_types = return_match(blood_type)
    print(matching_types)
    nearby_donors = []
    for i in matching_types:
        all_donors = Donor.query.filter_by(blood_type=i).all()
        print(i)
        for donor in all_donors:
            distance = get_distance(hospital.lat, hospital.lng, donor.lat, donor.lng)
            if distance <= 30:
                nearby_donors.append(donor)
    
    print(nearby_donors)
    return nearby_donors


















# send a msg to the donor
def send_donation_don_email(user, request, hospital, user_donation):
    msg = Message(' Donation Confirmation',
                  sender='noreply.lifegiver@gmail.com',
                  recipients=[user.email]) # reset the sender to the email comming from the domain later
    msg.body = f'''Dear {user.first_name},

Thank you for your generous decision to donate blood. Here are the details of your donation:

Hospital: {hospital.name}
Location: {hospital.street}, {hospital.city}, {hospital.province}, {hospital.zip_code}, {hospital.country}
Phone: {hospital.phone_number}
Email: {hospital.email}

Donation Request Information:
- Blood Type: {request.blood_type}
- Request Date: {request.request_date}
- Expiration Date: {request.expiration_date}

Please ensure that you arrive at the hospital at {user_donation.donation_date}. If you have any questions or need to reschedule, feel free to contact the hospital directly.

Thank you for using LifeGiver!

{url_for('main.home', _external=True)}
'''
    mail.send(msg)


# send a msg to the hospital
def send_donation_hos_email(user, request_id, user_donation):
    msg = Message(' Your Donation Request has been approved',
                  sender='noreply.lifegiver@gmail.com',
                  recipients=[user.email]) # reset the sender to the email comming from the domain later
    msg.body = f'''Dear {user.name},

Your urgent request has been approved by a Donor.

Please ensure that you are prepared to receive the donor at {user_donation.donation_date} and facilitate the donation process.

We kindly remind you to update the donation request information after the  the donation has been completed.

{url_for('urgentrequests.update_urgent_request', urgent_request_id=request_id, _external=True)}

Thank you for using LifeGiver!
{url_for('main.home', _external=True)}
'''
    mail.send(msg)




