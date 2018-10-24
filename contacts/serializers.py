from django.db import transaction, IntegrityError
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
        fields = ('id', 'address', 'city', 'state', 'country', 'zip_code')


class ContactSerializer(serializers.ModelSerializer):
    phone_numbers = serializers.SlugRelatedField(many=True, read_only=True, slug_field='phone')
    emails = serializers.SlugRelatedField(many=True, read_only=True, slug_field='email')
    addresses = AddressSerializer(many=True, required=False)

    class Meta:
        model = Contact
        fields = ('id', 'first_name', 'last_name', 'date_of_birth', 'phone_numbers', 'emails', 'addresses')


class ContactNestedSerializer(serializers.ModelSerializer):
    phone_numbers = PhoneNumberSerializer(many=True, required=True)
    emails = EmailFieldSerializer(many=True, required=True)
    addresses = AddressSerializer(many=True, required=False)

    @transaction.atomic
    def create(self, validated_data):
        phone_numbers_data = validated_data.pop('phone_numbers')
        emails_data = validated_data.pop('emails')
        addresses_data = validated_data.pop('addresses')

        created_contact = self.Meta.model.objects.create(**validated_data)

        if not phone_numbers_data:
            raise serializers.ValidationError({'phone_numbers': ['This field is required.']})
        for phone_data in phone_numbers_data:
            phone_serializer = PhoneNumberSerializer(PhoneNumber(contact=created_contact), data=phone_data)
            phone_serializer.is_valid(raise_exception=True)
            phone_serializer.save()

        if not emails_data:
            raise serializers.ValidationError({'emails': ['This field is required.']})
        for email_data in emails_data:
            email_serializer = EmailFieldSerializer(EmailField(contact=created_contact), data=email_data)
            email_serializer.is_valid(raise_exception=True)
            email_serializer.save()

        for address_data in addresses_data:
            address_serializer = AddressSerializer(AddressField(contact=created_contact), data=address_data)
            address_serializer.is_valid(raise_exception=True)
            try:
                address_serializer.save()
            except IntegrityError:
                raise serializers.ValidationError({'addresses': 'This field is already registered'})

        return created_contact

    class Meta:
        model = Contact
        fields = '__all__'
