from django.db import transaction, IntegrityError
from rest_framework import generics, status
from rest_framework.response import Response

from contacts.decorators import validate_contact_data, validate_phone_number_data, validate_emails_data, \
    validate_address_data
from contacts.models import Contact, PhoneNumber, EmailField, AddressField
from contacts.serializers import ContactSerializer


class ListContactsView(generics.ListCreateAPIView):
    """
    Provides a GET and POST method handler
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    @validate_contact_data
    @validate_phone_number_data
    @validate_emails_data
    @validate_address_data
    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                created_contact = Contact.objects.create(
                    first_name=request.data['first_name'],
                    last_name=request.data['last_name'],
                    date_of_birth=request.data['date_of_birth']
                )
                for phone_number in request.data['phone_numbers']:
                    PhoneNumber.objects.create(
                        contact=created_contact,
                        phone=phone_number['phone'],
                        primary=phone_number.get('primary', False)
                    )
                for email in request.data['emails']:
                    EmailField.objects.create(contact=created_contact, email=email)
                for address in request.data['addresses']:
                    AddressField.objects.create(
                        contact=created_contact,
                        address=address['address'],
                        city=address['city'],
                        state=address['state'],
                        country=address['country'],
                        zip_code=address['zip_code']
                    )
                return Response(data=self.serializer_class(created_contact).data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(
                data={'message': 'The contact is not valid. There are attributes with duplicated values'},
                status=status.HTTP_409_CONFLICT
            )


class ContactDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def get(self, request, *args, **kwargs):
        try:
            retrieved_contact = self.queryset.get(pk=kwargs['contact_id'])
            return Response(self.serializer_class(retrieved_contact).data)
        except Contact.DoesNotExist:
            return Response(data={'message': 'The requested contact does not exist'}, status=status.HTTP_404_NOT_FOUND)

    @validate_contact_data
    def put(self, request, *args, **kwargs):
        try:
            original_contact = self.queryset.get(pk=kwargs['contact_id'])
            serializer = self.serializer_class()
            updated_contact = serializer.update(original_contact, request.data)
            return Response(self.serializer_class(updated_contact).data)
        except Contact.DoesNotExist:
            return Response(data={'message': 'The requested contact does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        try:
            requested_contact = self.queryset.get(pk=kwargs['contact_id'])
            requested_contact.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Contact.DoesNotExist:
            return Response(data={'message': 'The requested contact does not exist'}, status=status.HTTP_404_NOT_FOUND)
