from flask import render_template, flash, redirect, url_for, request, session, Blueprint
from lifegiver.hospitals.forms import (HospitalRegistrationForm, HospitalLoginForm,
                             RequestResetForm, ResetPasswordForm, HospitalUpdatingForm)
from lifegiver import db, bcrypt
from lifegiver.models  import Donor, Hospital, DonationRequest, UrgentRequest
from flask_login import login_user, current_user, login_required
from flask import current_app
from lifegiver.hospitals.utils import make_serial, geocode_address, send_barcode_email, save_picture, send_reset_email, find_nearby_donors

hospitals = Blueprint('hospitals', __name__)




# route for hospital registration:
@hospitals.route('/hospital_registration', methods=['GET', 'POST'], strict_slashes=False)
def hospital_registration():
    # To manage the authentication of the hospital
     if current_user.is_authenticated:
        return redirect(url_for('hospitals.hospital_dashboard'))
     form = HospitalRegistrationForm()
     if form.validate_on_submit():
        # check if the name of the hospital exists in our database
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        barcode = make_serial(15)
        address = f"{form.street.data}, {form.city.data}, {form.province.data}, {form.zip_code.data}, {form.country.data}"
        lat, lng = geocode_address(address)
        print(f"Address: {address}")
        print(f"Latitude: {lat}, Longitude: {lng}")
        hospital = Hospital(name=form.name.data,
                     email=form.email.data,
                     password=hashed_password,
                     phone_number=form.phone_number.data,
                     street=form.street.data,
                     city=form.city.data,
                     province=form.province.data,
                     zip_code=form.zip_code.data,
                     country=form.country.data,
                     barcode=barcode,
                     lat=lat,
                     lng=lng)
        db.session.add(hospital)
        db.session.commit()
        print(hospital.barcode)
        send_barcode_email(hospital, barcode)
        flash(f'Acount created for {form.name.data}, Your serial number has been sent to your email!', 'success')
        return redirect(url_for('hospitals.hospital_login'))
     return render_template('hospital_registration.html', title='Hospital Registration', form=form)


# route fo rhospital login
@hospitals.route('/hospital_login', methods=['GET', 'POST'], strict_slashes=False)
def hospital_login():
    # To manage the authentication of the hospital
     if current_user.is_authenticated:
        return redirect(url_for('hospitals.hospital_dashboard'))
     form = HospitalLoginForm()
     if form.validate_on_submit():

        hospital = Hospital.query.filter_by(barcode=form.barcode.data).first()
        if hospital and bcrypt.check_password_hash(hospital.password, form.password.data):
            login_user(hospital, remember=form.remember.data)
            session['user_type'] = 'hospital'
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('hospitals.hospital_dashboard'))
        else:
#        flash(f'The hospital {form.barcode.data} loged in successefuly!', 'success')
            flash('Login Unsuccessful. Please check barcode and password', 'danger')
        return redirect(url_for('hospitals.hospital_login'))
     return render_template('hospital_login.html', title='Hospital Login', form=form)




