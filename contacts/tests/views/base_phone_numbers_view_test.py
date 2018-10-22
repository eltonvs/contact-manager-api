import json
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from contacts.models import PhoneNumber


class BasePhoneNumbersViewTest(APITestCase):
    client = APIClient()
    fixtures = ['initial_data.json']

    @staticmethod
    def insert_phone_number(contact_id, phone, is_primary=False):
        """
        Add a phone number to a contact
        :param contact_id:
        :param phone:
        :param is_primary:
        """
        if contact_id and phone:
            PhoneNumber.objects.create(contact_id=contact_id, phone=phone, primary=is_primary)

    def setUp(self):
        # Default Values
        self.valid_contact_id = 1
        self.valid_contact_phone_number = '+44 7911 123456'
        self.nonexistent_contact_id = 42
        self.current_version = 'v1'
        # Default tests data
        self.valid_phone_number_data = {
            'phone': '+1 202 555 0104',
            'primary': True
        }
        self.empty_phone_number_data = {}
        self.invalid_phone_number_data = {'phone': ''}
        self.valid_phone_number = '+55 999 999 999'
        self.nonexistent_phone_number = '+99 9999 9999'

    def add_phone_number(self, contact_id, data):
        """
        Perform a POST request to add a phone number to a contact
        :param contact_id:
        :param data:
        :return:
        """
        return self.client.post(
            reverse('phone-numbers-list', kwargs={'version': self.current_version, 'contact_id': contact_id}),
            data=json.dumps(data),
            content_type='application/json'
        )

    def update_phone_number(self, contact_id, phone_number, new_data):
        """
        Perform a PUT request to update an existing phone number from a contact
        :param contact_id:
        :param phone_number:
        :param new_data:
        :return:
        """
        return self.client.put(
            reverse('phone-number-details',
                    kwargs={'version': self.current_version, 'contact_id': contact_id, 'phone_number': phone_number}),
            data=json.dumps(new_data),
            content_type='application/json'
        )

    def fetch_all_phone_numbers(self, contact_id):
        """
        Perform a GET request to retrieve all existing phone numbers from a contact
        :param contact_id:
        :return:
        """
        return self.client.get(
            reverse('phone-numbers-list', kwargs={'version': self.current_version, 'contact_id': contact_id})
        )

    def fetch_phone_number(self, contact_id, phone_number):
        """
        Perform a GET request to retrieve an existing phone number from a contact
        :param contact_id:
        :param phone_number:
        :return:
        """
        return self.client.get(
            reverse('phone-number-details',
                    kwargs={'version': self.current_version, 'contact_id': contact_id, 'phone_number': phone_number})
        )

    def remove_phone_number(self, contact_id, phone_number):
        """
        Perform a DELETE request to remove an existing phone number from a contact
        :param contact_id:
        :param phone_number:
        :return:
        """
        return self.client.delete(
            reverse('phone-number-details',
                    kwargs={'version': self.current_version, 'contact_id': contact_id, 'phone_number': phone_number})
        )
