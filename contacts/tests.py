import json
from datetime import date
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient

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


# View Tests

class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def insert_contact(first_name, last_name, date_of_birth):
        """
        Create a contact and store on database
        :param first_name:
        :param last_name:
        :param date_of_birth:
        """
        if first_name != '' and last_name != '' and date_of_birth:
            Contact.objects.create(first_name=first_name, last_name=last_name, date_of_birth=date_of_birth)

    def setUp(self):
        # Populate database
        self.insert_contact('Elton', 'John', date(1947, 3, 25))
        self.insert_contact('Elvis', 'Presley', date(1935, 1, 8))
        self.insert_contact('Marilyn', 'Monroe', date(1926, 6, 1))
        # Default Values
        self.valid_contact_id = 1
        self.invalid_contact_id = 42
        self.current_version = 'v1'
        # Default tests data
        self.valid_contact_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1990-10-20'
        }
        self.empty_contact_data = {
            'first_name': '',
            'last_name': '',
            'date_of_birth': ''
        }

    def create_contact(self, data):
        """
        Perform a POST request to create a new contact
        :param data:
        :return:
        """
        return self.client.post(
            reverse('contacts-list', kwargs={'version': self.current_version}),
            data=json.dumps(data),
            content_type='application/json'
        )

    def update_contact(self, contact_id, new_data):
        """
        Perform a PUT request to update an existing contact
        :param contact_id:
        :param new_data:
        :return:
        """
        return self.client.put(
            reverse('contact-details', kwargs={'version': self.current_version, 'contact_id': contact_id}),
            data=json.dumps(new_data),
            content_type='application/json'
        )

    def fetch_contact(self, contact_id):
        """
        Perform a GET request to retrieve an existing contact by your id
        :param contact_id:
        :return:
        """
        return self.client.get(
            reverse('contact-details', kwargs={'version': self.current_version, 'contact_id': contact_id})
        )

    def remove_contact(self, contact_id):
        """
        Perform a DELETE request to remove an existing contact by your id
        :param contact_id:
        :return:
        """
        return self.client.delete(
            reverse('contact-details', kwargs={'version': self.current_version, 'contact_id': contact_id})
        )
