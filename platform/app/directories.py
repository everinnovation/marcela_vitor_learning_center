import os

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Directory where credentials are stored
CREDENTIALS_DIR = os.path.join(BASE_DIR, 'credentials')

# Google Calendar credentials file
GOOGLE_CALENDAR_CREDENTIALS = os.path.join(CREDENTIALS_DIR, 'google_calendar_credentials.json')
