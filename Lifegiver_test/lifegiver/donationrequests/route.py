from flask import render_template, flash, redirect, url_for, request, session, abort, Blueprint
from lifegiver.donationrequests.forms import CRUDRequestForm
from lifegiver import db
from lifegiver.models  import Hospital, DonationRequest
from flask_login import current_user, login_required
from lifegiver.donationrequests.utils import find_nearby_donors, send_notification_email

donationrequests = Blueprint('donationrequests', __name__)



# route for create operation for donation request
@donationrequests.route("/request/new", methods=['GET', 'POST'], strict_slashes=False)
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

         # Check if the send_notifications checkbox was checked
        if 'send_notifications' in request.form:
            nearby_donors = find_nearby_donors(current_user, form.blood_type.data)
            message = f'''
            Dear Donor, 
            A new Donation Request for {form.blood_type.data} blood type has been posted by {current_user.name} 
            Located at : {current_user.street}, {current_user.city}, {current_user.province}, {current_user.zip_code}, {current_user.country}
            Donate now : {url_for('donationrequests.don_request', don_request_id=don_request.id, _external=True)}
            '''

            for donor in nearby_donors:
                send_notification_email(donor, message)

            flash('Notifications sent to nearby donors!', 'info')
            return redirect(url_for('donationrequests.don_requests'))         
        else:
            return redirect(url_for('donationrequests.don_requests'))
    elif request.method == 'GET':
        #the name of the field is id but it will show the barcode
        form.hospital_id.data = current_user.barcode
        # add the same line for the name
    return render_template('create_request.html', title='New Request',form=form, image_file=current_user.image_file, legend='Create Request') # the legend keywoed will be used to change the template legend (whether its a new post or an update)
# route to return all the donation requests

@donationrequests.route('/don_requests', methods=['POST', 'GET'], strict_slashes=False)
def don_requests():
    page = request.args.get('page', 1, type=int)
    # we are going to use the query query.order_by(DonationRequest.request_date.asc()) to order our requests by date
    requests = DonationRequest.query.order_by(DonationRequest.request_date.asc()).paginate(page=page, per_page=5) # inteade of using .all() we gonna change it to .paginate() to get 10 requests per page
    image_file = current_user.image_file
    return render_template('requests.html', title='Donation Requests page', requests=requests, image_file=image_file)

# route that takes the user to a specific request by id
@donationrequests.route('/don_request/<int:don_request_id>', methods=['POST', 'GET'], strict_slashes=False)
def don_request(don_request_id):
# replaced by the next line to manage also a 404 error when the request is not found
#    don_request = DonationRequest.query.get(don_request_id)
    don_request = DonationRequest.query.get_or_404(don_request_id)
    return render_template('request_by_id.html', title='A Request By ID page', request=don_request)

# route to update a donation request
@donationrequests.route('/don_request/<int:don_request_id>/update', methods=['POST', 'GET'], strict_slashes=False)
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
        return redirect(url_for('donationrequests.don_request', don_request_id=donrequest.id))
    elif request.method == 'GET':
    # managed to populate the forms with data 
        form.hospital_id.data=current_user.barcode
        form.blood_type.data=donrequest.blood_type
        form.request_date.data=donrequest.request_date
        form.status.data=donrequest.status
        form.expiration_date.data=donrequest.expiration_date
    
    return render_template('create_request.html', title='Update Request',form=form, legend='Update Request') # the legend keywoed will be used to the template legend (whether its a new post or an update)


# route to handle the deletion of a request
@donationrequests.route('/don_request/<int:don_request_id>/delete', methods=['POST'], strict_slashes=False)
@login_required
def delete_don_request(don_request_id):
    donrequest = DonationRequest.query.get_or_404(don_request_id)
    # Ensure only the hospital that created the request can delete it
    if session.get('user_type') != 'hospital' or donrequest.hospital_id != current_user.id:
        abort(403)
    db.session.delete(donrequest)
    db.session.commit()
    flash('Your request has been deleted!', 'success')
    return redirect(url_for('donationrequests.don_requests'))

# route to get all the requests posted by a specifique hospital when clicking on the hospital's barcode
# change the barcode to the name of hospital later
@donationrequests.route('/hospital/<string:name>', methods=['POST', 'GET'], strict_slashes=False)
def hospital_requests(name):
    page = request.args.get('page', 1, type=int)
    hospital = Hospital.query.filter_by(name=name).first_or_404()
    # we are going to use the query query.order_by(DonationRequest.request_date.asc()) to order our requests by date
    # also using the backref hospital_request
    hospital_requests = DonationRequest.query.filter_by(hospital_request=hospital)\
            .order_by(DonationRequest.request_date.asc())\
            .paginate(page=page, per_page=5) # inteade of using .all() we gonna change it to .paginate() to get 10 requests per page

    return render_template('hospital_requests.html', title='Hospital Requests page', requests=hospital_requests, hospital=hospital)


