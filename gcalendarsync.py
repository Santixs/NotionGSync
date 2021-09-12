from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import datetime

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
    try:
        eventAdded = service.events().insert(calendarId=calendar_id, body=generate_json(event)).execute()
        print(f'added {event.name} {event.date} {event.eventId}')
    except Exception as e:
        save_error("creating", event.name, e)

def delete_event(service, event):
    if event.eventId is not None:
        try:        service.events().delete(calendarId=calendar_id, eventId=event.eventId).execute()
        except Exception as e:      save_error("deleting", event.name, e)


def update_event(service, event):
        try:    service.events().update(calendarId=calendar_id, eventId=event.eventId, body=generate_json(event)).execute()
        except Exception as e:   save_error("updating", event.name, e)



def generate_json(event):
    if event.status == 'Urgente': event.icon = "⭐"

    if event.type=="Exam": color = 11
    elif event.type == "Assignment" and (event.progress == 100 or event.status == 'Completado'): color = 4; event.icon = "✔️"
    else: color = 6    

    #We have to differentiate between the yyy-mm-dd format and the RFC3339 format
    if len(event.date)>11:date = datetype = "dateTime"
    else: datetype = "date"


    event_to_add = {
    'id': event.eventId,
    'colorId':color,
    'summary': f'{event.icon} {event.type[:1]}. {event.subject} {event.name} ',  
    'description': f'{event.type}. of {event.subject}: {event.name} \n{event.comments} \n {f"Progreso: {str(event.progress)}" if event.progress >=0 else ""} Status: {event.status}', 
    'start': {
        datetype : event.date,        
    },
    'end': {
        datetype : event.endDate,        
    },    
    'reminders': {
        'useDefault': False,
        'overrides': [        
        {'method': 'popup', 'minutes': 10080}, #1 week
        ],
    },
    }  
    return event_to_add

def save_error(type, name, msg = ""):
    text = f"{datetime.datetime.now()} --> Error while {type} the following event: {name} \n"
    file_object = open('errors.log', 'a')
    file_object.write(text)
    print (f"{text}  \n  {msg}")
    file_object.close()