from django.db import IntegrityError
from rest_framework import generics, status
from rest_framework.response import Response

from contacts.decorators import validate_flat_address_data
from contacts.models import Contact, AddressField
from contacts.serializers import AddressSerializer


class ListAddressesView(generics.ListCreateAPIView):
    """
    Provides a GET and POST method handler
    """
    serializer_class = AddressSerializer

    def get_queryset(self):
        return AddressField.objects.filter(contact_id=self.kwargs['contact_id'])

    @validate_flat_address_data
    def post(self, request, *args, **kwargs):
        try:
            requested_contact = Contact.objects.get(pk=kwargs['contact_id'])
            inserted_address = AddressField.objects.create(
                contact=requested_contact,
                address=request.data['address'],
                city=request.data['city'],
                state=request.data['state'],
                country=request.data['country'],
                zip_code=request.data['zip_code']
            )
            return Response(self.serializer_class(inserted_address).data, status=status.HTTP_201_CREATED)
        except Contact.DoesNotExist:
            return Response(data={'message': 'The requested contact does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return Response(
                data={'message': 'This address is already registered for the requested contact'},
                status=status.HTTP_409_CONFLICT
            )


class AddressDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer

    def get(self, request, *args, **kwargs):
        try:
            requested_contact = Contact.objects.get(pk=kwargs['contact_id'])
            retrieved_address = requested_contact.addresses.get(pk=kwargs['address_id'])
            return Response(self.serializer_class(retrieved_address).data)
        except Contact.DoesNotExist:
            return Response(data={'message': 'The requested contact does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except AddressField.DoesNotExist:
            return Response(data={'message': 'The requested address does not exist'}, status=status.HTTP_404_NOT_FOUND)

    @validate_flat_address_data
    def put(self, request, *args, **kwargs):
        try:
            requested_contact = Contact.objects.get(pk=kwargs['contact_id'])
            original_address = requested_contact.addresses.get(pk=kwargs['address_id'])
            serializer = self.serializer_class()
            updated_contact = serializer.update(original_address, request.data)
            return Response(self.serializer_class(updated_contact).data)
        except Contact.DoesNotExist:
            return Response(data={'message': 'The requested contact does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except AddressField.DoesNotExist:
            return Response(data={'message': 'The requested address does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return Response(
                data={'message': 'This address is already registered for the requested contact'},
                status=status.HTTP_409_CONFLICT
            )

    def delete(self, request, *args, **kwargs):
        try:
            requested_contact = Contact.objects.get(pk=kwargs['contact_id'])
            requested_address = requested_contact.addresses.get(pk=kwargs['address_id'])
            requested_address.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Contact.DoesNotExist:
            return Response(data={'message': 'The requested contact does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except AddressField.DoesNotExist:
            return Response(data={'message': 'The requested address does not exist'}, status=status.HTTP_404_NOT_FOUND)
