import unittest
from datetime import datetime
from lifegiver import db, app
from lifegiver.models import Donor, Hospital, UserDonation, DonationRequest, UrgentRequest

class TestModels(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_donor(self):
        donor = Donor(username='testuser', email='test@example.com', password='password', age=25,
                      phone_number='1234567890', blood_type='O+', street='123 Test St', city='Test City',
                      province='Test Province', zip_code='12345', country='Test Country', national_id='123456789')
        db.session.add(donor)
        db.session.commit()

        saved_donor = Donor.query.filter_by(username='testuser').first()
        self.assertIsNotNone(saved_donor)
        self.assertEqual(saved_donor.email, 'test@example.com')

    def test_create_hospital(self):
        hospital = Hospital(name='Test Hospital', email='hospital@example.com', password='password',
                            phone_number='1234567890', street='123 Hospital St', city='Hospital City',
                            province='Hospital Province', zip_code='12345', country='Hospital Country', barcode='12345')
        db.session.add(hospital)
        db.session.commit()

        saved_hospital = Hospital.query.filter_by(name='Test Hospital').first()
        self.assertIsNotNone(saved_hospital)
        self.assertEqual(saved_hospital.email, 'hospital@example.com')

    def test_create_user_donation(self):
        donor = Donor(username='testuser', email='test@example.com', password='password', age=25,
                      phone_number='1234567890', blood_type='O+', street='123 Test St', city='Test City',
                      province='Test Province', zip_code='12345', country='Test Country', national_id='123456789')
        hospital = Hospital(name='Test Hospital', email='hospital@example.com', password='password',
                            phone_number='1234567890', street='123 Hospital St', city='Hospital City',
                            province='Hospital Province', zip_code='12345', country='Hospital Country', barcode='12345')
        db.session.add(donor)
        db.session.add(hospital)
        db.session.commit()

        user_donation = UserDonation(donation_date=datetime.now(), status='requested',
                                     donor_id=donor.id, hospital_id=hospital.id)
        db.session.add(user_donation)
        db.session.commit()

        saved_donation = UserDonation.query.filter_by(status='requested').first()
        self.assertIsNotNone(saved_donation)
        self.assertEqual(saved_donation.donor_id, donor.id)

    def test_create_donation_request(self):
        hospital = Hospital(name='Test Hospital', email='hospital@example.com', password='password',
                            phone_number='1234567890', street='123 Hospital St', city='Hospital City',
                            province='Hospital Province', zip_code='12345', country='Hospital Country', barcode='12345')
        db.session.add(hospital)
        db.session.commit()

        donation_request = DonationRequest(hospital_id=hospital.id, blood_type='O+',
                                           request_date=datetime.now(), status='pending',
                                           expiration_date=datetime.now())
        db.session.add(donation_request)
        db.session.commit()

        saved_request = DonationRequest.query.filter_by(status='pending').first()
        self.assertIsNotNone(saved_request)
        self.assertEqual(saved_request.hospital_id, hospital.id)

    def test_create_urgent_request(self):
        hospital = Hospital(name='Test Hospital', email='hospital@example.com', password='password',
                            phone_number='1234567890', street='123 Hospital St', city='Hospital City',
                            province='Hospital Province', zip_code='12345', country='Hospital Country', barcode='12345')
        db.session.add(hospital)
        db.session.commit()

        urgent_request = UrgentRequest(hospital_id=hospital.id, blood_type='O+',
                                       request_date=datetime.now(),
                                       expiration_date=datetime.now())
        db.session.add(urgent_request)
        db.session.commit()

        saved_urgent_request = UrgentRequest.query.filter_by(blood_type='O+').first()
        self.assertIsNotNone(saved_urgent_request)
        self.assertEqual(saved_urgent_request.hospital_id, hospital.id)


if  __name__ == '__name__':
    unittest.main()