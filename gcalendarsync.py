from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

calendar_id = os.environ.get('calendar_id')
SCOPES = ['https://www.googleapis.com/auth/calendar']

def connect(): 
        creds = None        
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=8080)
            # Save the credentials for the next run
            with open("token.json", 'w') as token:
                token.write(creds.to_json())

        return build('calendar', 'v3', credentials=creds)

def create_event(service, event):    
    eventAdded = service.events().insert(calendarId=calendar_id, body=generate_json(event)).execute()
    print(f'added {event.name} {event.date} {event.eventId}')

def delete_event(service, event):
    if event.eventId is not None:
        service.events().delete(calendarId=calendar_id, eventId=event.eventId).execute()

def update_event(service, event):
    service.events().update(calendarId=calendar_id, eventId=event.eventId, body=generate_json(event)).execute()


def generate_json(event):
    event_to_add = {
    'id': event.eventId,
    'summary': f'{event.type} {event.subject}: {event.name} ',  
    'description': f'{event.type} de {event.subject}: {event.name} \n{event.comments}\nProgreso:{event.status}', 
    'start': {
        'date': event.date,        
    },
    'end': {
        'date': event.date,        
    },    
    'reminders': {
        'useDefault': False,
        'overrides': [        
        {'method': 'popup', 'minutes': 10080}, #1 week
        ],
    },
    }  
    return event_to_add

