import json
from django.utils.http import urlencode
from rest_framework.reverse import reverse

from rest_framework.test import APITestCase, APIClient

from contacts.models import Contact, AddressField
from contacts.tests.views.base_address_field_view_test import BaseAddressFieldViewTest
from contacts.tests.views.base_email_field_view_test import BaseEmailFieldViewTest
from contacts.tests.views.base_phone_numbers_view_test import BasePhoneNumbersViewTest


class BaseContactViewTest(APITestCase):
    client = APIClient()
    fixtures = ['initial_data.json']

    @staticmethod
    def insert_contact(first_name, last_name, date_of_birth, phone_numbers, emails, addresses=None):
        """
        Create a contact and store on database
        :param first_name:
        :param last_name:
        :param date_of_birth:
        :param phone_numbers:
        :param emails:
        :param addresses:
        """
        if first_name != '' and last_name != '' and date_of_birth and phone_numbers and emails:
            contact = Contact.objects.create(first_name=first_name, last_name=last_name, date_of_birth=date_of_birth)
            for phone_number in phone_numbers:
                BasePhoneNumbersViewTest.insert_phone_number(contact_id=contact.id, phone=phone_number['phone'])
            for email in emails:
                BaseEmailFieldViewTest.insert_email(contact_id=contact.id, email=email)
            for address in addresses:
                BaseAddressFieldViewTest.insert_address(
                    contact_id=contact.id, address=address['address'], city=address['city'],
                    state=address['state'], country=address['country'], zip_code=address['zip_code']
                )

    def setUp(self):
        # Default Values
        self.valid_contact_id = 1
        self.valid_contact_id_with_multiple_phones = 3
        self.invalid_contact_id = 42
        self.current_version = 'v1'
        # Default tests data
        self.valid_contact_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1990-10-20',
        }
        self.empty_contact_data = {
            'first_name': '',
            'last_name': '',
            'date_of_birth': '',
            'emails': [],
        }
        self.valid_email = 'john_doe@example.com'
        self.valid_email_data = {'emails': [self.valid_email]}
        self.valid_multiple_email_data = {'emails': ['john_doe@example.com', 'me@johndoe.com', 'john@doe.com']}
        self.invalid_multiple_email_data = {'emails': ['john_doe@example.com', 'me@johndoe.com', 'john@doe.com', '123']}
        self.empty_email_data = {'emails': []}
        self.email_data_with_empty_email = {'emails': ['']}
        self.empty_address_data = {'addresses': []}
        self.valid_address = {
            'address': '1722 Heron Way',
            'city': 'Portland',
            'state': 'Oregon',
            'country': 'United States',
            'zip_code': '97205',
        }
        self.address_with_empty_fields = {'address': '', 'city': '', 'state': '', 'country': '', 'zip_code': ''}
        self.valid_address_data = {'addresses': [self.valid_address]}
        self.multiple_valid_address = [{**self.valid_address, **{'city': 'Another City'}}, self.valid_address]
        self.multiple_valid_address_data = {'addresses': self.multiple_valid_address}
        self.multiple_invalid_address_data = {'addresses': [self.valid_address, self.address_with_empty_fields]}
        self.invalid_address_data = {'addresses': [self.address_with_empty_fields]}
        self.address_data_with_empty_address = {'addresses': [{}]}
        self.valid_phone = '+1 202 555 0104'
        self.valid_phone_data = {'phone_numbers': [self.valid_phone]}
        self.valid_multiple_phone_data = {'phone_numbers': ['+1 202 555 0104', '+2 123 456 7890', '+55 999 999 999']}
        self.invalid_multiple_phone_data = {
            'phone_numbers': ['+1 202 555 0104', '+2 123 456 7890', '+55 999 999 999', '']
        }
        self.empty_phone_data = {'phone_numbers': []}
        self.phone_data_with_empty_phone = {'phone_numbers': ['']}

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

    def search_contacts(self, query):
        """
        Perform a GET request to search for contacts that match a given query
        :param query:
        :return:
        """
        url = "{}?{}".format(
            reverse('contacts-search', kwargs={'version': self.current_version}), urlencode({'query': query})
        )
        return self.client.get(url)

    def remove_contact(self, contact_id):
        """
        Perform a DELETE request to remove an existing contact by your id
        :param contact_id:
        :return:
        """
        return self.client.delete(
            reverse('contact-details', kwargs={'version': self.current_version, 'contact_id': contact_id})
        )
