from rest_framework import status

from contacts.models import Contact, AddressField
from contacts.serializers import AddressSerializer
from contacts.tests.views.base_address_field_view_test import BaseAddressFieldViewTest


class GetAllAddressesFromAContactTest(BaseAddressFieldViewTest):
    def test_get_all_addresses_from_a_contact(self):
        """
        This ensures that all addresses added in the setUp method to a contact
        exist when we make a GET request to the contacts/{id}/addresses endpoint
        """
        # Retrieve response from API
        response = self.fetch_all_addresses(self.valid_contact_id)

        # Fetch data from database
        expected = Contact.objects.get(pk=self.valid_contact_id).addresses
        serialized = AddressSerializer(expected, many=True)

        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetAnAddressTest(BaseAddressFieldViewTest):
    def test_get_an_address(self):
        """
        This test ensures that a single address (from a given contact) can be retrieved
        """
        # Retrieve response from API
        response = self.fetch_address(self.valid_contact_id, self.valid_contact_address_id)

        # Fetch data from database
        expected = AddressField.objects.get(pk=self.valid_contact_address_id, contact_id=self.valid_contact_id)
        serialized = AddressSerializer(expected)

        self.assertEqual(response.json(), serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_a_nonexistent_address(self):
        """
        This test ensures that a nonexistent address cannot be retrieved
        """
        # Retrieve response from API
        response = self.fetch_address(self.valid_contact_id, self.nonexistent_address_id)

        self.assertTrue('not found', response.data['detail'].lower())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_an_address_from_a_nonexistent_contact(self):
        """
        This test ensures that an address from a nonexistent contact cannot be retrieved
        """
        # Retrieve response from API
        response = self.fetch_address(self.nonexistent_contact_id, self.valid_contact_address_id)

        self.assertTrue('not found', response.data['detail'].lower())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AddAnAddressToAContactTest(BaseAddressFieldViewTest):
    def test_add_an_address_to_a_contact(self):
        """
        This test ensures that a single address can be added to a contact
        """
        # Use the API endpoint to add an address to a contact
        response = self.add_address(self.valid_contact_id, self.valid_address)

        self.assertEqual(response.json(), self.valid_address)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_a_duplicated_address_to_a_contact(self):
        """
        This test ensures that a contact cannot have duplicated addresses
        """
        # Use the API endpoint to add a duplicated address to a contact
        response = self.add_address(self.valid_contact_id, self.valid_contact_address_data)

        self.assertTrue(len(response.data['address']) > 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_an_empty_address_to_a_contact(self):
        """
        This test ensures that an empty address cannot be added to a contact
        """
        # Use the API endpoint to add an address to a contact
        response = self.add_address(self.valid_contact_id, self.empty_address_data)

        self.assertTrue(len(response.data['address']) > 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_an_address_to_a_nonexistent_contact(self):
        """
        This test ensures that an empty address cannot be added to a contact
        """
        # Use the API endpoint to add an address to a contact
        response = self.add_address(self.nonexistent_contact_id, self.valid_address)

        self.assertTrue('not found', response.data['detail'].lower())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateAnAddressFromAContactTest(BaseAddressFieldViewTest):
    def test_update_an_address_from_a_contact(self):
        """
        This test ensures that a single address from a contact can be updated
        """
        # Use the API endpoint to update a contact
        response = self.update_address(
            contact_id=self.valid_contact_id,
            address_id=self.valid_contact_address_id,
            new_data=self.valid_address
        )

        self.assertEqual(response.json(), self.valid_address)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_an_address_from_a_contact_with_a_duplicated_value(self):
        """
        This test ensures that a single address from a contact can be updated
        """
        self.insert_address(
            self.valid_contact_id, self.valid_address['address'], self.valid_address['city'],
            self.valid_address['state'], self.valid_address['country'], self.valid_address['zip_code']
        )
        # Use the API endpoint to update a contact
        response = self.update_address(
            contact_id=self.valid_contact_id,
            address_id=self.valid_contact_address_id,
            new_data=self.valid_address
        )

        self.assertTrue(len(response.data['address']) > 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_an_address_with_empty_values(self):
        """
        This test ensures that a single address from a contact cannot be updated to an empty one
        """
        # Use the API endpoint to update a contact
        response = self.update_address(
            contact_id=self.valid_contact_id,
            address_id=self.valid_contact_address_id,
            new_data=self.empty_address_data
        )

        self.assertTrue(len(response.data['address']) > 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_an_address_from_a_nonexistent_contact(self):
        """
        This test ensures that a single address from a nonexistent contact cannot be updated
        """
        # Use the API endpoint to update a contact
        response = self.update_address(
            contact_id=self.nonexistent_contact_id,
            address_id=self.valid_contact_address_id,
            new_data=self.valid_address
        )

        self.assertTrue('not found', response.data['detail'].lower())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_a_nonexistent_address_from_a_contact(self):
        """
        This test ensures that a nonexistent address from a contact cannot be updated
        """
        # Use the API endpoint to update a contact
        response = self.update_address(
            contact_id=self.valid_contact_id,
            address_id=self.nonexistent_address_id,
            new_data=self.valid_address
        )

        self.assertTrue('not found', response.data['detail'].lower())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class RemoveAnAddressFromAContactTest(BaseAddressFieldViewTest):
    def test_remove_an_address_from_a_contact(self):
        """
        This test ensures that a single address from a contact can be removed
        """
        # Use the API endpoint to remove a contact
        response = self.remove_address(
            contact_id=self.valid_contact_id,
            address_id=self.valid_contact_address_id
        )

        try:
            AddressField.objects.get(pk=self.valid_contact_address_id, contact_id=self.valid_contact_id)
            self.fail()
        except AddressField.DoesNotExist:
            pass

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_remove_a_nonexistent_address(self):
        """
        This test ensures that a nonexistent address from a contact cannot be removed
        """
        # Use the API endpoint to remove a contact
        response = self.remove_address(
            contact_id=self.valid_contact_id,
            address_id=self.nonexistent_address_id
        )

        self.assertTrue('not found', response.data['detail'].lower())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_an_address_from_a_nonexistent_contact(self):
        """
        This test ensures that a address from a nonexistent contact cannot be removed
        """
        # Use the API endpoint to remove a contact
        response = self.remove_address(
            contact_id=self.nonexistent_contact_id,
            address_id=self.valid_contact_address_id
        )

        self.assertTrue('not found', response.data['detail'].lower())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
