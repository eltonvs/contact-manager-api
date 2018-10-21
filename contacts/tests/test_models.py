from datetime import date

from rest_framework.test import APITestCase

from contacts.models import Contact, PhoneNumber


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
        self.assertEqual(self.created_contact.first_name, 'John')
        self.assertEqual(self.created_contact.last_name, 'Doe')
        self.assertEqual(self.created_contact.date_of_birth, date(1980, 10, 5))
        self.assertEqual(str(self.created_contact), "John Doe")


class PhoneNumberModelTest(APITestCase):
    def setUp(self):
        self.created_contact = Contact.objects.create(
            first_name='John',
            last_name='Doe',
            date_of_birth=date(1980, 10, 5)
        )
        self.created_email = PhoneNumber.objects.create(
            contact=self.created_contact,
            phone='+1 202 555 0104',
            primary=True
        )

    def test_email_field(self):
        """
        Simple test to ensure that the email created in the setup exists
        """
        self.assertEqual(self.created_email.contact, self.created_contact)
        self.assertEqual(self.created_email.phone, '+1 202 555 0104')
        self.assertEqual(self.created_email.primary, True)
        self.assertEqual(str(self.created_email), '+1 202 555 0104')
