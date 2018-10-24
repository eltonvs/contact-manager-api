from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from contacts.models import EmailField, Contact
from contacts.serializers import EmailFieldSerializer


class ListEmailsView(generics.ListCreateAPIView):
    """
    Provides a GET and POST method handler
    """
    serializer_class = EmailFieldSerializer

    def get_queryset(self):
        return EmailField.objects.filter(contact_id=self.kwargs['contact_id'])

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        requested_contact = get_object_or_404(Contact, pk=kwargs['contact_id'])
        inserted_email = EmailField.objects.create(contact=requested_contact, **serializer.validated_data)
        return Response(self.serializer_class(inserted_email).data, status=status.HTTP_201_CREATED)


class EmailDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EmailFieldSerializer

    def get(self, request, *args, **kwargs):
        retrieved_email = get_object_or_404(EmailField, contact_id=kwargs['contact_id'], email=kwargs['email'])
        return Response(self.serializer_class(retrieved_email).data)

    def put(self, request, *args, **kwargs):
        original_email = get_object_or_404(EmailField, contact_id=kwargs['contact_id'], email=kwargs['email'])

        serializer = self.serializer_class(original_email, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        requested_contact = get_object_or_404(Contact, pk=kwargs['contact_id'])
        if requested_contact.emails.count() > 1:
            requested_email = get_object_or_404(EmailField, email=kwargs['email'])
            requested_email.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(data={'email': ['This email cannot be deleted']}, status=status.HTTP_400_BAD_REQUEST)
