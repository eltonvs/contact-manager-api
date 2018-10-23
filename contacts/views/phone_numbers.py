from django.db import IntegrityError
from rest_framework import generics, status
from rest_framework.response import Response

from contacts.decorators import validate_phone_number
from contacts.models import PhoneNumber, Contact
from contacts.serializers import PhoneNumberSerializer


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
            if requested_contact.phone_numbers.count() > 1:
                requested_phone_number.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

            return Response(data={'message': 'This phone cannot be deleted'}, status=status.HTTP_400_BAD_REQUEST)
        except Contact.DoesNotExist:
            return Response(data={'message': 'The requested contact does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except PhoneNumber.DoesNotExist:
            return Response(data={'message': 'The requested phone does not exist'}, status=status.HTTP_404_NOT_FOUND)
