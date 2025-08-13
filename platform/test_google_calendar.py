#!/usr/bin/env python
import os
import sys
import json
import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Path to the credentials file
BASE_DIR = "/usr/src/platform"
CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials", "google_calendar_credentials.json")

def test_google_calendar():
    """Test Google Calendar API integration."""
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        from googleapiclient.errors import HttpError
        
        logger.info("Google API libraries imported successfully")
        
        # Check if credentials file exists
        if not os.path.exists(CREDENTIALS_FILE):
            logger.error(f"Google Calendar credentials file not found at {CREDENTIALS_FILE}")
            return False
        
        logger.info(f"Credentials file found at {CREDENTIALS_FILE}")
        
        # Read the credentials file content
        with open(CREDENTIALS_FILE, "r") as f:
            creds_content = f.read()
            logger.info(f"Credentials file content length: {len(creds_content)}")
        
        # Load credentials
        try:
            credentials = service_account.Credentials.from_service_account_file(
                CREDENTIALS_FILE, scopes=["https://www.googleapis.com/auth/calendar"]
            )
            logger.info("Credentials loaded successfully")
        except Exception as e:
            logger.error(f"Error loading credentials: {str(e)}")
            return False
        
        # Build calendar service
        try:
            service = build("calendar", "v3", credentials=credentials)
            logger.info("Google Calendar service built successfully")
        except Exception as e:
            logger.error(f"Error building service: {str(e)}")
            return False
        
        # Test listing calendars
        try:
            calendars = service.calendarList().list().execute()
            logger.info(f"Calendars retrieved: {len(calendars.get('items', []))}")
            
            # Print calendar IDs
            for calendar in calendars.get('items', []):
                logger.info(f"Calendar: {calendar.get('summary')} (ID: {calendar.get('id')})")
            
            # If no calendars, use primary
            calendar_id = "primary"
            if calendars.get('items'):
                calendar_id = calendars.get('items')[0].get('id')
                
            logger.info(f"Using calendar ID: {calendar_id}")
        except Exception as e:
            logger.error(f"Error listing calendars: {str(e)}")
            # Still try to create an event using primary
            calendar_id = "primary"
        
        # Create a test event
        try:
            today = datetime.datetime.now()
            tomorrow = today + datetime.timedelta(days=1)
            
            start_time = tomorrow.replace(hour=10, minute=0, second=0).isoformat()
            end_time = tomorrow.replace(hour=11, minute=0, second=0).isoformat()
            
            event = {
                "summary": "Test Event",
                "location": "Test Location",
                "description": "Test Description",
                "start": {
                    "dateTime": start_time,
                    "timeZone": "America/Sao_Paulo",
                },
                "end": {
                    "dateTime": end_time,
                    "timeZone": "America/Sao_Paulo",
                }
            }
            
            created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
            logger.info(f"Event created with ID: {created_event.get('id')}")
            logger.info(f"Event link: {created_event.get('htmlLink')}")
            
            # Clean up by deleting the test event
            service.events().delete(calendarId=calendar_id, eventId=created_event.get('id')).execute()
            logger.info("Test event deleted successfully")
            
            return True
        except Exception as e:
            logger.error(f"Error creating/deleting event: {str(e)}")
            return False
    
    except ImportError as e:
        logger.error(f"Error importing Google libraries: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_google_calendar()
    if success:
        print("Google Calendar integration test PASSED")
        sys.exit(0)
    else:
        print("Google Calendar integration test FAILED")
        sys.exit(1)
