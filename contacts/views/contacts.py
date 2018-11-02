import datetime
from django.db import transaction
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from contacts.models import Contact
from contacts.serializers import ContactSerializer, ContactNestedSerializer


class SearchContactsView(generics.ListAPIView):
    serializer_class = ContactSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        by_first_name = Contact.objects.filter(first_name__icontains=query)
        by_last_name = Contact.objects.filter(last_name__icontains=query)
        by_email = Contact.objects.filter(emails__email__icontains=query)
        by_phone = Contact.objects.filter(phone_numbers__phone__icontains=query)
        queryset = by_first_name | by_last_name | by_email | by_phone

        if queryset:
            return queryset.order_by('first_name', 'last_name').distinct()
        else:
            raise NotFound()


class BirthdaysView(generics.ListAPIView):
    serializer_class = ContactSerializer

    def get_queryset(self):
        today = datetime.datetime.now()
        queryset = Contact.objects.filter(date_of_birth__month=today.month)

        if queryset:
            return queryset.order_by('date_of_birth__day', 'first_name', 'last_name')
        else:
            raise NotFound()


class ListContactsView(generics.ListCreateAPIView):
    """
    Provides a GET and POST method handler
    """
    queryset = Contact.objects.all().order_by('first_name', 'last_name')
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
