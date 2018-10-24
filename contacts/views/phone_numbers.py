from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from contacts.models import PhoneNumber, Contact
from contacts.serializers import PhoneNumberSerializer


class ListPhoneNumbersView(generics.ListCreateAPIView):
    """
    Provides a GET and POST method handler
    """
    serializer_class = PhoneNumberSerializer

    def get_queryset(self):
        return PhoneNumber.objects.filter(contact_id=self.kwargs['contact_id'])

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        requested_contact = get_object_or_404(Contact, pk=kwargs['contact_id'])
        try:
            serializer.create({**serializer.validated_data, **{'contact': requested_contact}})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(data={'phone': ['This phone is already registered']}, status=status.HTTP_400_BAD_REQUEST)


class PhoneNumbersDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PhoneNumberSerializer

    def get(self, request, *args, **kwargs):
        retrieved_phone = get_object_or_404(PhoneNumber, contact_id=kwargs['contact_id'], phone=kwargs['phone_number'])
        return Response(self.serializer_class(retrieved_phone).data)

    def put(self, request, *args, **kwargs):
        original_phone = get_object_or_404(PhoneNumber, contact_id=kwargs['contact_id'], phone=kwargs['phone_number'])

        serializer = self.serializer_class(original_phone, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return Response(serializer.data)
        except IntegrityError:
            return Response(data={'phone': ['This phone is already registered']}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        requested_contact = get_object_or_404(Contact, pk=kwargs['contact_id'])
        requested_phone = get_object_or_404(PhoneNumber, contact_id=kwargs['contact_id'], phone=kwargs['phone_number'])
        if requested_contact.phone_numbers.count() > 1:
            requested_phone.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(data={'phone': ['This phone cannot be deleted']}, status=status.HTTP_400_BAD_REQUEST)
