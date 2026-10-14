from django.db import models
from django.conf import settings
from apps.contacts.models import Contact
from apps.schedules.models import Touchpoint

class Message(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('queued', 'Queued'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='messages')
    touchpoint = models.ForeignKey(Touchpoint, on_delete=models.SET_NULL, blank=True, null=True, related_name='messages')
    
    body = models.TextField(help_text="The actual content of the message")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='draft')
    
    # Context used for generation (optional tracking)
    purpose = models.CharField(max_length=100, blank=True, null=True)
    tone = models.CharField(max_length=50, blank=True, null=True)
    length = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_status_display()} message for {self.contact.name}"

class DeliveryAttempt(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='delivery_attempts')
    provider = models.CharField(max_length=50, help_text="e.g., manual_handoff, email, whatsapp_api")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.provider} attempt for Message {self.message.id}: {self.get_status_display()}"
