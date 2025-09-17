# filepath: /Users/everinnovation/Documents/CODE/LEARNING CENTER/marcela_vitor_learning_center/platform/website/utils/google_calendar.py
import os
import datetime
import logging
import sys
import traceback
import json

# Set up logging
logger = logging.getLogger(__name__)

# Path to the credentials file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Removed reference to credentials file as we'll use environment variables

class GoogleCalendarService:
    """Service class for interacting with Google Calendar API."""
    
    def __init__(self):
        """Initialize the Google Calendar service."""
        self.service = None
        self.initialized = False
        
        # Set the specific calendar ID for Marcela Vitor's calendar
        self.calendar_id = 'contactmarcelavitor@gmail.com'
        self.calendar_url = 'https://calendar.google.com/calendar/embed?src=contactmarcelavitor%40gmail.com&ctz=America%2FSao_Paulo'
        self.calendar_ical = 'https://calendar.google.com/calendar/ical/contactmarcelavitor%40gmail.com/public/basic.ics'
        
        try:
            from google.oauth2 import service_account
            from googleapiclient.discovery import build
            
            logger.info("Successfully imported Google API libraries")
            
            # Check if environment variables are set
            required_vars = [
                'GOOGLE_CALENDAR_TYPE',
                'GOOGLE_CALENDAR_PROJECT_ID',
                'GOOGLE_CALENDAR_PRIVATE_KEY_ID',
                'GOOGLE_CALENDAR_PRIVATE_KEY',
                'GOOGLE_CALENDAR_CLIENT_EMAIL',
                'GOOGLE_CALENDAR_CLIENT_ID',
                'GOOGLE_CALENDAR_AUTH_URI',
                'GOOGLE_CALENDAR_TOKEN_URI',
                'GOOGLE_CALENDAR_AUTH_PROVIDER_CERT_URL',
                'GOOGLE_CALENDAR_CLIENT_CERT_URL',
                'GOOGLE_CALENDAR_UNIVERSE_DOMAIN'
            ]
            
            missing_vars = [var for var in required_vars if not os.getenv(var)]
            if missing_vars:
                logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
                return
            
            logger.info("Found all required environment variables for Google Calendar API")
            
            # For service accounts, we need to specify the calendar ID explicitly
            # Using the specific calendar ID for Marcela Vitor's calendar
            self.calendar_id = 'contactmarcelavitor@gmail.com'
            self.calendar_url = 'https://calendar.google.com/calendar/embed?src=contactmarcelavitor%40gmail.com&ctz=America%2FSao_Paulo'
            self.calendar_ical = 'https://calendar.google.com/calendar/ical/contactmarcelavitor%40gmail.com/public/basic.ics'
            
            logger.info(f"Using calendar ID: {self.calendar_id}")
            
            # Scopes required for calendar access
            scopes = ['https://www.googleapis.com/auth/calendar']
            
            # Load credentials and build service
            try:
                logger.info("Creating credentials from environment variables")
                
                # Create credentials info dictionary from environment variables
                credentials_info = {
                    "type": os.getenv("GOOGLE_CALENDAR_TYPE"),
                    "project_id": os.getenv("GOOGLE_CALENDAR_PROJECT_ID"),
                    "private_key_id": os.getenv("GOOGLE_CALENDAR_PRIVATE_KEY_ID"),
                    "private_key": os.getenv("GOOGLE_CALENDAR_PRIVATE_KEY").replace('\\n', '\n'),
                    "client_email": os.getenv("GOOGLE_CALENDAR_CLIENT_EMAIL"),
                    "client_id": os.getenv("GOOGLE_CALENDAR_CLIENT_ID"),
                    "auth_uri": os.getenv("GOOGLE_CALENDAR_AUTH_URI"),
                    "token_uri": os.getenv("GOOGLE_CALENDAR_TOKEN_URI"),
                    "auth_provider_x509_cert_url": os.getenv("GOOGLE_CALENDAR_AUTH_PROVIDER_CERT_URL"),
                    "client_x509_cert_url": os.getenv("GOOGLE_CALENDAR_CLIENT_CERT_URL"),
                    "universe_domain": os.getenv("GOOGLE_CALENDAR_UNIVERSE_DOMAIN")
                }
                
                # Create credentials from dictionary instead of file
                credentials = service_account.Credentials.from_service_account_info(
                    credentials_info, scopes=scopes
                )
                logger.info("Successfully created credentials from environment variables")
                
                logger.info("Building Google Calendar service")
                self.service = build('calendar', 'v3', credentials=credentials)
                
                # Verify calendar access
                if self.verify_calendar_access():
                    self.initialized = True
                    logger.info("Google Calendar service initialized successfully with verified access")
                else:
                    logger.error("Google Calendar service could not verify calendar access")
                    self.initialized = False
            except Exception as e:
                logger.error(f"Error initializing Google Calendar service: {str(e)}")
                logger.error(traceback.format_exc())
                self.initialized = False
        
        except ImportError as e:
            logger.error(f"Google API libraries not available: {str(e)}")
            logger.error(f"Python path: {sys.path}")
            self.initialized = False
    
    def is_initialized(self):
        """Check if the Google Calendar service is properly initialized."""
        return self.initialized and self.service is not None
    
    def verify_calendar_access(self):
        """Verify that we have access to the calendar and can create events."""
        if not self.service:
            logger.error("Google Calendar service not initialized. Cannot verify access.")
            return False
        
        try:
            # First, try to access the specific calendar provided
            try:
                logger.info(f"Attempting to access calendar with ID: {self.calendar_id}")
                calendar = self.service.calendars().get(calendarId=self.calendar_id).execute()
                logger.info(f"Successfully accessed calendar: {calendar['summary']} ({self.calendar_id})")
                
                # Try to create a test event in the calendar
                try:
                    # Create a simple test event
                    now = datetime.datetime.utcnow()
                    event = {
                        'summary': 'Test Event (Will be deleted)',
                        'start': {
                            'dateTime': now.isoformat() + 'Z',
                            'timeZone': 'America/Sao_Paulo',
                        },
                        'end': {
                            'dateTime': (now + datetime.timedelta(hours=1)).isoformat() + 'Z',
                            'timeZone': 'America/Sao_Paulo',
                        },
                    }
                    
                    test_event = self.service.events().insert(calendarId=self.calendar_id, body=event).execute()
                    logger.info(f"Test event created in {self.calendar_id} with ID {test_event['id']}")
                    
                    # Delete the test event
                    self.service.events().delete(calendarId=self.calendar_id, eventId=test_event['id']).execute()
                    logger.info(f"Test event deleted from {self.calendar_id}")
                    
                    return True
                except Exception as e:
                    logger.warning(f"Cannot create events in calendar {self.calendar_id}: {str(e)}")
            except Exception as e:
                logger.warning(f"Cannot access calendar {self.calendar_id}: {str(e)}")
            
            # If the direct access failed, try listing and finding calendars
            logger.info("Listing available calendars")
            calendar_list = self.service.calendarList().list().execute()
            calendars = calendar_list.get('items', [])
            
            if not calendars:
                logger.warning("No calendars found - the service account may not have access to any calendars")
                
                # Try to create a calendar for the service account
                logger.info("Attempting to create a new calendar for the service account")
                calendar = {
                    'summary': 'Marcela Vitor Daycare Visits',
                    'timeZone': 'America/Sao_Paulo'
                }
                
                created_calendar = self.service.calendars().insert(body=calendar).execute()
                logger.info(f"Created new calendar: {created_calendar['id']}")
                
                # Use this calendar
                self.calendar_id = created_calendar['id']
                return True
            
            # If we have calendars, log them and verify we can access them
            logger.info(f"Found {len(calendars)} calendars")
            for calendar in calendars:
                logger.info(f"Calendar: {calendar['summary']} ({calendar['id']})")
                
                # Try to create a test event in each calendar
                try:
                    # Create a simple test event
                    now = datetime.datetime.utcnow()
                    event = {
                        'summary': 'Test Event (Will be deleted)',
                        'start': {
                            'dateTime': now.isoformat() + 'Z',
                            'timeZone': 'America/Sao_Paulo',
                        },
                        'end': {
                            'dateTime': (now + datetime.timedelta(hours=1)).isoformat() + 'Z',
                            'timeZone': 'America/Sao_Paulo',
                        },
                    }
                    
                    # Try to insert the event
                    calendar_id = calendar['id']
                    logger.info(f"Testing event creation in calendar {calendar_id}")
                    test_event = self.service.events().insert(calendarId=calendar_id, body=event).execute()
                    
                    # If successful, delete the test event
                    logger.info(f"Test event created in {calendar_id} with ID {test_event['id']}")
                    self.service.events().delete(calendarId=calendar_id, eventId=test_event['id']).execute()
                    logger.info(f"Test event deleted from {calendar_id}")
                    
                    # Use this calendar as it works
                    self.calendar_id = calendar_id
                    logger.info(f"Using calendar {calendar_id} for events")
                    return True
                    
                except Exception as e:
                    logger.warning(f"Cannot create events in calendar {calendar['id']}: {str(e)}")
            
            # If we get here, we couldn't find a calendar we can write to
            logger.error("Could not find any calendars with write access")
            
            # Try creating our own calendar as a last resort
            try:
                logger.info("Attempting to create a new calendar as no writable calendars were found")
                calendar = {
                    'summary': 'Marcela Vitor Daycare Visits',
                    'timeZone': 'America/Sao_Paulo'
                }
                
                created_calendar = self.service.calendars().insert(body=calendar).execute()
                logger.info(f"Created new calendar: {created_calendar['id']}")
                
                # Use this calendar
                self.calendar_id = created_calendar['id']
                return True
            except Exception as create_e:
                logger.error(f"Failed to create a new calendar: {str(create_e)}")
                return False
            
        except Exception as e:
            logger.error(f"Error verifying calendar access: {str(e)}")
            logger.error(traceback.format_exc())
            return False
    
    def create_event(self, visit_schedule):
        """Create a calendar event for a visit schedule."""
        if not self.is_initialized():
            logger.error("Google Calendar service not initialized. Cannot create event.")
            return None
        
        try:
            # Format the visit time - check the format first
            logger.info(f"Visit date: {visit_schedule.visit_date}, type: {type(visit_schedule.visit_date)}")
            logger.info(f"Time slot: {visit_schedule.time_slot}, type: {type(visit_schedule.time_slot)}")
            
            # Format the visit time
            start_time = f"{visit_schedule.visit_date.isoformat()}T{visit_schedule.time_slot}:00"
            
            # Visits last 1 hour
            hour, minute = visit_schedule.time_slot.split(':')
            end_hour = int(hour) + 1
            end_time = f"{visit_schedule.visit_date.isoformat()}T{end_hour}:{minute}:00"
            
            logger.info(f"Creating event for {visit_schedule.full_name} on {visit_schedule.visit_date} at {visit_schedule.time_slot}")
            logger.info(f"Start time: {start_time}, End time: {end_time}")
            logger.info(f"Using calendar ID: {self.calendar_id}")
            
            # Create event details
            event = {
                'summary': f'Daycare Visit - {visit_schedule.full_name}',
                'location': 'Marcela Vitor Learning Center',
                'description': (
                    f"Visit scheduled for {visit_schedule.full_name}\n"
                    f"Phone: {visit_schedule.phone}\n"
                    f"Email: {visit_schedule.email}\n"
                    f"Number of children: {visit_schedule.number_of_children}\n"
                    f"Children ages: {visit_schedule.children_ages}\n"
                    f"Special requests: {visit_schedule.special_requests or 'None'}"
                ),
                'start': {
                    'dateTime': start_time,
                    'timeZone': 'America/Sao_Paulo',
                },
                'end': {
                    'dateTime': end_time,
                    'timeZone': 'America/Sao_Paulo',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},  # 1 day before
                        {'method': 'popup', 'minutes': 60},  # 1 hour before
                    ],
                },
            }
            
            # Create the event
            logger.info(f"Sending request to Google Calendar API to create event")
            try:
                # Log the full event details for debugging
                import json
                logger.info(f"Event details: {json.dumps(event, default=str)}")
                
                # Try to get the calendar to verify access
                try:
                    calendar = self.service.calendars().get(calendarId=self.calendar_id).execute()
                    logger.info(f"Successfully accessed calendar: {calendar['summary']} ({self.calendar_id})")
                except Exception as cal_error:
                    logger.error(f"Error accessing calendar {self.calendar_id}: {str(cal_error)}")
                    
                    # Try with contactmarcelavitor@gmail.com
                    try:
                        # Use the Marcela Vitor calendar ID
                        marcela_id = 'contactmarcelavitor@gmail.com'
                        logger.info(f"Trying with Marcela Vitor's calendar ID: {marcela_id}")
                        calendar = self.service.calendars().get(calendarId=marcela_id).execute()
                        logger.info(f"Successfully accessed calendar: {calendar['summary']} ({marcela_id})")
                        self.calendar_id = marcela_id
                    except Exception as alt_error:
                        logger.error(f"Error accessing Marcela's calendar: {str(alt_error)}")
                        
                        # Try with primary
                        try:
                            test_id = 'primary'
                            logger.info(f"Trying with alternate calendar ID: {test_id}")
                            calendar = self.service.calendars().get(calendarId=test_id).execute()
                            logger.info(f"Successfully accessed calendar: {calendar['summary']} ({test_id})")
                            self.calendar_id = test_id
                        except Exception as alt2_error:
                            logger.error(f"Error accessing primary calendar: {str(alt2_error)}")
                            
                            # Try to create a new calendar
                            try:
                                logger.info("Creating a new calendar")
                                calendar = {
                                    'summary': 'Marcela Vitor Daycare Visits',
                                    'timeZone': 'America/Sao_Paulo'
                                }
                                created_calendar = self.service.calendars().insert(body=calendar).execute()
                                self.calendar_id = created_calendar['id']
                                logger.info(f"Created new calendar with ID: {self.calendar_id}")
                            except Exception as create_error:
                                logger.error(f"Error creating new calendar: {str(create_error)}")
                                return None
                
                # Create the event in the calendar
                logger.info(f"Creating event in calendar {self.calendar_id}")
                created_event = self.service.events().insert(calendarId=self.calendar_id, body=event).execute()
                
                if created_event:
                    logger.info(f"Created event response: {json.dumps(created_event, default=str)}")
                    
                    event_id = created_event.get('id')
                    event_link = created_event.get('htmlLink')
                    
                    if not event_id:
                        logger.error(f"No event ID in response: {created_event}")
                        return None
                    
                    logger.info(f"Event created: ID={event_id}, Link={event_link}")
                    return event_id
                else:
                    logger.error("No response from Google Calendar API")
                    return None
            except Exception as api_error:
                logger.error(f"API error creating Google Calendar event: {str(api_error)}")
                # Log detailed information about the API error
                logger.error(f"Error type: {type(api_error).__name__}")
                if hasattr(api_error, 'content'):
                    logger.error(f"Error content: {api_error.content}")
                
                logger.error(traceback.format_exc())
                return None
        
        except Exception as e:
            logger.error(f"Error creating Google Calendar event: {str(e)}")
            logger.error(traceback.format_exc())
            return None
    
    def update_event(self, event_id, visit_schedule):
        """Update an existing calendar event."""
        if not self.initialized or not self.service:
            logger.error("Google Calendar service not initialized. Cannot update event.")
            return False
        
        try:
            # Get the existing event
            event = self.service.events().get(calendarId=self.calendar_id, eventId=event_id).execute()
            
            # Format the visit time
            start_time = f"{visit_schedule.visit_date.isoformat()}T{visit_schedule.time_slot}:00"
            
            # Visits last 1 hour
            hour, minute = visit_schedule.time_slot.split(':')
            end_hour = int(hour) + 1
            end_time = f"{visit_schedule.visit_date.isoformat()}T{end_hour}:{minute}:00"
            
            # Update event details
            event['summary'] = f'Daycare Visit - {visit_schedule.full_name}'
            event['description'] = (
                f"Visit scheduled for {visit_schedule.full_name}\n"
                f"Phone: {visit_schedule.phone}\n"
                f"Email: {visit_schedule.email}\n"
                f"Number of children: {visit_schedule.number_of_children}\n"
                f"Children ages: {visit_schedule.children_ages}\n"
                f"Special requests: {visit_schedule.special_requests or 'None'}"
            )
            event['start'] = {
                'dateTime': start_time,
                'timeZone': 'America/Sao_Paulo',
            }
            event['end'] = {
                'dateTime': end_time,
                'timeZone': 'America/Sao_Paulo',
            }
            
            # Update the event
            updated_event = self.service.events().update(
                calendarId=self.calendar_id, eventId=event_id, body=event
            ).execute()
            
            logger.info(f"Event updated: {updated_event.get('htmlLink')}")
            return True
        
        except Exception as e:
            logger.error(f"Error updating Google Calendar event: {str(e)}")
            return False
    
    def delete_event(self, event_id):
        """Delete a calendar event."""
        if not self.initialized or not self.service:
            logger.error("Google Calendar service not initialized. Cannot delete event.")
            return False
        
        try:
            self.service.events().delete(calendarId=self.calendar_id, eventId=event_id).execute()
            logger.info(f"Event deleted: {event_id}")
            return True
        
        except Exception as e:
            logger.error(f"Error deleting Google Calendar event: {str(e)}")
            return False
    
    def get_available_slots(self, date_str):
        """Get available time slots for a specific date."""
        # All possible time slots
        all_slots = ['09:00', '10:00', '11:00', '14:00', '15:00', '16:00']
        
        if not self.initialized or not self.service:
            logger.error("Google Calendar service not initialized. Cannot get available slots.")
            # Return all slots if we can't check availability
            return all_slots
        
        try:
            # Get the beginning and end of the selected date
            date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            start_datetime = datetime.datetime.combine(date_obj, datetime.time.min).isoformat() + 'Z'
            end_datetime = datetime.datetime.combine(date_obj, datetime.time.max).isoformat() + 'Z'
            
            # Get events for that day
            events_result = self.service.events().list(
                calendarId=self.calendar_id,
                timeMin=start_datetime,
                timeMax=end_datetime,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            logger.info(f"Found {len(events)} events for date {date_str}")
            
            # Find booked slots
            booked_slots = []
            for event in events:
                start = event['start'].get('dateTime')
                if start:
                    # Extract the hour:minute from the dateTime string
                    time_part = start.split('T')[1][:5]  # Format HH:MM
                    booked_slots.append(time_part)
            
            # Return available slots (all slots minus booked slots)
            available_slots = [slot for slot in all_slots if slot not in booked_slots]
            logger.info(f"Available slots for {date_str}: {available_slots}")
            return available_slots
        
        except Exception as e:
            logger.error(f"Error getting available slots from Google Calendar: {str(e)}")
            return all_slots  # Return all slots if we can't check availability
