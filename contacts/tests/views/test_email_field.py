from rest_framework import status

from contacts.models import Contact, EmailField
from contacts.serializers import EmailFieldSerializer
from contacts.tests.views.base_email_field_view_test import BaseEmailFieldViewTest


class GetAllEmailsFromAContactTest(BaseEmailFieldViewTest):
    def test_get_all_emails_from_a_contact(self):
        """
        This ensures that all emails added in the setUp method to a contact
        exist when we make a GET request to the contacts/{id}/emails endpoint
        """
        # Retrieve response from API
        response = self.fetch_all_emails(self.valid_contact_id)

        # Fetch data from database
        expected = Contact.objects.get(pk=self.valid_contact_id).emails
        serialized = EmailFieldSerializer(expected, many=True)

        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetAEmailTest(BaseEmailFieldViewTest):
    def test_get_a_email(self):
        """
        This test ensures that a single email (from a given contact) can be retrieved
        """
        # Retrieve response from API
        response = self.fetch_email(self.valid_contact_id, self.valid_contact_email)

        # Fetch data from database
        expected = EmailField.objects.get(contact_id=self.valid_contact_id, email=self.valid_contact_email)
        serialized = EmailFieldSerializer(expected)

        self.assertEqual(response.json(), serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_a_nonexistent_email(self):
        """
        This test ensures that a nonexistent email cannot be retrieved
        """
        # Retrieve response from API
        response = self.fetch_email(self.valid_contact_id, self.nonexistent_email)

        self.assertTrue('not exist' in response.data['message'])
        self.assertTrue('email' in response.data['message'])
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_a_email_from_a_nonexistent_contact(self):
        """
        This test ensures that a email from a nonexistent contact cannot be retrieved
        """
        # Retrieve response from API
        response = self.fetch_email(self.nonexistent_contact_id, self.valid_email)

        self.assertTrue('not exist' in response.data['message'])
        self.assertTrue('contact' in response.data['message'])
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AddAEmailToAContactTest(BaseEmailFieldViewTest):
    def test_add_a_email_to_a_contact(self):
        """
        This test ensures that a single email can be added to a contact
        """
        # Use the API endpoint to add a email to a contact
        response = self.add_email(self.valid_contact_id, self.valid_email_data)

        self.assertEqual(response.json(), self.valid_email_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_a_duplicate_email_to_a_contact(self):
        """
        This test ensures that a contact cannot have duplicated emails
        """
        # Use the API endpoint to add a duplicated email to a contact
        email_data = {'email': self.valid_contact_email}
        response = self.add_email(self.valid_contact_id, email_data)

        self.assertTrue('already registered' in response.data['message'])
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_add_an_empty_email_to_a_contact(self):
        """
        This test ensures that an empty email cannot be added to a contact
        """
        # Use the API endpoint to add a email to a contact
        response = self.add_email(self.valid_contact_id, self.empty_email_data)

        self.assertTrue('required' in response.data['message'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_an_invalid_email_to_a_contact(self):
        """
        This test ensures that an empty email cannot be added to a contact
        """
        # Use the API endpoint to add a email to a contact
        response = self.add_email(self.valid_contact_id, self.invalid_email_data)

        self.assertTrue('valid' in response.data['message'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_a_email_to_a_nonexistent_contact(self):
        """
        This test ensures that an empty email cannot be added to a contact
        """
        # Use the API endpoint to add a email to a contact
        response = self.add_email(self.nonexistent_contact_id, self.valid_email_data)

        self.assertTrue('not exist' in response.data['message'])
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateAEmailFromAContactTest(BaseEmailFieldViewTest):
    def test_update_a_email_from_a_contact(self):
        """
        This test ensures that a single email from a contact can be updated
        """
        # Use the API endpoint to update a contact
        response = self.update_email(
            contact_id=self.valid_contact_id,
            email=self.valid_contact_email,
            new_data=self.valid_email_data
        )

        self.assertEqual(response.json(), self.valid_email_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_a_email_from_a_contact_with_a_duplicated_value(self):
        """
        This test ensures that a single email from a contact can be updated
        """
        self.insert_email(self.valid_contact_id, self.valid_email_data['email'])
        # Use the API endpoint to update a contact
        response = self.update_email(
            contact_id=self.valid_contact_id,
            email=self.valid_contact_email,
            new_data=self.valid_email_data
        )

        self.assertTrue('already registered' in response.data['message'])
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_update_a_email_with_empty_values(self):
        """
        This test ensures that a single email from a contact cannot be updated to an empty one
        """
        # Use the API endpoint to update a contact
        response = self.update_email(
            contact_id=self.valid_contact_id,
            email=self.valid_contact_email,
            new_data=self.empty_email_data
        )

        self.assertTrue('required' in response.data['message'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_a_email_with_invalid_values(self):
        """
        This test ensures that a single email from a contact can be updated with invalid values
        """
        # Use the API endpoint to update a contact
        response = self.update_email(
            contact_id=self.valid_contact_id,
            email=self.valid_contact_email,
            new_data=self.invalid_email_data
        )

        self.assertTrue('valid' in response.data['message'])
        self.assertTrue('email' in response.data['message'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_a_email_from_a_nonexistent_contact(self):
        """
        This test ensures that a single email from a nonexistent contact cannot be updated
        """
        # Use the API endpoint to update a contact
        response = self.update_email(
            contact_id=self.nonexistent_contact_id,
            email=self.valid_contact_email,
            new_data=self.valid_email_data
        )

        self.assertTrue('not exist' in response.data['message'])
        self.assertTrue('contact' in response.data['message'])
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_a_nonexistent_email_from_a_contact(self):
        """
        This test ensures that a nonexistent email from a contact cannot be updated
        """
        # Use the API endpoint to update a contact
        response = self.update_email(
            contact_id=self.valid_contact_id,
            email=self.nonexistent_email,
            new_data=self.valid_email_data
        )

        self.assertTrue('not exist' in response.data['message'])
        self.assertTrue('email' in response.data['message'])
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class RemoveAEmailFromAContactTest(BaseEmailFieldViewTest):
    def test_remove_a_email_from_a_contact(self):
        """
        This test ensures that a single email from a contact can be removed
        """
        # Use the API endpoint to remove a contact
        response = self.remove_email(contact_id=self.valid_contact_id, email=self.valid_contact_email)

        try:
            EmailField.objects.get(contact_id=self.valid_contact_id, email=self.valid_contact_email)
            self.fail()
        except EmailField.DoesNotExist:
            pass

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_remove_the_last_email_from_a_contact(self):
        """
        This test ensures that the last single email from a contact cannot be removed
        """
        # Use the API endpoint to remove a contact
        contact_email = 'elvis_presley@example.com'
        response = self.remove_email(contact_id=2, email=contact_email)

        email = EmailField.objects.get(contact_id=2, email=contact_email)

        self.assertEqual(email.email, contact_email)
        self.assertTrue('email' in response.data['message'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_remove_a_nonexistent_email(self):
        """
        This test ensures that a nonexistent email from a contact cannot be removed
        """
        # Use the API endpoint to remove a contact
        response = self.remove_email(
            contact_id=self.valid_contact_id,
            email=self.nonexistent_email
        )

        self.assertTrue('not exist' in response.data['message'])
        self.assertTrue('email' in response.data['message'])
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_a_email_from_a_nonexistent_contact(self):
        """
        This test ensures that a email from a nonexistent contact cannot be removed
        """
        # Use the API endpoint to remove a contact
        response = self.remove_email(
            contact_id=self.nonexistent_contact_id,
            email=self.valid_email
        )

        self.assertTrue('not exist' in response.data['message'])
        self.assertTrue('contact' in response.data['message'])
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
