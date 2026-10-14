from django.db import models
from django.conf import settings

class Tag(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=50)

    class Meta:
        unique_together = ('user', 'name')

    def __str__(self):
        return self.name

class Contact(models.Model):
    RELATIONSHIP_CHOICES = [
        ('friend', 'Friend'),
        ('family', 'Family'),
        ('colleague', 'Colleague'),
        ('mentor', 'Mentor'),
        ('mentee', 'Mentee'),
        ('acquaintance', 'Acquaintance'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('archived', 'Archived'),
    ]

    CHANNEL_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('whatsapp', 'WhatsApp'),
        ('telegram', 'Telegram'),
        ('in_person', 'In Person'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    whatsapp = models.CharField(max_length=50, blank=True, null=True)
    telegram = models.CharField(max_length=50, blank=True, null=True)
    
    relationship = models.CharField(max_length=50, choices=RELATIONSHIP_CHOICES)
    birthday = models.DateField(blank=True, null=True)
    timezone = models.CharField(max_length=50, blank=True, null=True)
    preferred_channel = models.CharField(max_length=50, choices=CHANNEL_CHOICES, blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='active')
    
    tags = models.ManyToManyField(Tag, related_name='contacts', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_contacted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name
