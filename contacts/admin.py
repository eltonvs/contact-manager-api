from django.contrib import admin

from contacts.models import Contact, PhoneNumber

admin.site.register(Contact)
admin.site.register(PhoneNumber)
