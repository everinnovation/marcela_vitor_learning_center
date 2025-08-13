#!/usr/bin/env python
import os
import sys
import datetime
import logging

# Set up Django environment first
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

# Now import Django models and utils
from website.models.schedule import VisitSchedule
from website.utils.google_calendar import GoogleCalendarService

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_schedule_creation():
    """Test creating a schedule and adding it to Google Calendar."""
    try:
        # Create a test schedule
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        
        schedule = VisitSchedule(
            full_name="Test User",
            email="test@example.com",
            phone="555-1234",
            visit_date=tomorrow,
            time_slot="10:00",
            number_of_children=2,
            children_ages="4, 6",
            special_requests="This is a test visit",
            status="scheduled"
        )
        
        # Don't save to database yet
        logger.info(f"Created test schedule for {schedule.full_name} on {schedule.visit_date} at {schedule.time_slot}")
        
        # Create Google Calendar event
        calendar_service = GoogleCalendarService()
        event_id = calendar_service.create_event(schedule)
        
        if event_id:
            logger.info(f"Google Calendar event created with ID: {event_id}")
            
            # Update the schedule with the event ID
            schedule.google_calendar_event_id = event_id
            
            # Now clean up
            delete_result = calendar_service.delete_event(event_id)
            logger.info(f"Test event deleted: {delete_result}")
            
            return True
        else:
            logger.error("Failed to create Google Calendar event")
            return False
    
    except Exception as e:
        logger.error(f"Error testing schedule creation: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_schedule_creation()
    if success:
        print("Schedule creation and Google Calendar integration test PASSED")
        sys.exit(0)
    else:
        print("Schedule creation and Google Calendar integration test FAILED")
        sys.exit(1)
