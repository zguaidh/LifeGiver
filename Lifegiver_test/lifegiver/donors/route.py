from flask import render_template, flash, redirect, url_for, request, session, Blueprint
from lifegiver.donors.forms import (DonorLoginForm, DonorRegistrationForm, DonorUpdatingForm, 
                             RequestResetForm, ResetPasswordForm)
from lifegiver import db, bcrypt
from lifegiver.models  import Donor, Hospital, UserDonation
from flask_login import login_user, current_user, login_required
from flask import current_app
from lifegiver.donors.utils import geocode_address, save_picture, send_reset_email, get_distance

donors = Blueprint('donors', __name__)



@donors.route('/new_donor', methods=['GET', 'POST'], strict_slashes=False)
def new_donor():
    if current_user.is_authenticated:
        return redirect(url_for('donors.donor_dashboard'))
    form = DonorRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        address = f"{form.street.data}, {form.city.data}, {form.province.data}, {form.zip_code.data}, {form.country.data}"
        lat, lng = geocode_address(address)
        print(f"Address: {address}")
        print(f"Latitude: {lat}, Longitude: {lng}")
        donor = Donor(first_name=form.first_name.data,
                     last_name=form.last_name.data,
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
                     national_id=form.national_id.data,
                     lat=lat,
                     lng=lng)
        db.session.add(donor)
        db.session.commit()
     #   print(f"Latitude: {current_user.lat}, Longitude: {current_user.lng}")
        flash(f'Acount created for {form.first_name.data} {form.last_name.data}!', 'success')
        return redirect(url_for('donors.existing_donor'))
    return render_template('new_donor.html', title='New Donor registration', form=form)

@donors.route('/existing_donor', methods=['GET', 'POST'], strict_slashes=False)
def existing_donor():
    if current_user.is_authenticated:
        return redirect(url_for('donors.donor_dashboard'))
    form = DonorLoginForm()
    if form.validate_on_submit():
        donor = Donor.query.filter_by(email=form.email.data).first()
        if donor and bcrypt.check_password_hash(donor.password, form.password.data):
            login_user(donor, remember=form.remember.data)
            session['user_type'] = 'donor'
            # ternary conditional: to redirect the user to the the page he was tryinh to access befor logging in
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
        return redirect(url_for('donors.existing_donor'))
    return render_template('existing_donor.html', title='Donor Login', form=form)


