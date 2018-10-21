from datetime import date
from rest_framework.test import APITestCase

from contacts.models import Contact


# Models Tests

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
