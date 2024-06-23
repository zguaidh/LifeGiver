import string
import random
import secrets
from PIL import Image
from datetime import datetime
import os
from flask import render_template, flash, redirect, url_for, request, session, abort
from lifegiver.forms import (DonorLoginForm, DonorRegistrationForm,
                             HospitalRegistrationForm, HospitalLoginForm,
                             DonorUpdatingForm, CRUDRequestForm, 
                             RequestResetForm, ResetPasswordForm,
                             CRUDUrgentRequestForm, HospitalUpdatingForm,
                             UserDonationForm)
from lifegiver import app, db, bcrypt, mail
from lifegiver.models  import Donor, Hospital, UserDonation, DonationRequest, UrgentRequest
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


@app.route('/', methods=['POST', 'GET'], strict_slashes=False)
@app.route('/home', methods=['POST', 'GET'], strict_slashes=False)
def home():
    return render_template('home.html', title='Home page')

# to check later if we gonna keep it
@app.route("/about", methods=['GET'], strict_slashes=False)
def about():
    return render_template('about.html', title='About page')



@app.route('/new_donor', methods=['GET', 'POST'], strict_slashes=False)
def new_donor():
    if current_user.is_authenticated:
        return redirect(url_for('donor_dashboard'))
    form = DonorRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        donor = Donor(username=form.username.data,
                     email=form.email.data,
                     password=hashed_password,
                     age=form.age.data,
                     phone_number=form.phone_number.data,
                     blood_type=form.blood_type.data,
                     street=form.street.data,
                     city=form.city.data,
                     province=form.province.data,
                     zip_code=form.zip_code.data,
                     country=form.country.data,
                     national_id=form.national_id.data)
        db.session.add(donor)
        db.session.commit()
        flash(f'Acount created for {form.username.data}!', 'success')
        return redirect(url_for('existing_donor'))
    return render_template('new_donor.html', title='New Donor registration', form=form)

@app.route('/existing_donor', methods=['GET', 'POST'], strict_slashes=False)
def existing_donor():
    if current_user.is_authenticated:
        return redirect(url_for('donor_dashboard'))
    form = DonorLoginForm()
    if form.validate_on_submit():
        donor = Donor.query.filter_by(email=form.email.data).first()
        if donor and bcrypt.check_password_hash(donor.password, form.password.data):
            login_user(donor, remember=form.remember.data)
            session['user_type'] = 'donor'
            # ternary conditional: to redirect the user to the the page he was tryinh to access befor logging in
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
        return redirect(url_for('existing_donor'))
    return render_template('existing_donor.html', title='Donor Login', form=form)

# method to make serial numbers:
def make_serial(count):
    all_char = string.ascii_letters + string.digits
    chars_count = len(all_char)
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
Your serial number is:  {barcode}.
Please keep this serial number safe, as you will need it to log in.

