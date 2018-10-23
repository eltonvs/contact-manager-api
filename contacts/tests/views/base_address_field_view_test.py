import json
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from contacts.models import AddressField


class BaseAddressFieldViewTest(APITestCase):
    client = APIClient()
    fixtures = ['initial_data.json']

    @staticmethod
    def insert_address(contact_id, address, city, state, country, zip_code):
        """
        Add a email to a contact
        :param contact_id:
        :param address:
        :param city:
        :param state:
        :param country:
        :param zip_code:
        """
        if all([contact_id, address, city, state, country, zip_code]):
            AddressField.objects.create(
                contact_id=contact_id, address=address, city=city, state=state, country=country, zip_code=zip_code
            )

    def setUp(self):
        # Default Values
        self.valid_contact_id = 1
        self.valid_contact_address_id = 1
        self.valid_contact_address_data = {
            'address': '1 Blythe Road',
            'city': 'London',
            'state': 'Hammersmith',
            'country': 'United Kingdom',
            'zip_code': 'W14 0HG'
        }
        self.nonexistent_contact_id = 42
        self.nonexistent_address_id = 42
        self.current_version = 'v1'
        # Default tests data
        self.valid_address = {
            'address': '1722 Heron Way',
            'city': 'Portland',
            'state': 'Oregon',
            'country': 'United States',
            'zip_code': '97205',
        }
        self.valid_address_data = {'address': self.valid_address}
        self.empty_address_data = {}

    def add_address(self, contact_id, data):
        """
        Perform a POST request to add an address to a contact
        :param contact_id:
        :param data:
        :return:
        """
        return self.client.post(
            reverse('addresses-list', kwargs={'version': self.current_version, 'contact_id': contact_id}),
            data=json.dumps(data),
            content_type='application/json'
        )

    def update_address(self, contact_id, address_id, new_data):
        """
        Perform a PUT request to update an existing address from a contact
        :param contact_id:
        :param address_id:
        :param new_data:
        :return:
        """
        return self.client.put(
            reverse('address-details',
                    kwargs={'version': self.current_version, 'contact_id': contact_id, 'address_id': address_id}),
            data=json.dumps(new_data),
            content_type='application/json'
        )

    def fetch_all_addresses(self, contact_id):
        """
        Perform a GET request to retrieve all existing addresses from a contact
        :param contact_id:
        :return:
        """
        return self.client.get(
            reverse('addresses-list', kwargs={'version': self.current_version, 'contact_id': contact_id})
        )

    def fetch_address(self, contact_id, address_id):
        """
        Perform a GET request to retrieve an existing address from a contact
        :param contact_id:
        :param address_id:
        :return:
        """
        return self.client.get(
            reverse('address-details',
                    kwargs={'version': self.current_version, 'contact_id': contact_id, 'address_id': address_id})
        )

    def remove_address(self, contact_id, address_id):
        """
        Perform a DELETE request to remove an existing address from a contact
        :param contact_id:
        :param address_id:
        :return:
        """
        return self.client.delete(
            reverse('address-details',
                    kwargs={'version': self.current_version, 'contact_id': contact_id, 'address_id': address_id})
        )
