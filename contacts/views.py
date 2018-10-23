from django.db import IntegrityError
from rest_framework import generics, status
from rest_framework.response import Response

from contacts.decorators import validate_contact_data, validate_phone_number_data, validate_phone_number, \
    validate_emails_data, validate_flat_email_data
from contacts.models import Contact, PhoneNumber, EmailField
from contacts.serializers import ContactSerializer, PhoneNumberSerializer, EmailFieldSerializer


class ListContactsView(generics.ListCreateAPIView):
    """
    Provides a GET and POST method handler
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    @validate_contact_data
    @validate_phone_number_data
    @validate_emails_data
    def post(self, request, *args, **kwargs):
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
        return Response(data=self.serializer_class(created_contact).data, status=status.HTTP_201_CREATED)


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


class ListPhoneNumbersView(generics.ListCreateAPIView):
    """
    Provides a GET and POST method handler
    """
    serializer_class = PhoneNumberSerializer

    def get_queryset(self):
        return PhoneNumber.objects.filter(contact_id=self.kwargs['contact_id'])

    @validate_phone_number
    def post(self, request, *args, **kwargs):
        try:
            requested_contact = Contact.objects.get(pk=kwargs['contact_id'])
            inserted_phone = PhoneNumber.objects.create(
                contact=requested_contact,
                phone=request.data['phone'],
                primary=request.data.get('primary', False)
            )
            return Response(self.serializer_class(inserted_phone).data, status=status.HTTP_201_CREATED)
        except Contact.DoesNotExist:
            return Response(data={'message': 'The requested contact does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return Response(
                data={'message': 'This phone is already registered for the requested contact'},
                status=status.HTTP_409_CONFLICT
            )


class PhoneNumbersDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PhoneNumberSerializer

    def get(self, request, *args, **kwargs):
        try:
            requested_contact = Contact.objects.get(pk=kwargs['contact_id'])
            retrieved_phone_number = requested_contact.phone_numbers.get(phone=kwargs['phone_number'])
            return Response(self.serializer_class(retrieved_phone_number).data)
        except Contact.DoesNotExist:
            return Response(data={'message': 'The requested contact does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except PhoneNumber.DoesNotExist:
            return Response(data={'message': 'The requested phone does not exist'}, status=status.HTTP_404_NOT_FOUND)

    @validate_phone_number
    def put(self, request, *args, **kwargs):
        try:
            requested_contact = Contact.objects.get(pk=kwargs['contact_id'])
            original_phone_number = requested_contact.phone_numbers.get(phone=kwargs['phone_number'])
            serializer = self.serializer_class()
            updated_contact = serializer.update(original_phone_number, request.data)
            return Response(self.serializer_class(updated_contact).data)
        except Contact.DoesNotExist:
            return Response(data={'message': 'The requested contact does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except PhoneNumber.DoesNotExist:
            return Response(data={'message': 'The requested phone does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return Response(
                data={'message': 'This phone is already registered for the requested contact'},
                status=status.HTTP_409_CONFLICT
            )

    def delete(self, request, *args, **kwargs):
        try:
            requested_contact = Contact.objects.get(pk=kwargs['contact_id'])
            requested_phone_number = requested_contact.phone_numbers.get(phone=kwargs['phone_number'])
            requested_phone_number.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Contact.DoesNotExist:
            return Response(data={'message': 'The requested contact does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except PhoneNumber.DoesNotExist:
            return Response(data={'message': 'The requested phone does not exist'}, status=status.HTTP_404_NOT_FOUND)


class ListEmailsView(generics.ListCreateAPIView):
    """
    Provides a GET and POST method handler
    """
    serializer_class = EmailFieldSerializer

    def get_queryset(self):
        return EmailField.objects.filter(contact_id=self.kwargs['contact_id'])

    @validate_flat_email_data
    def post(self, request, *args, **kwargs):
        try:
            requested_contact = Contact.objects.get(pk=kwargs['contact_id'])
            inserted_email = EmailField.objects.create(contact=requested_contact, email=request.data['email'])
            return Response(self.serializer_class(inserted_email).data, status=status.HTTP_201_CREATED)
        except Contact.DoesNotExist:
            return Response(data={'message': 'The requested contact does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return Response(data={'message': 'This email is already registered'}, status=status.HTTP_409_CONFLICT)


class EmailDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EmailFieldSerializer

    def get(self, request, *args, **kwargs):
        try:
            requested_contact = Contact.objects.get(pk=kwargs['contact_id'])
            retrieved_email = requested_contact.emails.get(email=kwargs['email'])
            return Response(self.serializer_class(retrieved_email).data)
        except Contact.DoesNotExist:
            return Response(data={'message': 'The requested contact does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except EmailField.DoesNotExist:
            return Response(data={'message': 'The requested email does not exist'}, status=status.HTTP_404_NOT_FOUND)

    @validate_flat_email_data
    def put(self, request, *args, **kwargs):
        try:
            requested_contact = Contact.objects.get(pk=kwargs['contact_id'])
            original_email = requested_contact.emails.get(email=kwargs['email'])
            serializer = self.serializer_class()
            updated_contact = serializer.update(original_email, request.data)
            return Response(self.serializer_class(updated_contact).data)
        except Contact.DoesNotExist:
            return Response(data={'message': 'The requested contact does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except EmailField.DoesNotExist:
            return Response(data={'message': 'The requested email does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return Response(
                data={'message': 'This email is already registered'},
                status=status.HTTP_409_CONFLICT
            )

    def delete(self, request, *args, **kwargs):
        try:
            requested_contact = Contact.objects.get(pk=kwargs['contact_id'])
            requested_email = requested_contact.emails.get(email=kwargs['email'])
            requested_email.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Contact.DoesNotExist:
            return Response(data={'message': 'The requested contact does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except EmailField.DoesNotExist:
            return Response(data={'message': 'The requested email does not exist'}, status=status.HTTP_404_NOT_FOUND)
