from django.core.validators import RegexValidator
from django.db import models


class Contact(models.Model):
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    date_of_birth = models.DateField(editable=True)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class PhoneNumber(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='phone_numbers')
    phone_regex = RegexValidator(regex=r'^\+(?:[0-9] ?){6,14}[0-9]$')
    phone = models.CharField(validators=[phone_regex], max_length=20, unique=True)

    def __str__(self):
        return self.phone


class EmailField(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='emails')
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


class AddressField(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='addresses')
    address = models.CharField(max_length=512)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)

    class Meta:
        unique_together = ('contact', 'address', 'city', 'state', 'country', 'zip_code')

    def __str__(self):
        return "{}, {} - {}, {}, {}".format(self.address, self.city, self.state, self.country, self.zip_code)
