from django.db import models


class Contact(models.Model):
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    date_of_birth = models.DateField(editable=True)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class PhoneNumber(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='phone_numbers')
    phone = models.CharField(max_length=100, blank=False, null=False)
    primary = models.BooleanField(default=False)

    def __str__(self):
        return self.phone
