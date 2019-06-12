from datetime import timedelta
import datetime

import httplib2
import pytz
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

service_account_email = 'gcalendar@ultimate-ascent-241315.iam.gserviceaccount.com'

CLIENT_SECRET_FILE = 'gcalendar/gcal.json'

SCOPES = 'https://www.googleapis.com/auth/calendar'
scopes = [SCOPES]


def build_service():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(filename=CLIENT_SECRET_FILE, scopes=SCOPES)

    http = credentials.authorize(httplib2.Http())

    service = build('calendar', 'v3', http=http, cache_discovery=False)

    return service


def execute_event(validated_data):
    service = build_service()

    event = service.events().insert(calendarId='hannabretsko@gmail.com', body={
        'summary': validated_data.get('meal_name'),
        'description': validated_data.get('detail'),
        'start': {'dateTime': validated_data.get('start_date')},
        'end': {'dateTime': validated_data.get('end_date')},
    }).execute()

    return event


def create_event_test():
    service = build_service()

    start_datetime = datetime.datetime.now(pytz.timezone("Australia/Melbourne"))
    event = service.events().insert(calendarId='hannabretsko@gmail.com', body={
        'summary': 'Test',
        'description': 'Test',
        'start': {'dateTime': start_datetime.isoformat()},
        'end': {'dateTime': (start_datetime + timedelta(minutes=15)).isoformat()},
    }).execute()

    print(event)


# create_event_test()
