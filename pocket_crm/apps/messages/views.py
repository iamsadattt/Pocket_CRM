from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Message
from .serializers import MessageSerializer, MessageGenerateSerializer
from apps.contacts.models import Contact
from services.message_generation import generate_message_draft

class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(contact__user=self.request.user)

    def perform_create(self, serializer):
        # Contact validation is handled by serializer but we can ensure ownership
        contact = serializer.validated_data.get('contact')
        if contact.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You do not own this contact.")
        serializer.save()

class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(contact__user=self.request.user)

class MessageGenerateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = MessageGenerateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        contact_id = data.get('contact_id')
        contact = get_object_or_404(Contact, id=contact_id, user=request.user)

        try:
            draft_text = generate_message_draft(
                contact=contact,
                purpose=data.get('purpose'),
                tone=data.get('tone'),
                length=data.get('length'),
                custom_instruction=data.get('custom_instruction')
            )
            
            # Save the draft
            message = Message.objects.create(
                contact=contact,
                body=draft_text,
                status='draft',
                purpose=data.get('purpose'),
                tone=data.get('tone'),
                length=data.get('length')
            )
            
            return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MessageSendView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        message = get_object_or_404(Message, pk=pk, contact__user=request.user)

        if message.status != 'approved':
            return Response(
                {"error": "Message must be approved before sending."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # In a real app, this would queue a Celery task to send via Twilio/SendGrid.
        # For MVP, we simulate a manual handoff / instant mock delivery.
        from .models import DeliveryAttempt
        attempt = DeliveryAttempt.objects.create(
            message=message,
            provider='manual_handoff',
            status='success'
        )

        message.status = 'delivered'
        message.save(update_fields=['status'])

        # If linked to a touchpoint, mark it completed to advance the schedule
        if message.touchpoint and message.touchpoint.status != 'completed':
            message.touchpoint.status = 'completed'
            message.touchpoint.save(update_fields=['status'])
            
            from services.scheduling import advance_schedule
            advance_schedule(message.touchpoint.schedule)

        return Response({"status": "Message handed off/delivered successfully."})
