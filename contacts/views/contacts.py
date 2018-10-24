from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response

from contacts.models import Contact
from contacts.serializers import ContactSerializer, ContactNestedSerializer


class ListContactsView(generics.ListCreateAPIView):
    """
    Provides a GET and POST method handler
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        request.data['phone_numbers'] = list(map(lambda x: {'phone': x}, request.data.get('phone_numbers', [])))
        request.data['emails'] = list(map(lambda x: {'email': x}, request.data.get('emails', [])))

        serializer = ContactNestedSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        created_contact = serializer.create(serializer.validated_data)

        return Response(data=self.serializer_class(created_contact).data, status=status.HTTP_201_CREATED)


class ContactDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    lookup_url_kwarg = 'contact_id'
