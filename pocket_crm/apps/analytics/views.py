from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.utils import timezone
from django.db.models import Count
from apps.contacts.models import Contact
from apps.interactions.models import Interaction
from apps.schedules.models import Touchpoint
from apps.messages.models import Message

class AnalyticsOverviewView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        now = timezone.now()

        # 1. Total active contacts (assuming all contacts are active for now)
        total_contacts = Contact.objects.filter(user=user).count()

        # 2. Upcoming touchpoints (status=pending, scheduled_for >= now)
        upcoming_touchpoints = Touchpoint.objects.filter(
            schedule__contact__user=user,
            status='pending',
            scheduled_for__gte=now
        ).count()

        # 3. Overdue touchpoints (status=pending, scheduled_for < now)
        overdue_touchpoints = Touchpoint.objects.filter(
            schedule__contact__user=user,
            status='pending',
            scheduled_for__lt=now
        ).count()

        # 4. Contacts contacted during a selected period (e.g., last 30 days)
        thirty_days_ago = now - timezone.timedelta(days=30)
        contacts_contacted_last_30_days = Interaction.objects.filter(
            contact__user=user,
            occurred_at__gte=thirty_days_ago
        ).values('contact').distinct().count()

        # 5. Recent interactions (count over last 30 days)
        recent_interactions = Interaction.objects.filter(
            contact__user=user,
            occurred_at__gte=thirty_days_ago
        ).count()

        # 6. Delivery status breakdown (last 30 days)
        delivery_status = Message.objects.filter(
            contact__user=user,
            created_at__gte=thirty_days_ago
        ).values('status').annotate(count=Count('status'))
        
        delivery_status_dict = {item['status']: item['count'] for item in delivery_status}

        return Response({
            "total_active_contacts": total_contacts,
            "upcoming_touchpoints": upcoming_touchpoints,
            "overdue_touchpoints": overdue_touchpoints,
            "contacts_contacted_last_30_days": contacts_contacted_last_30_days,
            "recent_interactions": recent_interactions,
            "delivery_status": delivery_status_dict
        })
