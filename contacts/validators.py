from django.core.exceptions import ValidationError


def validate_address_dict(address):
    if not all(*address.values()):
        raise ValidationError
