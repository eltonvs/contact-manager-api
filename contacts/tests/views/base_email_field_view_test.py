import json
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from contacts.models import EmailField


class BaseEmailFieldViewTest(APITestCase):
    client = APIClient()
    fixtures = ['initial_data.json']

    @staticmethod
    def insert_email(contact_id, email):
        """
        Add a email to a contact
        :param contact_id:
        :param email:
        """
        if contact_id and email:
            EmailField.objects.create(contact_id=contact_id, email=email)

    def setUp(self):
        # Default Values
        self.valid_contact_id = 1
        self.valid_contact_email = 'elton_john@example.com'
        self.nonexistent_contact_id = 42
        self.current_version = 'v1'
        # Default tests data
        self.valid_email_data = {'email': 'valid@example.com'}
        self.empty_email_data = {}
        self.invalid_email_data = {'email': '123'}
        self.valid_email = 'valid@example.com'
        self.nonexistent_email = 'unknown@example.com'

    def add_email(self, contact_id, data):
        """
        Perform a POST request to add a email to a contact
        :param contact_id:
        :param data:
        :return:
        """
        return self.client.post(
            reverse('emails-list', kwargs={'version': self.current_version, 'contact_id': contact_id}),
            data=json.dumps(data),
            content_type='application/json'
        )

    def update_email(self, contact_id, email, new_data):
        """
        Perform a PUT request to update an existing email from a contact
        :param contact_id:
        :param email:
        :param new_data:
        :return:
        """
        return self.client.put(
            reverse('email-details',
                    kwargs={'version': self.current_version, 'contact_id': contact_id, 'email': email}),
            data=json.dumps(new_data),
            content_type='application/json'
        )

    def fetch_all_emails(self, contact_id):
        """
        Perform a GET request to retrieve all existing emails from a contact
        :param contact_id:
        :return:
        """
        return self.client.get(
            reverse('emails-list', kwargs={'version': self.current_version, 'contact_id': contact_id})
        )

    def fetch_email(self, contact_id, email):
        """
        Perform a GET request to retrieve an existing email from a contact
        :param contact_id:
        :param email:
        :return:
        """
        return self.client.get(
            reverse('email-details', kwargs={'version': self.current_version, 'contact_id': contact_id, 'email': email})
        )

    def remove_email(self, contact_id, email):
        """
        Perform a DELETE request to remove an existing email from a contact
        :param contact_id:
        :param email:
        :return:
        """
        return self.client.delete(
            reverse('email-details', kwargs={'version': self.current_version, 'contact_id': contact_id, 'email': email})
        )
