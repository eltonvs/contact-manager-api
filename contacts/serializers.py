from rest_framework import serializers

from contacts.models import Contact, PhoneNumber, EmailField, AddressField


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ('phone',)


class EmailFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailField
        fields = ('email',)


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressField
        fields = ('address', 'city', 'state', 'country', 'zip_code')


class ContactSerializer(serializers.ModelSerializer):
    phone_numbers = serializers.SlugRelatedField(many=True, queryset=PhoneNumber.objects.all(), slug_field='phone')
    emails = serializers.SlugRelatedField(many=True, queryset=[], slug_field='email')
    addresses = AddressSerializer(many=True)

    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'date_of_birth', 'phone_numbers', 'emails', 'addresses')
