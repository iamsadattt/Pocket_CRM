from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from .models import Schedule, Touchpoint
from .serializers import ScheduleSerializer, TouchpointSerializer
from apps.contacts.models import Contact

class ScheduleListCreateView(generics.ListCreateAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        contact_id = self.kwargs.get('contact_id')
        contact = get_object_or_404(Contact, id=contact_id, user=self.request.user)
        return Schedule.objects.filter(contact=contact)

    def perform_create(self, serializer):
        contact_id = self.kwargs.get('contact_id')
        contact = get_object_or_404(Contact, id=contact_id, user=self.request.user)
        # We also need to trigger the generation of the first touchpoint
        schedule = serializer.save(contact=contact)
        from services.scheduling import generate_touchpoint_for_schedule
        generate_touchpoint_for_schedule(schedule)

class ScheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        contact_id = self.kwargs.get('contact_id')
        contact = get_object_or_404(Contact, id=contact_id, user=self.request.user)
        return Schedule.objects.filter(contact=contact)

    def perform_update(self, serializer):
        schedule = serializer.save()
        from services.scheduling import generate_touchpoint_for_schedule
        generate_touchpoint_for_schedule(schedule)

class UpcomingTouchpointListView(generics.ListAPIView):
    """View to see all upcoming touchpoints across all contacts for the user"""
    serializer_class = TouchpointSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Touchpoint.objects.filter(
            schedule__contact__user=self.request.user,
            status__in=['pending', 'snoozed']
        ).order_by('due_at')

class TouchpointDetailView(generics.RetrieveUpdateAPIView):
    """View to manage a specific touchpoint (e.g. mark it snoozed/skipped)"""
    serializer_class = TouchpointSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Touchpoint.objects.filter(schedule__contact__user=self.request.user)

    def perform_update(self, serializer):
        touchpoint = serializer.save()
        if touchpoint.status == 'completed':
            from services.scheduling import advance_schedule
            advance_schedule(touchpoint.schedule)
