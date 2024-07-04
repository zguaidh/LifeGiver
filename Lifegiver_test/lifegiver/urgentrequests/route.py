from flask import render_template, flash, redirect, url_for, request, session, abort, Blueprint
from lifegiver.urgentrequests.forms import CRUDUrgentRequestForm
from lifegiver import db
from lifegiver.models  import Hospital, UrgentRequest
from flask_login import current_user, login_required
from lifegiver.urgentrequests.utils import find_nearby_donors, send_notification_email, send_urg_donation_hos_email

urgentrequests = Blueprint('urgentrequests', __name__)



# route for create operation for Urgent request
@urgentrequests.route("/urgent_request/new", methods=['GET', 'POST'], strict_slashes=False)
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
        
        # Check if the send_notifications checkbox was checked
        if 'send_notifications' in request.form:
            nearby_donors = find_nearby_donors(current_user, form.blood_type.data)
            message = f'''
            Dear Donor, 
            A new Urgent request for {form.blood_type.data} blood has been posted by {current_user.name} 
            Located at : {current_user.street}, {current_user.city}, {current_user.province}, {current_user.zip_code}, {current_user.country}
            Donate now : {url_for('urgentrequests.urgent_don_request', urgent_request_id=urgent_don_request.id, _external=True)}
            '''

            for donor in nearby_donors:
                send_notification_email(donor, message)

            flash('Notifications sent to nearby donors!', 'info')
            return redirect(url_for('hospitals.nearby_donors', hospital_id=current_user.id, blood_type=form.blood_type.data))           
        else:
            return redirect(url_for('urgentrequests.urgent_requests'))
    elif request.method == 'GET':
        #the name of the field is id but it will show the barcode
        form.hospital_id.data = current_user.barcode
        # add the same line for the name
    return render_template('create_urgent_request.html', title='New Urgent Request',form=form, image_file=current_user.image_file, legend='Create Urgent Request') # the legend keywoed will be used to change the template legend (whether its a new post or an update)

# route for all urgent requests
@urgentrequests.route('/urgent_requests', methods=['POST', 'GET'], strict_slashes=False)
def urgent_requests():
    page = request.args.get('page', 1, type=int)
    # we are going to use the query query.order_by(DonationRequest.request_date.asc()) to order our requests by date
    requests = UrgentRequest.query.order_by(UrgentRequest.request_date.asc()).paginate(page=page, per_page=5) # inteade of using .all() we gonna change it to .paginate() to get 10 requests per page
    # dont forget the display the list in the homa page banner
    
    return render_template('urgent_requests.html', title='Urgent Requests page', requests=requests, image_file=current_user.image_file)

# route that takes the user to a specific urgent request by id
@urgentrequests.route('/urgent_don_request/<int:urgent_request_id>', methods=['POST', 'GET'], strict_slashes=False)
def urgent_don_request(urgent_request_id):
# replaced by the next line to manage also a 404 error when the request is not found
#    urgent_request = UrgentRequest.query.get(urgent_request_id)
    urgent_don_request = UrgentRequest.query.get_or_404(urgent_request_id)
    return render_template('urgent_request_by_id.html', title='Urgent Request By ID page', request=urgent_don_request)

# route to update an urgent donation request
@urgentrequests.route('/urgent_request/<int:urgent_request_id>/update', methods=['POST', 'GET'], strict_slashes=False)
@login_required
def update_urgent_request(urgent_request_id):
# replaced by the next line to manage also a 404 error when the request is not found
#    don_request = DonationRequest.query.get(urgent_request_id)
    donrequest = UrgentRequest.query.get_or_404(urgent_request_id)
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
        return redirect(url_for('urgentrequests.urgent_requests', urgent_request_id=donrequest.id))
    elif request.method == 'GET':
    # managed to populate the forms with data
        form.hospital_id.data=current_user.barcode
        form.blood_type.data=donrequest.blood_type
        form.request_date.data=donrequest.request_date
        form.expiration_date.data=donrequest.expiration_date
    
    return render_template('create_urgent_request.html', title='Update Urgent Request',form=form, legend='Update Urgent Request') # the legend keywoed will be used to the template legend (whether its a new post or an update)


# route to handle the deletion of an urgent request
@urgentrequests.route('/urgent_request/<int:urgent_request_id>/delete', methods=['POST'], strict_slashes=False)
@login_required
def delete_urgent_request(urgent_request_id):
    donrequest = UrgentRequest.query.get_or_404(urgent_request_id)
    # Ensure only the hospital that created the urgent request can delete it
    if session.get('user_type') != 'hospital' or donrequest.hospital_id != current_user.id:
        abort(403)
    db.session.delete(donrequest)
    db.session.commit()
    flash('Your urgent request has been deleted!', 'success')
    return redirect(url_for('urgentrequests.urgent_requests'))

# route to get all the urgent requests posted by a specifique hospital when clicking on the hospital's name
@urgentrequests.route('/hospital_urgent/<string:name>', methods=['POST', 'GET'], strict_slashes=False)
def hospital_urgent_requests(name):
    page = request.args.get('page', 1, type=int)
    hospital = Hospital.query.filter_by(name=name).first_or_404()
    # we are going to use the query query.order_by(DonationRequest.request_date.asc()) to order our requests by date
    # also using the backref hospital_request
    hospital_urg_requests = UrgentRequest.query.filter_by(hospital_id=hospital.id)\
            .order_by(UrgentRequest.request_date.asc())\
            .paginate(page=page, per_page=5) # inteade of using .all() we gonna change it to .paginate() to get 10 requests per page

    return render_template('hospital_urgent_requests.html', title='Hospital Urgent Requests', requests=hospital_urg_requests, hospital=hospital)



@urgentrequests.route("/urgent_donation/<int:don_request_id>", methods=['GET', 'POST'], strict_slashes=False)
@login_required
def urgent_donation(don_request_id):
    urgent_request = UrgentRequest.query.get(don_request_id)

    hospital = urgent_request.hospital_urgent_request
#    current_user.increment_donation_count()
    send_urg_donation_hos_email(hospital, don_request_id)
    
    return render_template("urgent_donation.html", title='Donating page', urgent_request=urgent_request)