Login now : {url_for('hospital_login', _external=True)}
'''
    mail.send(msg)

# route for hospital registration:
@app.route('/hospital_registration', methods=['GET', 'POST'], strict_slashes=False)
def hospital_registration():
    # To manage the authentication of the hospital
     if current_user.is_authenticated:
        return redirect(url_for('hospital_dashboard'))
     form = HospitalRegistrationForm()
     if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        barcode = make_serial(15)
        hospital = Hospital(name=form.name.data,
                     email=form.email.data,
                     password=hashed_password,
                     phone_number=form.phone_number.data,
                     street=form.street.data,
                     city=form.city.data,
                     province=form.province.data,
                     zip_code=form.zip_code.data,
                     country=form.country.data,
                     barcode=barcode)
        db.session.add(hospital)
        db.session.commit()
        print(hospital.barcode)
        send_barcode_email(hospital, barcode)
        flash(f'Acount created for {form.name.data}, Your serial number has been sent to your email!', 'success')
        return redirect(url_for('hospital_login'))
     return render_template('hospital_registration.html', title='Hospital Registration', form=form)


# route fo rhospital login
@app.route('/hospital_login', methods=['GET', 'POST'], strict_slashes=False)
def hospital_login():
    # To manage the authentication of the hospital
     if current_user.is_authenticated:
        return redirect(url_for('hospital_dashboard'))
     form = HospitalLoginForm()
     if form.validate_on_submit():
#        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#        hospital = Hospital(barcode=form.barcode.data, password=hashed_password)
#        db.session.add(hospital)
#        db.session.commit()
        hospital = Hospital.query.filter_by(barcode=form.barcode.data).first()
        if hospital and bcrypt.check_password_hash(hospital.password, form.password.data):
            login_user(hospital, remember=form.remember.data)
            session['user_type'] = 'hospital'
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('hospital_dashboard'))
        else:
#        flash(f'The hospital {form.barcode.data} loged in successefuly!', 'success')
            flash('Login Unsuccessful. Please check barcode and password', 'danger')
        return redirect(url_for('hospital_login'))
     return render_template('hospital_login.html', title='Hospital Login', form=form)



def save_picture(form_picture):
    # to prevent that the name of the uploaded image collide with an existing name we will randomise the name of the image as hex

    random_hex = secrets.token_hex(8)
    # get the extention of the picture, lets usr the _ the throw away the picture name variable cuz it wont be used
    _, f_ext = os.path.splitext(form_picture.filename)
    # combining the random hex and the file extention to create the file name of the image to save
    picture_fn = random_hex + f_ext
    # get the full path to where we are going to save our picture using root_path attribute of our app
    picture_path = os.path.join(app.root_path, 'static/pics', picture_fn)
    

# resizing the images befor saving them using the pillow package
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
# saving resized picture in the full path 
    i.save(picture_path)

    return picture_fn

@app.route('/donor_dashboard', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def donor_dashboard():
    form = DonorUpdatingForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_File = save_picture(form.picture.data)
            current_user.image_file = picture_File

        current_user.username = form.username.data
        current_user.email=form.email.data
        current_user.age=form.age.data
        current_user.phone_number=form.phone_number.data
        current_user.blood_type=form.blood_type.data
        current_user.street=form.street.data
        current_user.city=form.city.data
        current_user.province=form.province.data
        current_user.zip_code=form.zip_code.data
        current_user.country=form.country.data
        current_user.national_id=form.national_id.data
        db.session.commit()
        flash('Your account has been updated successfuly!', 'success')
        return redirect(url_for('donor_dashboard'))
    # to make sure that the form will be populated with the existing data
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data=current_user.email
        form.age.data=current_user.age
        form.phone_number.data=current_user.phone_number
        form.blood_type.data=current_user.blood_type
        form.street.data=current_user.street
        form.city.data=current_user.city
        form.province.data=current_user.province
        form.zip_code.data=current_user.zip_code
        form.country.data=current_user.country
        form.national_id.data=current_user.national_id
    image_file = url_for('static', filename='pics/' + current_user.image_file)
    return render_template('donor_dashboard.html', title='Donor dashboard', image_file=image_file, form=form)

@app.route('/hospital_dashboard', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def hospital_dashboard():
    form = HospitalUpdatingForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_File = save_picture(form.picture.data)
            current_user.image_file = picture_File

        current_user.name = form.name.data
        current_user.email=form.email.data
        current_user.phone_number=form.phone_number.data
        current_user.street=form.street.data
        current_user.city=form.city.data
        current_user.province=form.province.data
        current_user.zip_code=form.zip_code.data
        current_user.country=form.country.data
        db.session.commit()
        flash('Your account has been updated successfuly!', 'success')
        return redirect(url_for('hospital_dashboard'))
    # to make sure that the form will be populated with the existing data
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data=current_user.email
        form.phone_number.data=current_user.phone_number
        form.street.data=current_user.street
        form.city.data=current_user.city
        form.province.data=current_user.province
        form.zip_code.data=current_user.zip_code
        form.country.data=current_user.country
        image_file = url_for('static', filename='pics/' + current_user.image_file)
    hospital_requests = DonationRequest.query.filter_by(hospital_id=current_user.id).all()
    hospital_urgent_requests = UrgentRequest.query.filter_by(hospital_id=current_user.id).all()
    requests_count = len(hospital_requests)
    urgent_requests_count = len(hospital_urgent_requests)
    return render_template('hospital_dashboard.html', title='Hospital dashboard', image_file=image_file, requests_count=requests_count, urgent_requests_count=urgent_requests_count, form=form)


@app.route("/logout")
def logout():

    logout_user()
    return redirect(url_for('home'))


# route for create operation for donation request
@app.route("/request/new", methods=['GET', 'POST'], strict_slashes=False)
@login_required
def new_request():
    form = CRUDRequestForm()
    if form.validate_on_submit():
        don_request = DonationRequest(
            hospital_id=current_user.id,
            blood_type=form.blood_type.data,
            request_date=form.request_date.data,
            status=form.status.data,
            expiration_date=form.expiration_date.data,
            hospital_request=current_user
        )
        db.session.add(don_request)
        db.session.commit()
        flash('Your Request has been created!', 'success')
        return redirect(url_for('requests'))
    elif request.method == 'GET':
        #the name of the field is id but it will show the barcode
        form.hospital_id.data = current_user.barcode
        # add the same line for the name
    return render_template('create_request.html', title='New Request',form=form, legend='Create Request') # the legend keywoed will be used to change the template legend (whether its a new post or an update)

@app.route('/requests', methods=['POST', 'GET'], strict_slashes=False)
def requests():
    page = request.args.get('page', 1, type=int)
    # we are going to use the query query.order_by(DonationRequest.request_date.desc()) to order our requests by date
    requests = DonationRequest.query.order_by(DonationRequest.request_date.desc()).paginate(page=page, per_page=5) # inteade of using .all() we gonna change it to .paginate() to get 10 requests per page

    return render_template('requests.html', title='Donation Requests page', requests=requests)

# route that takes the user to a specific request by id
@app.route('/don_request/<int:don_request_id>', methods=['POST', 'GET'], strict_slashes=False)
def don_request(don_request_id):
# replaced by the next line to manage also a 404 error when the request is not found
#    don_request = DonationRequest.query.get(don_request_id)
    don_request = DonationRequest.query.get_or_404(don_request_id)
    return render_template('request_by_id.html', title='A Request By ID page', request=don_request)

# route to update a donation request
@app.route('/don_request/<int:don_request_id>/update', methods=['POST', 'GET'], strict_slashes=False)
@login_required
def update_don_request(don_request_id):
# replaced by the next line to manage also a 404 error when the request is not found
#    don_request = DonationRequest.query.get(don_request_id)
    donrequest = DonationRequest.query.get_or_404(don_request_id)
    # give permission of updating just for the user who created the don_request
    if session.get('user_type') != 'hospital' or donrequest.hospital_id != current_user.id:
        abort(403)
    form = CRUDRequestForm()
    if form.validate_on_submit():
        donrequest.hospital_id=current_user.id
        donrequest.blood_type=form.blood_type.data
        donrequest.request_date=form.request_date.data
        donrequest.status=form.status.data
        donrequest.expiration_date=form.expiration_date.data
        db.session.commit()
        flash('Your Request has been updated!', 'success')
        return redirect(url_for('don_request', don_request_id=donrequest.id))
    elif request.method == 'GET':
    # managed to populate the forms with data 
        form.hospital_id.data=current_user.barcode
        form.blood_type.data=donrequest.blood_type
        form.request_date.data=donrequest.request_date
        form.status.data=donrequest.status
        form.expiration_date.data=donrequest.expiration_date
    
    return render_template('create_request.html', title='Update Request',form=form, legend='Update Request') # the legend keywoed will be used to the template legend (whether its a new post or an update)


# route to handle the deletion of a request
@app.route('/don_request/<int:don_request_id>/delete', methods=['POST'], strict_slashes=False)
@login_required
def delete_don_request(don_request_id):
    donrequest = DonationRequest.query.get_or_404(don_request_id)
    # Ensure only the hospital that created the request can delete it
    if session.get('user_type') != 'hospital' or donrequest.hospital_id != current_user.id:
        abort(403)
    db.session.delete(donrequest)
    db.session.commit()
    flash('Your request has been deleted!', 'success')
    return redirect(url_for('requests'))

# route to get all the requests posted by a specifique hospital when clicking on the hospital's barcode
# change the barcode to the name of hospital later
@app.route('/hospital/<string:name>', methods=['POST', 'GET'], strict_slashes=False)
def hospital_requests(name):
    page = request.args.get('page', 1, type=int)
    hospital = Hospital.query.filter_by(name=name).first_or_404()
    # we are going to use the query query.order_by(DonationRequest.request_date.desc()) to order our requests by date
    # also using the backref hospital_request
    hospital_requests = DonationRequest.query.filter_by(hospital_request=hospital)\
            .order_by(DonationRequest.request_date.desc())\
            .paginate(page=page, per_page=5) # inteade of using .all() we gonna change it to .paginate() to get 10 requests per page

    return render_template('hospital_requests.html', title='Hospital Requests page', requests=hospital_requests, hospital=hospital)






# route for create operation for Urgent request
@app.route("/urgent_request/new", methods=['GET', 'POST'], strict_slashes=False)
@login_required
def new_urgent_request():
    form = CRUDUrgentRequestForm()
    if form.validate_on_submit():
        urgent_don_request = UrgentRequest(
            hospital_id=current_user.id,
            blood_type=form.blood_type.data,
            request_date=form.request_date.data,
            expiration_date=form.expiration_date.data,
            hospital_urgent_request=current_user
        )
        db.session.add(urgent_don_request)
        db.session.commit()

        flash('Your Urgent Request has been created!', 'success')
        return redirect(url_for('urgent_requests'))
    elif request.method == 'GET':
        #the name of the field is id but it will show the barcode
        form.hospital_id.data = current_user.barcode
        # add the same line for the name
    return render_template('create_urgent_request.html', title='New Urgent Request',form=form, legend='Create Urgent Request') # the legend keywoed will be used to change the template legend (whether its a new post or an update)

# route for all urgent requests
@app.route('/urgent_requests', methods=['POST', 'GET'], strict_slashes=False)
def urgent_requests():
    page = request.args.get('page', 1, type=int)
    # we are going to use the query query.order_by(DonationRequest.request_date.desc()) to order our requests by date
    requests = UrgentRequest.query.order_by(UrgentRequest.request_date.desc()).paginate(page=page, per_page=5) # inteade of using .all() we gonna change it to .paginate() to get 10 requests per page
    # dont forget the display the list in the homa page banner
    return render_template('urgent_requests.html', title='Urgent Requests page', requests=requests)

# route that takes the user to a specific urgent request by id
@app.route('/urgent_don_request/<int:urgent_request_id>', methods=['POST', 'GET'], strict_slashes=False)
def urgent_don_request(urgent_request_id):
# replaced by the next line to manage also a 404 error when the request is not found
#    urgent_request = UrgentRequest.query.get(urgent_request_id)
    urgent_don_request = UrgentRequest.query.get_or_404(urgent_request_id)
    return render_template('urgent_request_by_id.html', title='Urgent Request By ID page', request=urgent_don_request)

# route to update an urgent donation request
@app.route('/urgent_request/<int:urgent_request_id>/update', methods=['POST', 'GET'], strict_slashes=False)
@login_required
def update_urgent_request(urgent_request_id):
# replaced by the next line to manage also a 404 error when the request is not found
#    don_request = DonationRequest.query.get(urgent_request_id)
    donrequest = DonationRequest.query.get_or_404(urgent_request_id)
    # give permission of updating just for the user who created the don_request
    if session.get('user_type') != 'hospital' or donrequest.hospital_id != current_user.id:
        abort(403)
    form = CRUDUrgentRequestForm()
    if form.validate_on_submit():
        donrequest.hospital_id=current_user.id
        donrequest.blood_type=form.blood_type.data
        donrequest.request_date=form.request_date.data
        donrequest.expiration_date=form.expiration_date.data
        db.session.commit()
        flash('Your Urgent Request has been updated!', 'success')
        return redirect(url_for('urgent_request', urgent_request_id=donrequest.id))
    elif request.method == 'GET':
    # managed to populate the forms with data
        form.hospital_id.data=current_user.barcode
        form.blood_type.data=donrequest.blood_type
        form.request_date.data=donrequest.request_date
        form.expiration_date.data=donrequest.expiration_date
    
    return render_template('create_urgent_request.html', title='Update Urgent Request',form=form, legend='Update Urgent Request') # the legend keywoed will be used to the template legend (whether its a new post or an update)


# route to handle the deletion of an urgent request
@app.route('/urgent_request/<int:urgent_request_id>/delete', methods=['POST'], strict_slashes=False)
@login_required
def delete_urgent_request(urgent_request_id):
    donrequest = DonationRequest.query.get_or_404(urgent_request_id)
    # Ensure only the hospital that created the urgent request can delete it
    if session.get('user_type') != 'hospital' or donrequest.hospital_id != current_user.id:
        abort(403)
    db.session.delete(donrequest)
    db.session.commit()
    flash('Your urgent request has been deleted!', 'success')
    return redirect(url_for('urgent_requests'))

# route to get all the urgent requests posted by a specifique hospital when clicking on the hospital's name
@app.route('/hospital/<string:name>', methods=['POST', 'GET'], strict_slashes=False)
def hospital_urgent_requests(name):
    page = request.args.get('page', 1, type=int)
    hospital = Hospital.query.filter_by(name=name).first_or_404()
    # we are going to use the query query.order_by(DonationRequest.request_date.desc()) to order our requests by date
    # also using the backref hospital_request
    hospital_requests = UrgentRequest.query.filter_by(hospital_request=hospital)\
            .order_by(UrgentRequest.request_date.desc())\
            .paginate(page=page, per_page=5) # inteade of using .all() we gonna change it to .paginate() to get 10 requests per page

    return render_template('hospital_urgent_requests.html', title='Hospital Urgent Requests page', requests=hospital_requests, hospital=hospital)









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

{url_for('reset_token', token=token, _external=True)}

Thank you for using LifeGiver!
{url_for('home', _external=True)}

'''
  # we are using the external in order to get an absolute url instead of a relative url <= this one needs the full domain in the link
    mail.send(msg)

