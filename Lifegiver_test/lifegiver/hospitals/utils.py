import string
import random
import secrets
from PIL import Image
import os
from flask import url_for
from lifegiver import mail
from lifegiver.models  import Donor
from flask_mail import Message
from flask import current_app
import requests
from haversine import haversine, Unit

# Method that take the adress and return the latitude and longeture
def geocode_address(address):
    print(f"requests type: {type(requests)}") 
    response = requests.get(
        'https://maps.googleapis.com/maps/api/geocode/json',
        params={'address': address, 'key': current_app.config['GOOGLE_MAPS_API_KEY']}
    )
    data = response.json()
    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    return None, None




# method to make serial numbers:
def make_serial(count):
    all_char = string.ascii_letters + string.digits
    serial_list = []
    while count > 0:
        random_number = random.randint(0, len(all_char) - 1)
        random_character = all_char[random_number]
        serial_list.append(random_character)
        count -= 1
    return ("".join(serial_list))
# send a serial number to the newly created hospital
def send_barcode_email(user, barcode):
    msg = Message(' Your hispital Barcode',
                  sender='noreply.lifegiver@gmail.com',
                  recipients=[user.email]) # reset the sender to the email comming from the domain later
    msg.body = f'''Dear {user.name},
Your account has been created successfully.
Your serial number is:  {barcode}
Please keep this serial number safe, as you will need it to log in.

Login now : {url_for('hospitals.hospital_login', _external=True)}
'''
    msg.charset = 'utf-8'
    mail.send(msg)




def save_picture(form_picture):
    # to prevent that the name of the uploaded image collide with an existing name we will randomise the name of the image as hex

    random_hex = secrets.token_hex(8)
    # get the extention of the picture, lets usr the _ the throw away the picture name variable cuz it wont be used
    _, f_ext = os.path.splitext(form_picture.filename)
    # combining the random hex and the file extention to create the file name of the image to save
    picture_fn = random_hex + f_ext
    # get the full path to where we are going to save our picture using root_path attribute of our app
    picture_path = os.path.join(current_app.root_path, 'static/images', picture_fn)
    

# resizing the images befor saving them using the pillow package
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
# saving resized picture in the full path 
    i.save(picture_path)

    return picture_fn


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



# using flask-mail flask extention to send emails:
def send_reset_email(user):
    token = user.get_reset_token() # Using the get method from our models class Donor
    msg = Message(' Password Reset Request',
                  sender='noreply.lifegiver@gmail.com',
                  recipients=[user.email]) # reset the sender to the email comming from the domain later
    msg.body = f'''Hello from LifeGiver!

You are receiving this email because you or someone else has requested
a password for your user account.

This mail can be safely ignored if you did not request a password reset.

If it was you, you can sign up for an account using the link below.

{url_for('hospitals.reset_token', token=token, _external=True)}

Thank you for using LifeGiver!
{url_for('main.home', _external=True)}

'''
  # we are using the external in order to get an absolute url instead of a relative url <= this one needs the full domain in the link
    mail.send(msg)











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