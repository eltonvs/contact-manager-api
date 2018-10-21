from rest_framework import generics


class ListContactsView(generics.ListCreateAPIView):
    pass


class ContactDetailsView(generics.RetrieveUpdateDestroyAPIView):
    pass
