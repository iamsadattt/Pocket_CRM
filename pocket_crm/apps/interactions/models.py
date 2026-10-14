from django.db import models
from django.conf import settings
from apps.contacts.models import Contact

class Interaction(models.Model):
    CHANNEL_CHOICES = [
        ('phone', 'Phone Call'),
        ('message', 'Text/Message'),
        ('in_person', 'In-person Meeting'),
        ('video', 'Video Call'),
        ('special', 'Special Occasion'),
        ('custom', 'Custom Interaction'),
    ]

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='interactions')
    channel = models.CharField(max_length=50, choices=CHANNEL_CHOICES, default='custom')
    occurred_at = models.DateTimeField(help_text="When the interaction took place")
    summary = models.TextField(blank=True, null=True, help_text="Notes or summary of the interaction")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-occurred_at']

    def __str__(self):
        return f"{self.get_channel_display()} with {self.contact.name} on {self.occurred_at.date()}"
