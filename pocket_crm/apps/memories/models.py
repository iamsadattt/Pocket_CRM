from django.db import models
from django.conf import settings
from apps.contacts.models import Contact

class Memory(models.Model):
    CATEGORY_CHOICES = [
        ('interest', 'Interest & Preferences'),
        ('event', 'Life Event'),
        ('experience', 'Shared Experience'),
        ('topic', 'Discussion Topic'),
        ('milestone', 'Upcoming Milestone'),
        ('preference', 'Communication Preference'),
        ('other', 'Other'),
    ]

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='memories')
    content = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    include_in_drafts = models.BooleanField(default=True, help_text="Allow this memory to be used when AI generates message drafts.")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Memories'
        ordering = ['-created_at']

    def __str__(self):
        return f"Memory for {self.contact.name}: {self.content[:30]}..."
