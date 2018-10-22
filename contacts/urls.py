from django.urls import path

from contacts.views import ListContactsView, ContactDetailsView, ListPhoneNumbersView, PhoneNumbersDetailsView

urlpatterns = [
    path('contacts/', ListContactsView.as_view(), name='contacts-list'),
    path('contacts/<int:contact_id>', ContactDetailsView.as_view(), name='contact-details'),
    path('contacts/<int:contact_id>/phone_numbers', ListPhoneNumbersView.as_view(), name='phone-numbers-list'),
    path('contacts/<int:contact_id>/phone_number/<str:phone_number>', PhoneNumbersDetailsView.as_view(),
         name='phone-number-details')
]
