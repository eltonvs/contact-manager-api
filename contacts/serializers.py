from rest_framework import serializers

from contacts.models import Contact, PhoneNumber


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ('phone', 'primary')


class ContactSerializer(serializers.ModelSerializer):
    phone_numbers = PhoneNumberSerializer(many=True)

    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'date_of_birth', 'phone_numbers')