@hospitals.route('/hospital_dashboard', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def hospital_dashboard():
    form = HospitalUpdatingForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_File = save_picture(form.picture.data)
            current_user.image_file = picture_File
        address = f"{form.street.data}, {form.city.data}, {form.province.data}, {form.zip_code.data}, {form.country.data}"
        lat, lng = geocode_address(address)
        current_user.name = form.name.data
        current_user.email=form.email.data
        current_user.phone_number=form.phone_number.data
        current_user.street=form.street.data
        current_user.city=form.city.data
        current_user.province=form.province.data
        current_user.zip_code=form.zip_code.data
        current_user.country=form.country.data
        current_user.lat=lat
        current_user.lng=lng
        db.session.commit()
        flash('Your account has been updated successfuly!', 'success')
        return redirect(url_for('hospitals.hospital_dashboard'))
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
        image_file = url_for('static', filename='images/' + current_user.image_file)
    hospital_requests = DonationRequest.query.filter_by(hospital_id=current_user.id).all()
    hospital_urgent_requests = UrgentRequest.query.filter_by(hospital_id=current_user.id).all()
    requests_count = len(hospital_requests)
    urgent_requests_count = len(hospital_urgent_requests)
    return render_template('hospital_dashboard.html', title='Hospital dashboard', image_file=image_file, requests_count=requests_count, urgent_requests_count=urgent_requests_count, form=form)

@hospitals.route('/hospital_profile', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def hospital_profile():
    form = HospitalUpdatingForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_File = save_picture(form.picture.data)
            current_user.image_file = picture_File
        address = f"{form.street.data}, {form.city.data}, {form.province.data}, {form.zip_code.data}, {form.country.data}"
        lat, lng = geocode_address(address)
        current_user.name = form.name.data
        current_user.email=form.email.data
        current_user.phone_number=form.phone_number.data
        current_user.street=form.street.data
        current_user.city=form.city.data
        current_user.province=form.province.data
        current_user.zip_code=form.zip_code.data
        current_user.country=form.country.data
        current_user.lat=lat
        current_user.lng=lng
        db.session.commit()
        flash('Your account has been updated successfuly!', 'success')
        return redirect(url_for('hospitals.hospital_dashboard'))
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
        image_file = url_for('static', filename='images/' + current_user.image_file)
    hospital_requests = DonationRequest.query.filter_by(hospital_id=current_user.id).all()
    hospital_urgent_requests = UrgentRequest.query.filter_by(hospital_id=current_user.id).all()
    requests_count = len(hospital_requests)
    urgent_requests_count = len(hospital_urgent_requests)
    return render_template('hospital_profile.html', title='Hospital profile', image_file=image_file, requests_count=requests_count, urgent_requests_count=urgent_requests_count, form=form, user=current_user)



# 
@hospitals.route("/reset_password", methods=['GET', 'POST'], strict_slashes=False)
def reset_request():
    # to make sure that the user is logged out befor they can reset their password
    if current_user.is_authenticated:
        return redirect(url_for('hospitals.donor_dashboard'))
    form = RequestResetForm()
    if form.validate_on_submit():
        donor = Donor.query.filter_by(email=form.email.data).first()
        send_reset_email(donor)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('existing_donor'))
    return render_template('reset_request.html', title='Reset Password', form=form)
    


@hospitals.route("/reset_password/<token>", methods=['GET', 'POST'], strict_slashes=False)
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home')) # change it later
    donor = Donor.verify_reset_token(token)  # using the staticmethod from the class Donor of Models
    if donor is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('hospitals.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        donor.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('hospitals.existing_donor'))
    return render_template('reset_token.html', title='Reset Password', form=form)



#  a route to the history of all the requests
@hospitals.route('/requests_history/<string:name>', methods=['POST', 'GET'], strict_slashes=False)
def requests_history(name):
    page = request.args.get('page', 1, type=int)
    hospital = Hospital.query.filter_by(name=name).first_or_404()
    # we are going to use the query query.order_by(DonationRequest.request_date.desc()) to order our requests by date
    # also using the backref hospital_request
    hospital_requests = DonationRequest.query.filter_by(hospital_request=hospital)\
            .order_by(DonationRequest.request_date.desc())\
            .paginate(page=page, per_page=5) # inteade of using .all() we gonna change it to .paginate() to get 10 requests per page

    return render_template('requests_history.html', title='All Hospital Requests', requests=hospital_requests, hospital=hospital)



# route to show the nearby donors map:
@hospitals.route('/nearby_donors/<int:hospital_id>/<string:blood_type>', methods=['GET'])
def nearby_donors(hospital_id, blood_type):
    hospital = Hospital.query.get_or_404(hospital_id)
    donors = Donor.query.filter_by(blood_type=blood_type).all()
    
    nearby_donors = find_nearby_donors(hospital, blood_type)
    
    markers = []
    for donor in nearby_donors:
        markers.append(f"markers=color:red|label:D|{donor.lat},{donor.lng}")
    markers.append(f"markers=color:blue|label:H|{hospital.lat},{hospital.lng}")
    
    markers_string = "&".join(markers)
    api_key = current_app.config['GOOGLE_MAPS_API_KEY']
    
    # Debugging output
    print(f"API Key: {api_key}")
    print(f"Markers: {markers_string}")

    map_url = (
        f"https://maps.googleapis.com/maps/api/staticmap?size=600x400&{markers_string}&zoom=12&key={api_key}"
    )

    # Debugging output
    print(f"Map URL: {map_url}")

    return render_template('nearby_donors.html', hospital=hospital, donors=nearby_donors, map_url=map_url)

