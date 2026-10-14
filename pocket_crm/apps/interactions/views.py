from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from .models import Interaction
from .serializers import InteractionSerializer
from apps.contacts.models import Contact

class InteractionListCreateView(generics.ListCreateAPIView):
    serializer_class = InteractionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        contact_id = self.kwargs.get('contact_id')
        contact = get_object_or_404(Contact, id=contact_id, user=self.request.user)
        return Interaction.objects.filter(contact=contact)

    def perform_create(self, serializer):
        contact_id = self.kwargs.get('contact_id')
        contact = get_object_or_404(Contact, id=contact_id, user=self.request.user)
        serializer.save(contact=contact)

class InteractionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InteractionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        contact_id = self.kwargs.get('contact_id')
        contact = get_object_or_404(Contact, id=contact_id, user=self.request.user)
        return Interaction.objects.filter(contact=contact)
