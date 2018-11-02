from rest_framework import status

from contacts.models import Contact, PhoneNumber
from contacts.serializers import PhoneNumberSerializer
from contacts.tests.views.base_phone_numbers_view_test import BasePhoneNumbersViewTest


class GetAllPhoneNumbersFromAContactTest(BasePhoneNumbersViewTest):
    def test_get_all_phone_numbers_from_a_contact(self):
        """
        This ensures that all phone numbers added in the setUp method to a contact
        exist when we make a GET request to the contacts/{id}/phone_numbers endpoint
        """
        # Retrieve response from API
        response = self.fetch_all_phone_numbers(self.valid_contact_id)

        # Fetch data from database
        expected = Contact.objects.get(pk=self.valid_contact_id).phone_numbers
        serialized = PhoneNumberSerializer(expected, many=True)

        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetAPhoneNumberTest(BasePhoneNumbersViewTest):
    def test_get_a_phone_number(self):
        """
        This test ensures that a single phone number (from a given contact) can be retrieved
        """
        # Retrieve response from API
        response = self.fetch_phone_number(self.valid_contact_id, self.valid_contact_phone_number)

        # Fetch data from database
        expected = PhoneNumber.objects.get(contact_id=self.valid_contact_id, phone=self.valid_contact_phone_number)
        serialized = PhoneNumberSerializer(expected)

        self.assertEqual(response.json(), serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_a_nonexistent_phone_number(self):
        """
        This test ensures that a nonexistent phone number cannot be retrieved
        """
        # Retrieve response from API
        response = self.fetch_phone_number(self.valid_contact_id, self.nonexistent_phone_number)

        self.assertTrue('not found' in response.data['detail'].lower())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_a_phone_number_from_a_nonexistent_contact(self):
        """
        This test ensures that a phone number from a nonexistent contact cannot be retrieved
        """
        # Retrieve response from API
        response = self.fetch_phone_number(self.nonexistent_contact_id, self.valid_phone_number)

        self.assertTrue('not found' in response.data['detail'].lower())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AddAPhoneNumberToAContactTest(BasePhoneNumbersViewTest):
    def test_add_a_phone_number_to_a_contact(self):
        """
        This test ensures that a single phone number can be added to a contact
        """
        # Use the API endpoint to add a phone number to a contact
        response = self.add_phone_number(self.valid_contact_id, self.valid_phone_number_data)

        self.assertEqual(response.json(), self.valid_phone_number_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_a_duplicate_phone_number_to_a_contact(self):
        """
        This test ensures that a contact cannot have duplicated phone numbers
        """
        # Use the API endpoint to add a duplicated phone number to a contact
        phone_number_data = {'phone': self.valid_contact_phone_number}
        response = self.add_phone_number(self.valid_contact_id, phone_number_data)

        self.assertTrue(len(response.data['phone']) > 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_an_empty_phone_number_to_a_contact(self):
        """
        This test ensures that an empty phone number cannot be added to a contact
        """
        # Use the API endpoint to add a phone number to a contact
        response = self.add_phone_number(self.valid_contact_id, self.empty_phone_number_data)

        self.assertTrue(len(response.data['phone']) > 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_an_invalid_phone_number_to_a_contact(self):
        """
        This test ensures that an empty phone number cannot be added to a contact
        """
        # Use the API endpoint to add a phone number to a contact
        response = self.add_phone_number(self.valid_contact_id, self.invalid_phone_number_data)

        self.assertTrue(len(response.data['phone']) > 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_another_invalid_phone_number_to_a_contact(self):
        """
        This test ensures that an empty phone number cannot be added to a contact
        """
        # Use the API endpoint to add a phone number to a contact
        response = self.add_phone_number(self.valid_contact_id, {'phone': 'invalid'})

        self.assertTrue(len(response.data['phone']) > 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_a_phone_number_to_a_nonexistent_contact(self):
        """
        This test ensures that an empty phone number cannot be added to a contact
        """
        # Use the API endpoint to add a phone number to a contact
        response = self.add_phone_number(self.nonexistent_contact_id, self.valid_phone_number_data)

        self.assertTrue('not found' in response.data['detail'].lower())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateAPhoneNumberFromAContactTest(BasePhoneNumbersViewTest):
    def test_update_a_phone_number_from_a_contact(self):
        """
        This test ensures that a single phone number from a contact can be updated
        """
        # Use the API endpoint to update a contact
        response = self.update_phone_number(
            contact_id=self.valid_contact_id,
            phone_number=self.valid_contact_phone_number,
            new_data=self.valid_phone_number_data
        )

        self.assertEqual(response.json(), self.valid_phone_number_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_a_phone_number_from_a_contact_with_a_duplicated_value(self):
        """
        This test ensures that a single phone number from a contact can be updated
        """
        self.insert_phone_number(self.valid_contact_id, self.valid_phone_number_data['phone'])
        # Use the API endpoint to update a contact
        response = self.update_phone_number(
            contact_id=self.valid_contact_id,
            phone_number=self.valid_contact_phone_number,
            new_data=self.valid_phone_number_data
        )

        self.assertTrue(len(response.data['phone']) > 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_a_phone_number_with_empty_values(self):
        """
        This test ensures that a single phone number from a contact cannot be updated to an empty one
        """
        # Use the API endpoint to update a contact
        response = self.update_phone_number(
            contact_id=self.valid_contact_id,
            phone_number=self.valid_contact_phone_number,
            new_data=self.empty_phone_number_data
        )

        self.assertTrue(len(response.data['phone']) > 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_a_phone_number_with_invalid_values(self):
        """
        This test ensures that a single phone number from a contact can be updated with invalid values
        """
        # Use the API endpoint to update a contact
        response = self.update_phone_number(
            contact_id=self.valid_contact_id,
            phone_number=self.valid_contact_phone_number,
            new_data=self.invalid_phone_number_data
        )

        self.assertTrue(len(response.data['phone']) > 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_a_phone_number_from_a_nonexistent_contact(self):
        """
        This test ensures that a single phone number from a nonexistent contact cannot be updated
        """
        # Use the API endpoint to update a contact
        response = self.update_phone_number(
            contact_id=self.nonexistent_contact_id,
            phone_number=self.valid_contact_phone_number,
            new_data=self.valid_phone_number_data
        )

        self.assertTrue('not found' in response.data['detail'].lower())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_a_nonexistent_phone_number_from_a_contact(self):
        """
        This test ensures that a nonexistent phone number from a contact cannot be updated
        """
        # Use the API endpoint to update a contact
        response = self.update_phone_number(
            contact_id=self.valid_contact_id,
            phone_number=self.nonexistent_phone_number,
            new_data=self.valid_phone_number_data
        )

        self.assertTrue('not found' in response.data['detail'].lower())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class RemoveAPhoneNumberFromAContactTest(BasePhoneNumbersViewTest):
    def test_remove_a_phone_number_from_a_contact(self):
        """
        This test ensures that a single contact can be removed
        """
        # Use the API endpoint to remove a contact
        contact_phone_number = '+1 000 111 2222'
        response = self.remove_phone_number(contact_id=3, phone_number=contact_phone_number)

        try:
            PhoneNumber.objects.get(contact_id=self.valid_contact_id, phone=contact_phone_number)
            self.fail()
        except PhoneNumber.DoesNotExist:
            pass

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_remove_the_last_phone_number_from_a_contact(self):
        """
        This test ensures that the last single phone number from a contact cannot be removed
        """
        # Use the API endpoint to remove a contact
        response = self.remove_phone_number(
            contact_id=self.valid_contact_id,
            phone_number=self.valid_contact_phone_number
        )

        phone_number = PhoneNumber.objects.get(contact_id=self.valid_contact_id, phone=self.valid_contact_phone_number)

        self.assertEqual(phone_number.phone, self.valid_contact_phone_number)
        self.assertTrue(len(response.data['phone']) > 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_remove_a_nonexistent_phone_number(self):
        """
        This test ensures that a nonexistent phone number from a contact cannot be removed
        """
        # Use the API endpoint to remove a contact
        response = self.remove_phone_number(
            contact_id=self.valid_contact_id,
            phone_number=self.nonexistent_phone_number
        )

        self.assertTrue('not found' in response.data['detail'].lower())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_a_phone_number_from_a_nonexistent_contact(self):
        """
        This test ensures that a phone number from a nonexistent contact cannot be removed
        """
        # Use the API endpoint to remove a contact
        response = self.remove_phone_number(
            contact_id=self.nonexistent_contact_id,
            phone_number=self.valid_phone_number
        )

        self.assertTrue('not found' in response.data['detail'].lower())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
