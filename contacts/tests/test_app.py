from django.apps import apps
from rest_framework.test import APITestCase

from contacts.apps import ContactsConfig


class ContactConfigTest(APITestCase):
    def test_apps(self):
        self.assertEqual(ContactsConfig.name, 'contacts')
        self.assertEqual(apps.get_app_config('contacts').name, 'contacts')