# 
@app.route("/reset_password", methods=['GET', 'POST'], strict_slashes=False)
def reset_request():
    # to make sure that the user is logged out befor they can reset their password
    if current_user.is_authenticated:
        return redirect(url_for('donor_dashboard'))
    form = RequestResetForm()
    if form.validate_on_submit():
        donor = Donor.query.filter_by(email=form.email.data).first()
        send_reset_email(donor)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('existing_donor'))
    return render_template('reset_request.html', title='Reset Password', form=form)
    


@app.route("/reset_password/<token>", methods=['GET', 'POST'], strict_slashes=False)
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home')) # change it later
    donor = Donor.verify_reset_token(token)  # using the staticmethod from the class Donor of Models
    if donor is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        donor.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('existing_donor'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@app.route("/schedule_donation/<int:don_request_id>", methods=['GET', 'POST'], strict_slashes=False)
@login_required
def schedule_donation(don_request_id):
    don_request = DonationRequest.query.get_or_404(don_request_id)
    form = UserDonationForm()
    if form.validate_on_submit():
        user_donation =UserDonation(
            donation_date=form.donation_date.data,
            status='requested',
            donor_id=current_user.id,
            request_id=don_request.id,
            hospital_id=don_request.hospital_request.id
        )
        db.session.add(user_donation)
        db.session.commit()
        flash('Your donation session has been booked in the hospital', 'success')
        return redirect(url_for('donation', don_request_id=don_request_id, user_donation=user_donation))
    if request.method == 'GET':
        form.donation_date.data=datetime.now()
    return render_template("schedule_donation.html", title='Donating page', don_request=don_request, form=form)

# send a msg to the hospital
def send_urg_donation_email(user, request_id):
    msg = Message(' Your Donation Request has been approved',
                  sender='noreply.lifegiver@gmail.com',
                  recipients=[user.email]) # reset the sender to the email comming from the domain later
    msg.body = f'''Dear {user.name},

Your urgent request has been approved by a Donor.

Please ensure that you are prepared to receive the donor and facilitate the donation process. 

We kindly remind you to update the donation request information after the  the donation has been completed.

{url_for('update_urgent_request', urgent_request_id=request_id, _external=True)}

Thank you for using LifeGiver!
{url_for('home', _external=True)}
'''
    mail.send(msg)

@app.route("/donation/<int:don_request_id>", methods=['GET', 'POST'], strict_slashes=False)
@login_required
def donation(don_request_id):
    urgent_request = UrgentRequest.query.get(don_request_id)
    don_request = DonationRequest.query.get(don_request_id)
    if urgent_request:
        hospital = urgent_request.hospital_urgent_request
        send_urg_donation_email(hospital, don_request_id)
        user_donation = None
    else:
        user_donation = UserDonation.query.filter_by(request_id=don_request_id, donor_id=current_user.id).first()
        if not user_donation:
            redirect(url_for("schedule_donation", don_request_id=don_request_id))
    
    return render_template("donation.html", title='Donating page', urgent_request=urgent_request, don_request=don_request, user_donation=user_donation)


