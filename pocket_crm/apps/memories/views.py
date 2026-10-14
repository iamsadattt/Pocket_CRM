from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from .models import Memory
from .serializers import MemorySerializer
from apps.contacts.models import Contact

class MemoryListCreateView(generics.ListCreateAPIView):
    serializer_class = MemorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        contact_id = self.kwargs.get('contact_id')
        # Ensure the contact belongs to the user
        contact = get_object_or_404(Contact, id=contact_id, user=self.request.user)
        return Memory.objects.filter(contact=contact)

    def perform_create(self, serializer):
        contact_id = self.kwargs.get('contact_id')
        contact = get_object_or_404(Contact, id=contact_id, user=self.request.user)
        serializer.save(contact=contact)

class MemoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MemorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        contact_id = self.kwargs.get('contact_id')
        contact = get_object_or_404(Contact, id=contact_id, user=self.request.user)
        return Memory.objects.filter(contact=contact)
