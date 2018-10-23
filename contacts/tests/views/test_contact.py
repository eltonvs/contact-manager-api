from django.urls import reverse
from rest_framework import status

from contacts.models import Contact
from contacts.serializers import ContactSerializer
from contacts.tests.views.base_contact_view_test import BaseContactViewTest


class GetAllContactsTest(BaseContactViewTest):
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


class GetAContactTest(BaseContactViewTest):
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


class CreateContactTest(BaseContactViewTest):
    def test_create_a_contact(self):
        """
        This test ensures that a single contact can be created
        """
        # Use the API endpoint to create a new contact
        contact_data = {**self.valid_contact_data, **self.valid_phone_data, **self.valid_email_data}
        response = self.create_contact(contact_data)

        self.assertEqual(response.json(), contact_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_a_contact_with_multiple_phones(self):
        """
        This test ensures that a single contact can be created
        """
        # Use the API endpoint to create a new contact
        contact_data = {**self.valid_contact_data, **self.valid_multiple_phone_data, **self.valid_email_data}
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


class UpdateContactTest(BaseContactViewTest):
    def test_update_a_contact(self):
        """
        This test ensures that a single contact can be updated
        """
        # Use the API endpoint to update a contact
        contact_phones = {'phone_numbers': [{'phone': '+1 123 456 7890', 'primary': True}]}
        contact_emails = {'emails': ['elvis_presley@example.com']}
        contact_data = {**self.valid_contact_data, **contact_phones, **contact_emails}
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


class RemoveContactTest(BaseContactViewTest):
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
