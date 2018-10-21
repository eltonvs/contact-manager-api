import json
from datetime import date
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from contacts.models import Contact
from contacts.serializers import ContactSerializer


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
        self.assertEqual(str(self.created_contact), "John Doe")


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

        self.assertEqual(response.data, serialized.data)
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
        response = self.create_contact(self.valid_contact_data)

        self.assertEqual(response.data, self.valid_contact_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_an_empty_contact(self):
        """
        This test ensures that an empty contact cannot be created
        """
        # Use the API endpoint to create a new contact
        response = self.create_contact(self.empty_contact_data)

        self.assertTrue('required' in response.data['message'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateContactTest(BaseViewTest):
    def test_update_a_contact(self):
        """
        This test ensures that a single contact can be updated
        """
        # Use the API endpoint to update a contact
        response = self.update_contact(contact_id=2, new_data=self.valid_contact_data)

        self.assertEqual(response.data, self.valid_contact_data)
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
