from rest_framework import serializers

from contacts.models import Contact, PhoneNumber, EmailField


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ('phone', 'primary')


class EmailFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailField
        fields = ('email',)


class AddressSerializer(serializers.ModelSerializer):
    pass


class ContactSerializer(serializers.ModelSerializer):
    phone_numbers = PhoneNumberSerializer(many=True)
    emails = serializers.SlugRelatedField(many=True, queryset=[], slug_field='email')

    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'date_of_birth', 'phone_numbers', 'emails')
