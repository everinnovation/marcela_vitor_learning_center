#!/usr/bin/env python
import os
import sys
import django
import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

# Import Django models and utilities after setting up Django
from website.models.schedule import VisitSchedule
from website.views.email_management import EmailManager

def test_schedule_email():
    """Test sending a schedule confirmation email."""
    try:
        # Create a test schedule object
        test_schedule = VisitSchedule(
            full_name="Test Visitor",
            email="test@example.com",  # Replace with a real email for testing
            phone="555-123-4567",
            visit_date=datetime.date.today() + datetime.timedelta(days=3),  # 3 days from now
            time_slot="10:00",
            number_of_children=2,
            children_ages="3, 5",
            special_requests="This is a test request"
        )
        
        logger.info(f"Created test schedule for {test_schedule.full_name} on {test_schedule.visit_date}")
        
        # Send the confirmation email
        try:
            email_sent = EmailManager.send_schedule_confirmation_email(test_schedule)
            
            if email_sent:
                logger.info("✅ Test schedule email sent successfully!")
                return True
            else:
                logger.error("❌ Failed to send test schedule email")
                return False
                
        except Exception as e:
            logger.error(f"❌ Exception when sending email: {str(e)}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_schedule_email()
    if success:
        print("Schedule email test PASSED")
        sys.exit(0)
    else:
        print("Schedule email test FAILED")
        sys.exit(1)
