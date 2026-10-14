from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Interaction
from apps.contacts.models import Contact

@receiver(post_save, sender=Interaction)
def update_contact_last_contacted_at(sender, instance, **kwargs):
    contact = instance.contact
    # Get the most recent interaction date for this contact
    latest_interaction = contact.interactions.order_by('-occurred_at').first()
    
    if latest_interaction:
        contact.last_contacted_at = latest_interaction.occurred_at
        contact.save(update_fields=['last_contacted_at'])
