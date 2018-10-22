from datetime import date

from rest_framework.test import APITestCase

from contacts.models import Contact, PhoneNumber, EmailField


class ContactModelTest(APITestCase):
    def setUp(self):
        self.created_contact = Contact.objects.create(
            first_name='John',
            last_name='Doe',
            date_of_birth=date(1980, 10, 5)
        )

    def test_contact(self):
        """
        Simple test to ensure that the contact created in the setup exists
        """
        self.assertEqual('John', self.created_contact.first_name)
        self.assertEqual('Doe', self.created_contact.last_name)
        self.assertEqual(date(1980, 10, 5), self.created_contact.date_of_birth)
        self.assertEqual('John Doe', str(self.created_contact))


class PhoneNumberModelTest(APITestCase):
    def setUp(self):
        self.created_contact = Contact.objects.create(
            first_name='John',
            last_name='Doe',
            date_of_birth=date(1980, 10, 5)
        )
        self.created_phone = PhoneNumber.objects.create(
            contact=self.created_contact,
            phone='+1 202 555 0104',
            primary=True
        )

    def test_email_field(self):
        """
        Simple test to ensure that the phone number created in the setup exists
        """
        self.assertEqual(self.created_contact, self.created_phone.contact)
        self.assertEqual('+1 202 555 0104', self.created_phone.phone)
        self.assertEqual(True, self.created_phone.primary)
        self.assertEqual('+1 202 555 0104', str(self.created_phone))


class EmailFieldModelTest(APITestCase):
    def setUp(self):
        self.created_contact = Contact.objects.create(
            first_name='John',
            last_name='Doe',
            date_of_birth=date(1980, 10, 5)
        )
        self.created_email = EmailField.objects.create(
            contact=self.created_contact,
            email='user@example.com'
        )

    def test_email_field(self):
        """
        Simple test to ensure that the email created in the setup exists
        """
        self.assertEqual(self.created_contact, self.created_email.contact)
        self.assertEqual('user@example.com', self.created_email.email)
        self.assertEqual('user@example.com', str(self.created_email))
