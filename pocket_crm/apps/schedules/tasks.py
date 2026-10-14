from celery import shared_task
from apps.schedules.models import Schedule
from services.scheduling import generate_touchpoint_for_schedule
import logging

logger = logging.getLogger(__name__)

@shared_task
def process_schedules_and_generate_touchpoints():
    """
    Periodic task to check for active schedules that are missing touchpoints
    or whose touchpoints are past due (for auto-escalation or regeneration).
    """
    logger.info("Starting touchpoint generation for active schedules...")
    # Find all schedules that are NOT paused
    active_schedules = Schedule.objects.exclude(mode='paused')
    
    generated_count = 0
    for schedule in active_schedules:
        # generate_touchpoint_for_schedule handles duplicate prevention
        touchpoint = generate_touchpoint_for_schedule(schedule)
        if touchpoint:
            generated_count += 1
            
    logger.info(f"Generated {generated_count} new touchpoints.")
    return generated_count
