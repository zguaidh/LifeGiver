import secrets
from PIL import Image
import os
from flask import render_template, flash, redirect, url_for, request, session, abort
from lifegiver.forms import DonorLoginForm, DonorRegistrationForm, HospitalRegistrationForm, DonorUpdatingForm, CRUDRequestForm
from lifegiver import app, db, bcrypt
from lifegiver.models  import Donor, Hospital, UserDonation, DonationRequest, UrgentRequest
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/', methods=['POST', 'GET'], strict_slashes=False)
@app.route('/home', methods=['POST', 'GET'], strict_slashes=False)
def home():
    return render_template('home.html', title='Home page')

# to check later if we gonna keep it
@app.route("/about", methods=['GET'], strict_slashes=False)
def about():
    return render_template('about.html', title='About page')


@app.route('/urgent_requests', methods=['GET'], strict_slashes=False)
def urgent_requests():
    return render_template('urgent_requests.html', title='Urgent Requests')

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

@app.route('/hospital', methods=['GET', 'POST'], strict_slashes=False)
def hospital():
    # To manage the authentication of the hospital
     if current_user.is_authenticated:
        return redirect(url_for('hospital_dashboard'))
     form = HospitalRegistrationForm()
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
        return redirect(url_for('hospital'))
     return render_template('hospital_registration.html', title='Hospital registration', form=form)

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
    # to make sure that the form will be populated with the existing data when its called
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
    return render_template('hospital_dashboard.html', title='Hospital dashboard')

@app.route("/logout")
def logout():

    logout_user()
    return redirect(url_for('home'))

# route for create operation for donation request
@app.route("/request/new", methods=['GET', 'POST'])
@login_required
def new_request():
    form = CRUDRequestForm()
    if form.validate_on_submit():
        don_request = DonationRequest(
            hospital_id=current_user.id,
            blood_type=form.blood_type.data,
            request_date=form.request_date.data,
            status=form.status.data,
            expiration_date=form.expiration_date.data
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
    requests = DonationRequest.query.all()
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
    don_request = DonationRequest.query.get_or_404(don_request_id)
    # give permission of updating just for the user who created the don_request
    if don_request.hospital_id != current_user.id:
        abort(403)
    form = CRUDRequestForm()
    if form.validate_on_submit():
        don_request.hospital_id=current_user.id,
        don_request.blood_type=form.blood_type.data,
        don_request.request_date=form.request_date.data,
        don_request.status=form.status.data,
        don_request.expiration_date=form.expiration_date.data
        db.session.commit()
        flash('Your Request has been updated!', 'success')
        return redirect(url_for('requests'), request_id=don_request.id)
    elif request.method == 'GET':
    # managed to populate the forms with data 
        form.hospital_id.data=current_user.barcode
        form.blood_type.data=don_request.blood_type
        form.request_date.data=don_request.request_date
        form.status.data=don_request.status
        form.expiration_date.data=don_request.expiration_date
    
    return render_template('create_request.html', title='Update Request',form=form, legend='Update Request') # the legend keywoed will be used to the template legend (whether its a new post or an update)