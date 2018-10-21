import json
from datetime import date
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APITestCase, APIClient

from contacts.models import Contact, PhoneNumber
from contacts.serializers import ContactSerializer


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def insert_contact(first_name, last_name, date_of_birth, phone_numbers):
        """
        Create a contact and store on database
        :param first_name:
        :param last_name:
        :param date_of_birth:
        :param phone_numbers:
        """
        if first_name != '' and last_name != '' and date_of_birth and phone_numbers:
            contact = Contact.objects.create(first_name=first_name, last_name=last_name, date_of_birth=date_of_birth)
            for phone_number in phone_numbers:
                PhoneNumber.objects.create(
                    contact=contact, phone=phone_number['phone'], primary=phone_number.get('primary', False)
                )

    def setUp(self):
        # Populate database
        self.insert_contact('Elton', 'John', date(1947, 3, 25), [{'phone': '+44 7911 123456', 'primary': True}])
        self.insert_contact('Elvis', 'Presley', date(1935, 1, 8), [{'phone': '+1 123 456 7890', 'primary': True}])
        self.insert_contact(
            'Marilyn', 'Monroe', date(1926, 6, 1),
            [{'phone': '+1 000 111 2222', 'primary': True}, {'phone': '+1 321 654 0987'}]
        )
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
        }
        self.valid_phone_data = {
            'phone_numbers': [
                {
                    'phone': '+1 202 555 0104',
                    'primary': True
                },
            ]
        }
        self.valid_multiple_phone_data = {
            'phone_numbers': [
                {
                    'phone': '+1 202 555 0104',
                    'primary': True
                },
                {
                    'phone': '+2 123 456 7890',
                    'primary': False
                },
                {
                    'phone': '+55 999 999 999',
                    'primary': False
                },
            ]
        }
        self.invalid_multiple_phone_data = {
            'phone_numbers': [
                {
                    'phone': '+1 202 555 0104',
                    'primary': True
                },
                {
                    'phone': '+2 123 456 7890',
                    'primary': False
                },
                {
                    'phone': '+55 999 999 999',
                    'primary': False
                },
                {
                    'phone': ''
                }
            ]
        }
        self.empty_phone_data = {
            'phone_numbers': []
        }
        self.phone_data_with_empty_phone = {
            'phone_numbers': [{'phone': ''}]
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


class GetAllContactsTest(BaseViewTest):
    def test_get_all_contacts(self):
        """
        This ensures that all contacts added in the setUp method
        exist when we make a GET request to the contacts/ endpoint
        """
        # Retrieve response from API
        response = self.client.get(reverse('contacts-list', kwargs={'version': self.current_version}))

        # Fetch data from database
        expected = Contact.objects.all()
        serialized = ContactSerializer(expected, many=True)

        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetAContactTest(BaseViewTest):
    def test_get_a_contact(self):
        """
        This test ensures that a single contact (with a given id) can be retrieved
        """
        # Retrieve response from API
        response = self.fetch_contact(self.valid_contact_id)

        # Fetch data from database
        expected = Contact.objects.get(pk=self.valid_contact_id)
        serialized = ContactSerializer(expected)

        self.assertEqual(response.json(), serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_a_contact_with_multiple_phones(self):
        """
        This test ensures that a single contact (with a given id) can be retrieved
        """
        # Retrieve response from API
        response = self.fetch_contact(self.valid_contact_id_with_multiple_phones)

        # Fetch data from database
        expected = Contact.objects.get(pk=self.valid_contact_id_with_multiple_phones)
        serialized = ContactSerializer(expected)

        self.assertEqual(response.json(), serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_a_nonexistent_contact(self):
        """
        This test ensures that a nonexistent contact cannot be retrieved
        """
        # Retrieve response from API
        response = self.fetch_contact(self.invalid_contact_id)

        self.assertTrue('not exist' in response.data['message'])
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateContactTest(BaseViewTest):
    def test_create_a_contact(self):
        """
        This test ensures that a single contact can be created
        """
        # Use the API endpoint to create a new contact
        contact_data = {**self.valid_contact_data, **self.valid_phone_data}
        response = self.create_contact(contact_data)

        self.assertEqual(response.json(), contact_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_a_contact_with_multiple_phones(self):
        """
        This test ensures that a single contact can be created
        """
        # Use the API endpoint to create a new contact
        contact_data = {**self.valid_contact_data, **self.valid_multiple_phone_data}
        response = self.create_contact(contact_data)

        self.assertEqual(response.json(), contact_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_a_contact_with_invalid_multiple_phones(self):
        """
        This test ensures that a single contact can be created
        """
        # Use the API endpoint to create a new contact
        contact_data = {**self.valid_contact_data, **self.invalid_multiple_phone_data}
        response = self.create_contact(contact_data)

        self.assertTrue('required' in response.data['message'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_a_contact_without_a_phone(self):
        """
        This test ensures that a single contact can be created
        """
        # Use the API endpoint to create a new contact
        response = self.create_contact(self.valid_contact_data)

        self.assertTrue('required' in response.data['message'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_a_contact_with_an_empty_list_of_phones(self):
        """
        This test ensures that a single contact can be created
        """
        # Use the API endpoint to create a new contact
        contact_data = {**self.valid_contact_data, **self.empty_phone_data}
        response = self.create_contact(contact_data)

        self.assertTrue('required' in response.data['message'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_a_contact_with_an_empty_phone(self):
        """
        This test ensures that a single contact can be created
        """
        # Use the API endpoint to create a new contact
        contact_data = {**self.valid_contact_data, **self.phone_data_with_empty_phone}
        response = self.create_contact(contact_data)

        self.assertTrue('required' in response.data['message'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_an_empty_contact_without_phone(self):
        """
        This test ensures that an empty contact cannot be created
        """
        # Use the API endpoint to create a new contact
        response = self.create_contact(self.empty_contact_data)

        self.assertTrue('required' in response.data['message'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_an_empty_contact_with_an_empty_phone(self):
        """
        This test ensures that an empty contact cannot be created
        """
        # Use the API endpoint to create a new contact
        contact_data = {**self.valid_contact_data, **self.empty_phone_data}
        response = self.create_contact(contact_data)

        self.assertTrue('required' in response.data['message'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_an_empty_contact_with_a_valid_phone(self):
        """
        This test ensures that an empty contact cannot be created
        """
        # Use the API endpoint to create a new contact
        contact_data = {**self.empty_contact_data, **self.valid_phone_data}
        response = self.create_contact(contact_data)

        self.assertTrue('required' in response.data['message'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateContactTest(BaseViewTest):
    def test_update_a_contact(self):
        """
        This test ensures that a single contact can be updated
        """
        # Use the API endpoint to update a contact
        contact_phones = {'phone_numbers': [{'phone': '+1 123 456 7890', 'primary': True}]}
        contact_data = {**self.valid_contact_data, **contact_phones}
        response = self.update_contact(contact_id=2, new_data=self.valid_contact_data)

        self.assertEqual(response.json(), contact_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_an_nonexistent_contact(self):
        """
        This test ensures that a nonexistent contact cannot be updated
        """
        # Use the API endpoint to update a contact
        response = self.update_contact(contact_id=self.invalid_contact_id, new_data=self.valid_contact_data)

        self.assertTrue('not exist' in response.data['message'])
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_a_contact_with_empty_values(self):
        """
        This test ensures that a single contact cannot be updated with empty data
        """
        # Use the API endpoint to update a contact
        response = self.update_contact(contact_id=2, new_data=self.empty_contact_data)

        self.assertTrue('required' in response.data['message'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RemoveContactTest(BaseViewTest):
    def test_remove_a_contact(self):
        """
        This test ensures that a single contact can be removed
        """
        # Use the API endpoint to remove a contact
        response = self.remove_contact(1)
        try:
            Contact.objects.get(pk=1)
            self.fail()
        except Contact.DoesNotExist:
            pass

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_remove_an_nonexistent_contact(self):
        """
        This test ensures that a nonexistent contact cannot be removed
        """
        # Use the API endpoint to remove a contact
        response = self.remove_contact(self.invalid_contact_id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
