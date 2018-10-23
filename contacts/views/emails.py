from django.db import IntegrityError
from rest_framework import generics, status
from rest_framework.response import Response

from contacts.decorators import validate_flat_email_data
from contacts.models import EmailField, Contact
from contacts.serializers import EmailFieldSerializer


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
            if requested_contact.emails.count() > 1:
                requested_email = requested_contact.emails.get(email=kwargs['email'])
                requested_email.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

            return Response(data={'message': 'This email cannot be deleted'}, status=status.HTTP_400_BAD_REQUEST)
        except Contact.DoesNotExist:
            return Response(data={'message': 'The requested contact does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except EmailField.DoesNotExist:
            return Response(data={'message': 'The requested email does not exist'}, status=status.HTTP_404_NOT_FOUND)
