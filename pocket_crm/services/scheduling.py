from datetime import timedelta
from django.utils import timezone
import random
from apps.schedules.models import Schedule, Touchpoint

def calculate_next_due_date(schedule: Schedule, base_date=None) -> timezone.datetime:
    """Calculates the next due date for a schedule based on its mode."""
    if not base_date:
        base_date = timezone.now()
        
    if schedule.mode == 'fixed':
        return base_date + timedelta(days=schedule.interval_min)
    elif schedule.mode == 'randomized':
        interval_max = schedule.interval_max if schedule.interval_max else schedule.interval_min
        random_days = random.randint(schedule.interval_min, interval_max)
        return base_date + timedelta(days=random_days)
    
    return None

def generate_touchpoint_for_schedule(schedule: Schedule):
    """Generates the next active touchpoint for a schedule if one doesn't exist."""
    if schedule.mode == 'paused':
        return None
        
    # Prevent duplicate active touchpoints
    existing_active = Touchpoint.objects.filter(
        schedule=schedule, 
        status__in=['pending', 'snoozed']
    ).first()
    
    if existing_active:
        return existing_active

    next_due = calculate_next_due_date(schedule)
    if next_due:
        touchpoint = Touchpoint.objects.create(
            schedule=schedule,
            due_at=next_due,
            status='pending'
        )
        schedule.next_due_at = next_due
        schedule.save(update_fields=['next_due_at'])
        return touchpoint
        
    return None

def advance_schedule(schedule: Schedule):
    """Mark current touchpoints as completed (or archive them) and generate the next one."""
    generate_touchpoint_for_schedule(schedule)
