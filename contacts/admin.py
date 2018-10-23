from django.contrib import admin

from contacts.models import Contact, PhoneNumber, EmailField

admin.site.register(Contact)
admin.site.register(PhoneNumber)
admin.site.register(EmailField)
