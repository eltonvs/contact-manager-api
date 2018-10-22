from rest_framework import status
from rest_framework.response import Response


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


def validate_phone_number(func):
    def decorated(*args, **kwargs):
        phone = args[0].request.data.get('phone', '')

        if not phone:
            return Response(data={"message": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)
        return func(*args, **kwargs)

    return decorated
