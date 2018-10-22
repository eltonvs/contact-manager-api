from datetime import date

import json
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from contacts.models import PhoneNumber
from contacts.tests.views.base_contact_view_test import BaseContactViewTest


class BasePhoneNumbersViewTest(APITestCase):
    client = APIClient()

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
        # Populate database
        BaseContactViewTest.insert_contact(
            'Elton', 'John', date(1947, 3, 25), [{'phone': '+44 7911 123456', 'primary': True}]
        )
        BaseContactViewTest.insert_contact(
            'Elvis', 'Presley', date(1935, 1, 8), [{'phone': '+1 123 456 7890', 'primary': True}]
        )
        BaseContactViewTest.insert_contact(
            'Marilyn', 'Monroe', date(1926, 6, 1),
            [{'phone': '+1 000 111 2222', 'primary': True}, {'phone': '+1 321 654 0987'}]
        )
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
