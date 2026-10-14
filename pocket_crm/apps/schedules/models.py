from django.db import models
from django.conf import settings
from apps.contacts.models import Contact

class Schedule(models.Model):
    MODE_CHOICES = [
        ('fixed', 'Fixed'),
        ('randomized', 'Randomized'),
        ('paused', 'Paused'),
    ]

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='schedules')
    mode = models.CharField(max_length=50, choices=MODE_CHOICES, default='fixed')
    interval_min = models.PositiveIntegerField(help_text="Minimum interval in days. Used for fixed mode.")
    interval_max = models.PositiveIntegerField(blank=True, null=True, help_text="Maximum interval in days. Used for randomized mode.")
    next_due_at = models.DateTimeField(blank=True, null=True, help_text="Calculated date for the next touchpoint")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_mode_display()} Schedule for {self.contact.name}"

class Touchpoint(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('snoozed', 'Snoozed'),
        ('skipped', 'Skipped'),
    ]

    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='touchpoints')
    due_at = models.DateTimeField(help_text="When this touchpoint is due")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Touchpoint for {self.schedule.contact.name} due {self.due_at.date()}"
