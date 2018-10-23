from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import status
from rest_framework.response import Response

from contacts.validators import validate_address_dict


def validate_contact_data(func):
    def decorated(*args, **kwargs):
        first_name = args[0].request.data.get("first_name", "")
        last_name = args[0].request.data.get("last_name", "")
        date_of_birth = args[0].request.data.get("date_of_birth", None)

        if not first_name or not last_name or not date_of_birth:
            return Response(data={"message": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)
        return func(*args, **kwargs)

    return decorated


def validate_phone_number_data(func):
    def decorated(*args, **kwargs):
        phone_numbers = args[0].request.data.get('phone_numbers', [])
        phones = [phone_number.get('phone', '') for phone_number in phone_numbers]

        if not phone_numbers or not all(phones):
            return Response(data={"message": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)
        return func(*args, **kwargs)

    return decorated


def validate_emails_data(func):
    def decorated(*args, **kwargs):
        emails = args[0].request.data.get('emails', [])

        if not emails or not all(emails):
            return Response(data={'message': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            [validate_email(email) for email in emails]
            return func(*args, **kwargs)
        except ValidationError:
            return Response(data={'message': 'All emails must be valid'}, status=status.HTTP_400_BAD_REQUEST)

    return decorated


def validate_address_data(func):
    def decorated(*args, **kwargs):
        addresses = args[0].request.data.get('addresses', [])

        try:
            [validate_address_dict(address) for address in addresses]
            return func(*args, **kwargs)
        except ValidationError:
            return Response(data={'message': 'All addresses must be valid'}, status=status.HTTP_400_BAD_REQUEST)

    return decorated


def validate_phone_number(func):
    def decorated(*args, **kwargs):
        phone = args[0].request.data.get('phone', '')

        if not phone:
            return Response(data={"message": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)
        return func(*args, **kwargs)

    return decorated


def validate_flat_email_data(func):
    def decorated(*args, **kwargs):
        email = args[0].request.data.get('email', '')

        if not email:
            return Response(data={'message': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_email(email)
            return func(*args, **kwargs)
        except ValidationError:
            return Response(data={'message': 'The email must be valid'}, status=status.HTTP_400_BAD_REQUEST)

    return decorated


def validate_flat_address_data(func):
    def decorated(*args, **kwargs):
        try:
            validate_address_dict(args[0].request.data)
            return func(*args, **kwargs)
        except ValidationError:
            return Response(data={'message': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

    return decorated