@donors.route('/donor_dashboard', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def donor_dashboard():
    form = DonorUpdatingForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_File = save_picture(form.picture.data)
            current_user.image_file = picture_File

        address = f"{form.street.data}, {form.city.data}, {form.province.data}, {form.zip_code.data}, {form.country.data}"
        lat, lng = geocode_address(address)
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
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
        current_user.lat=lat
        current_user.lng=lng
        db.session.commit()
        flash('Your account has been updated successfuly!', 'success')
        return redirect(url_for('donors.donor_dashboard'))
    # to make sure that the form will be populated with the existing data
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
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
    image_file = url_for('static', filename='images/' + current_user.image_file)
    return render_template('donor_dashboard.html', title='Donor dashboard', image_file=image_file, form=form)

@donors.route('/donor_profile', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def donor_profile():
    form = DonorUpdatingForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_File = save_picture(form.picture.data)
            current_user.image_file = picture_File

        address = f"{form.street.data}, {form.city.data}, {form.province.data}, {form.zip_code.data}, {form.country.data}"
        lat, lng = geocode_address(address)
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
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
        current_user.lat=lat
        current_user.lng=lng
        db.session.commit()
        flash('Your Profile has been updated successfuly!', 'success')
        return redirect(url_for('donors.donor_dashboard'))
    # to make sure that the form will be populated with the existing data
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
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
    image_file = url_for('static', filename='images/' + current_user.image_file)
    return render_template('donor_profile.html', title='Profile', image_file=image_file, form=form, user=current_user)

# 
@donors.route("/reset_password", methods=['GET', 'POST'], strict_slashes=False)
def reset_request():
    # to make sure that the user is logged out befor they can reset their password
    if current_user.is_authenticated:
        return redirect(url_for('donors.donor_dashboard'))
    form = RequestResetForm()
    if form.validate_on_submit():
        donor = Donor.query.filter_by(email=form.email.data).first()
        send_reset_email(donor)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('donors.existing_donor'))
    return render_template('reset_request.html', title='Reset Password', form=form)
    


@donors.route("/reset_password/<token>", methods=['GET', 'POST'], strict_slashes=False)
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home')) # change it later
    donor = Donor.verify_reset_token(token)  # using the staticmethod from the class Donor of Models
    if donor is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('donors.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        donor.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('donors.existing_donor'))
    return render_template('reset_token.html', title='Reset Password', form=form)

    


#  a route to the history of all a user donations
@donors.route('/donation_history/<int:donor_id>', methods=['POST', 'GET'], strict_slashes=False)
def donation_history(donor_id):
    page = request.args.get('page', 1, type=int)
    donor = Donor.query.filter_by(id=donor_id).first_or_404()
    # we are going to use the query query.order_by(DonationRequest.request_date.desc()) to order our requests by date
    # also using the backref hospital_request
    user_donations = UserDonation.query.filter_by(donor_id=donor_id)\
            .order_by(UserDonation.donation_date.desc())\
            .paginate(page=page, per_page=5) # inteade of using .all() we gonna change it to .paginate() to get 10 requests per page

    return render_template('donation_history.html', title='All User Donations', donations=user_donations, donor_id=donor_id)

# route return the distance between hopital and donor:
@donors.route('/distance/<int:donor_id>/<int:hospital_id>', methods=['GET', 'POST'], strict_slashes=False)
def distance(donor_id, hospital_id):
    donor = Donor.query.get_or_404(donor_id)
    hospital = Hospital.query.get_or_404(hospital_id)

    if not donor.lat or not donor.lng or not hospital.lat or not hospital.lng:
        flash('Invalid coordinates for donor or hospital', 'danger')
        return redirect(url_for('main.home'))
    
     # Debugging output
    print(f"Donor coordinates: {donor.lat}, {donor.lng}")
    print(f"Hospital coordinates: {hospital.lat}, {hospital.lng}")
    
    directions_url = f"https://www.google.com/maps/dir/?api=1&origin={donor.lat},{donor.lng}&destination={hospital.lat},{hospital.lng}&travelmode=driving"
    map_url = f"https://maps.googleapis.com/maps/api/staticmap?size=600x400&markers=color:red%7Clabel:D%7C{donor.lat},{donor.lng}&markers=color:blue%7Clabel:H%7C{hospital.lat},{hospital.lng}&path=color:0x0000ff%7Cweight:5%7C{donor.lat},{donor.lng}%7C{hospital.lat},{hospital.lng}&key={current_app.config['GOOGLE_MAPS_API_KEY']}"
    
    return render_template('distance.html', title='Distance Calculation', donor=donor, hospital=hospital, map_url=map_url, directions_url=directions_url)




# route to show the nearby hospitals map:
@donors.route('/nearby_hospitals/<int:donor_id>', methods=['GET'])
def nearby_hospitals(donor_id):
    donor = Donor.query.get_or_404(donor_id)
    
    nearby_hospitals =[]
    hospitals = Hospital.query.all()
    for hospital in hospitals:
        if donor.lat is not None and donor.lng is not None and hospital.lat is not None and hospital.lng is not None:
            distance = get_distance(hospital.lat, hospital.lng, donor.lat, donor.lng)
            if distance <= 30:
                nearby_hospitals.append(hospital)
    
    print(nearby_hospitals)
    
    markers = []
    for hospital in nearby_hospitals:
        markers.append(f"markers=color:red|label:D|{hospital.lat},{hospital.lng}")
    markers.append(f"markers=color:blue|label:H|{donor.lat},{donor.lng}")
    
    markers_string = "&".join(markers)
    api_key = current_app.config['GOOGLE_MAPS_API_KEY']
    
    # Debugging output
    print(f"Markers: {markers_string}")

    map_url = (
        f"https://maps.googleapis.com/maps/api/staticmap?size=600x400&{markers_string}&zoom=12&key={api_key}"
    )

    # Debugging output
    print(f"Map URL: {map_url}")

    return render_template('nearby_hospitals.html', hospitals=nearby_hospitals, donor=donor, map_url=map_url)