#!/usr/bin/env python
import os
import sys
import json
import datetime
import logging
import requests

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def simulate_form_submission():
    """Simulate submitting the schedule form through the web interface."""
    try:
        # Use the local Django development server
        base_url = "http://localhost:8000"
        schedule_url = f"{base_url}/schedule/"
        
        # Tomorrow's date
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        tomorrow_str = tomorrow.strftime("%Y-%m-%d")
        
        # Form data
        form_data = {
            "full_name": "Test Web User",
            "email": "test-web@example.com",
            "phone": "555-5678",
            "visit_date": tomorrow_str,
            "time_slot": "11:00",
            "number_of_children": "2",
            "children_ages": "3, 5",
            "special_requests": "This is a test web submission",
            "csrfmiddlewaretoken": "dummy-token"  # This will be ignored in our test
        }
        
        # First, get a CSRF token
        session = requests.Session()
        response = session.get(schedule_url)
        logger.info(f"Initial GET request status: {response.status_code}")
        
        # Now submit the form
        response = session.post(schedule_url, data=form_data, allow_redirects=True)
        logger.info(f"Form submission status: {response.status_code}")
        
        # Check if the submission was successful
        if response.status_code == 200 or response.status_code == 302:
            if "Your visit has been scheduled successfully" in response.text:
                logger.info("Visit scheduled successfully")
                return True
            elif "there was an issue with the calendar integration" in response.text:
                logger.warning("Visit scheduled but calendar integration failed")
                return False
            else:
                logger.error("Form submission response doesn't indicate success")
                return False
        else:
            logger.error(f"Form submission failed with status code {response.status_code}")
            return False
    
    except Exception as e:
        logger.error(f"Error simulating form submission: {str(e)}")
        return False

if __name__ == "__main__":
    success = simulate_form_submission()
    if success:
        print("Web form submission test PASSED")
        sys.exit(0)
    else:
        print("Web form submission test FAILED")
        sys.exit(1)
