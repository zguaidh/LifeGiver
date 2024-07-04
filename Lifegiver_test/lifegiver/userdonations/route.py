from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, Blueprint
from lifegiver.userdonations.forms import UserDonationForm
from lifegiver import db
from lifegiver.models  import UserDonation, DonationRequest
from flask_login import current_user, login_required
from lifegiver.userdonations.utils import send_donation_don_email, send_donation_hos_email

userdonations = Blueprint('userdonations', __name__)



@userdonations.route("/schedule_donation/<int:don_request_id>", methods=['GET', 'POST'], strict_slashes=False)
@login_required
def schedule_donation(don_request_id):
    don_request = DonationRequest.query.get_or_404(don_request_id)
    form = UserDonationForm()
    if form.validate_on_submit():
        print("Form is validated and ready for submission.")
        user_donation =UserDonation(
            donation_date=form.donation_date.data,
            donor_id=current_user.id,
            request_id=don_request.id,
            hospital_id=don_request.hospital_request.id
        )
        db.session.add(user_donation)
        try:
            db.session.commit()
            print("Database commit successful.")
            current_user.increment_donation_count()
            print(current_user.donation_count)
            flash('Your donation session has been booked in the hospital', 'success')
            return redirect(url_for('userdonations.donation', don_request_id=don_request_id))
        except Exception as e:
            db.session.rollback()
            print(f"Error committing to the database: {e}")
            flash('An error occurred while scheduling your donation. Please try again.', 'danger')
    
    else:
        if request.method == 'POST':
            print("Form validation failed")
            print(form.errors)
        form.donation_date.data=datetime.now()
    

    return render_template("schedule_donation.html", title='Schedule Donation', don_request=don_request, form=form)


@userdonations.route("/donation/<int:don_request_id>", methods=['GET', 'POST'], strict_slashes=False)
@login_required
def donation(don_request_id):
    don_request = DonationRequest.query.get_or_404(don_request_id)
    hospital = don_request.hospital_request
    user_donation = UserDonation.query.get(don_request_id)
    send_donation_hos_email(hospital, don_request_id, user_donation)
    send_donation_don_email(current_user, don_request, hospital, user_donation)
    return render_template("donation.html", title='Donating page', don_request=don_request, user_donation=user_donation)


