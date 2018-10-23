from django.core.exceptions import ValidationError


def validate_address_dict(address):
    address_values = [
        address.get('address', ''),
        address.get('city', ''),
        address.get('state', ''),
        address.get('country', ''),
        address.get('zip_code', '')
    ]
    if not all(address_values):
        raise ValidationError('An address cannot have empty fields, thus is not valid')
