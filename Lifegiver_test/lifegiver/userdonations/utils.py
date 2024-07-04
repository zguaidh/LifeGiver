from flask import url_for
from lifegiver import mail
from flask_mail import Message


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
