from rest_framework import generics, status
from rest_framework.response import Response

from contacts.decorators import validate_contact_data, validate_phone_number_data
from contacts.models import Contact, PhoneNumber
from contacts.serializers import ContactSerializer


class ListContactsView(generics.ListCreateAPIView):
    """
    Provides a GET and POST method handler
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    @validate_contact_data
    @validate_phone_number_data
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
