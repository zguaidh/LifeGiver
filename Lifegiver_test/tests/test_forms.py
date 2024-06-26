import unittest
from flask import Flask
from flask_testing import TestCase
from lifegiver import app, db
from lifegiver.models import Donor, Hospital
from lifegiver.forms import DonorRegistrationForm, DonorLoginForm, HospitalLoginForm, HospitalRegistrationForm, DonorUpdatingForm, HospitalUpdatingForm

class BaseTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SECRET_KEY'] = 'mysecret'
        return app

    def setUp(self):
        db.create_all()
        donor = Donor(username='testuser', email='test@example.com', password='password', age=25,
                      phone_number='1234567890', blood_type='O+', street='123 Test St', city='Test City',
                      province='Test Province', zip_code='12345', country='Test Country', national_id='123456789')
        hospital = Hospital(name='Test Hospital', email='hospital@example.com', password='password', 
                            phone_number='1234567890', street='123 Hospital St', city='Hospital City', 
                            province='Hospital Province', zip_code='12345', country='Hospital Country', barcode='12345')
        db.session.add(donor)
        db.session.add(hospital)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestDonorRegistrationForm(BaseTestCase):
    def test_donor_registration_form(self):
        form = DonorRegistrationForm(username='testuser2', email='test2@example.com', password='password', 
                                     confirm_password='password', age=30, phone_number='0987654321', blood_type='A+', 
                                     street='456 Test St', city='Test City', province='Test Province', 
                                     zip_code='54321', country='Test Country', national_id='987654321')
        self.assertTrue(form.validate())
    def test_invalid_donor_registration_form(self):
        form = DonorRegistrationForm(data={
            'username': '',  # Missing username
            'email': 'invalidemail',
            'password': 'password',
            'confirm_password': 'differentpassword',
            'age': 'invalidage',  # Age should be an integer
            'phone_number': '1234567890',
            'blood_type': 'O+',
            'street': '123 Test St',
            'city': 'Test City',
            'province': 'Test Province',
            'zip_code': '12345',
            'country': 'Test Country',
            'national_id': '123456789'
        })
        self.assertFalse(form.validate())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('confirm_password', form.errors)
        self.assertIn('age', form.errors)

class TestDonorLoginForm(BaseTestCase):
    def test_donor_login_form(self):
        form = DonorLoginForm(email='test@example.com', password='password')
        self.assertTrue(form.validate())

class TestHospitalLoginForm(BaseTestCase):
    def test_hospital_login_form(self):
        form = HospitalLoginForm(barcode='12345', password='password')
        self.assertTrue(form.validate())

class TestHospitalRegistrationForm(BaseTestCase):
    def test_hospital_registration_form(self):
        form = HospitalRegistrationForm(name='New Hospital', email='newhospital@example.com', password='password', 
                                        confirm_password='password', phone_number='1122334455', street='789 Hospital St', 
                                        city='New City', province='New Province', zip_code='67890', country='New Country')
        self.assertTrue(form.validate())
    def test_invalid_hospital_registration_form(self):
        form = HospitalRegistrationForm(data={
            'name': '',  # Missing name
            'email': 'invalidemail',
            'password': 'password',
            'confirm_password': 'differentpassword',
            'phone_number': '1234567890',
            'street': '123 Hospital St',
            'city': 'Hospital City',
            'province': 'Hospital Province',
            'zip_code': '12345',
            'country': 'Hospital Country',
            'barcode': '12345'
        })
        self.assertFalse(form.validate())
        self.assertIn('name', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('confirm_password', form.errors)

class TestDonorUpdatingForm(BaseTestCase):
    def test_donor_updating_form(self):
        form = DonorUpdatingForm(username='updateduser', email='updated@example.com', age=35, phone_number='2233445566', 
                                 blood_type='B+', street='987 Updated St', city='Updated City', province='Updated Province', 
                                 zip_code='87654', country='Updated Country', national_id='876543210')
        self.assertTrue(form.validate())

class TestHospitalUpdatingForm(BaseTestCase):
    def test_hospital_updating_form(self):
        form = HospitalUpdatingForm(name='Updated Hospital', email='updatedhospital@example.com', phone_number='5566778899', 
                                    street='654 Updated St', city='Updated City', province='Updated Province', 
                                    zip_code='45678', country='Updated Country')
        self.assertTrue(form.validate())

if __name__ == '__main__':
    unittest.main()
