from django.urls import path

from contacts.views import ListContactsView, ContactDetailsView

urlpatterns = [
    path('contacts/', ListContactsView.as_view(), name='contacts-list'),
    path('contacts/<int:contact_id>', ContactDetailsView.as_view(), name='contact-details')
]
