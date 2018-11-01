from django.urls import path

from contacts import views

urlpatterns = [
    path('contacts/', views.ListContactsView.as_view(), name='contacts-list'),
    path('contacts/<int:contact_id>', views.ContactDetailsView.as_view(), name='contact-details'),
    path('contacts/search', views.SearchContactsView.as_view(), name='contacts-search'),
    path('contacts/<int:contact_id>/phone_numbers', views.ListPhoneNumbersView.as_view(), name='phone-numbers-list'),
    path('contacts/<int:contact_id>/phone_numbers/<str:phone_number>', views.PhoneNumbersDetailsView.as_view(),
         name='phone-number-details'),
    path('contacts/<int:contact_id>/emails', views.ListEmailsView.as_view(), name='emails-list'),
    path('contacts/<int:contact_id>/emails/<str:email>', views.EmailDetailsView.as_view(), name='email-details'),
    path('contacts/<int:contact_id>/addresses', views.ListAddressesView.as_view(), name='addresses-list'),
    path('contacts/<int:contact_id>/addresses/<int:address_id>', views.AddressDetailsView.as_view(),
         name='address-details')
]
