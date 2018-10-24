from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from contacts.models import Contact, AddressField
from contacts.serializers import AddressSerializer


class ListAddressesView(generics.ListCreateAPIView):
    """
    Provides a GET and POST method handler
    """
    serializer_class = AddressSerializer

    def get_queryset(self):
        return AddressField.objects.filter(contact_id=self.kwargs['contact_id'])

    def post(self, request, *args, **kwargs):
        requested_contact = get_object_or_404(Contact, pk=kwargs['contact_id'])
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.create({**serializer.validated_data, **{'contact': requested_contact}})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError as err:
            raise ValidationError({'address': ['This field is already registered']}) from err


class AddressDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer

    def get(self, request, *args, **kwargs):
        retrieved_address = get_object_or_404(AddressField, contact_id=kwargs['contact_id'], pk=kwargs['address_id'])
        return Response(self.serializer_class(retrieved_address).data)

    def put(self, request, *args, **kwargs):
        original_address = get_object_or_404(AddressField, contact_id=kwargs['contact_id'], pk=kwargs['address_id'])

        serializer = self.serializer_class(original_address, data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
            return Response(serializer.data)
        except IntegrityError as err:
            raise ValidationError({'address': ['This field is already registered']}) from err

    def delete(self, request, *args, **kwargs):
        requested_address = get_object_or_404(AddressField, contact_id=kwargs['contact_id'], pk=kwargs['address_id'])
        requested_address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
