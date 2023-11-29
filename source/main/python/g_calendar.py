
import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GCalendar():
    def __init__(self, credentials: Credentials, calendar_id: str):
        self.gservice = build("calendar", "v3", credentials=credentials)
        self.calendar_id = calendar_id

    def delete_event(self, event_id):
        params = {"calendarId": self.calendar_id,
                  "eventId": event_id,
                  "sendNotifications": False,}

        try:
            # Call the Calendar API
            events_result = (self.gservice.events()
                             .delete(**params)
                             .execute())

        except HttpError as error:
            print(f"An error occurred: {error}")

    def write_event(self, body):
        params = {"calendarId": self.calendar_id,
                  "body": body}

        try:
            # Call the Calendar API
            events_result = (self.gservice.events()
                             .insert(**params)
                             .execute())

            events = events_result.get("htmlLink", [])

            if not events:
                raise ValueError("API didn't return the saved event with value {}".format(body))

        except Exception as error:
            print(f"An error occurred: {error}")

    def get_future_events_id(self):
        # other calendar
        # [{'kind': 'calendar#event',
        #   'etag': '"3402231187694000"',
        #   'id': '21ipsm2rqjiapkhhmnjuvqu857',
        #   'status': 'confirmed',
        #   'htmlLink': '<some_link>',
        #   'created': '2023-11-27T20:06:33.000Z',
        #   'updated': '2023-11-27T20:06:33.847Z',
        #   'creator': {'email': 'roberto@amutay.com'},
        #   'organizer': {'email': 'c_77c251614bb08a4acaa9b44137721ca7dccdbf83ec3414339e646fb4e14b4e7f@group.calendar.google.com',
        #   'displayName': 'Prueba calendar_ API',
        #   'self': True},
        #   'start': {'dateTime': '2023-11-27T21:00:00Z', 'timeZone': 'Europe/London'},
        #   'end': {'dateTime': '2023-11-27T22:00:00Z', 'timeZone': 'Europe/London'},
        #   'iCalUID': '21ipsm2rqjiapkhhmnjuvqu857@google.com',
        #   'sequence': 0,
        #   'reminders': {'useDefault': True},
        #   'eventType': 'default'}]
        #__________________________________________________________________
        # roberto calendar (is different because is recurrent?)
        # {'kind': 'calendar#event',
        #  'etag': '"3393042027362000"',
        #  'id': '03hjvgf10vckem1r8krk0ctoog_20240105T160000Z',
        #  'status': 'confirmed',
        #  'htmlLink': '<some_link',
        #  'created': '2019-07-08T16:47:34.000Z',
        #  'updated': '2023-10-05T15:50:13.681Z',
        #  'summary': 'Enviar facturas contador',
        #  'description': 'Enviar detalle de gastos y facturas al contador para declaración mensual.',
        #  'creator': {'email': '<some_email>'},
        #  'organizer': {'email': '<some_email>'},
        #  'start': {'dateTime': '2024-01-05T16:00:00Z',
        #  'timeZone': 'America/Guayaquil'},
        #  'end': {'dateTime': '2024-01-05T16:30:00Z',
        #  'timeZone': 'America/Guayaquil'},
        #  'recurringEventId': '03hjvgf10vckem1r8krk0ctoog',
        #  'originalStartTime': {'dateTime': '2024-01-05T16:00:00Z',
        #  'timeZone': 'America/Guayaquil'},
        #  'iCalUID': '03hjvgf10vckem1r8krk0ctoog@google.com',
        #  'sequence': 0,
        #  'attendees': [{'email': '<some_email', 'organizer': True, 'responseStatus': 'accepted'}, {...}],
        #  'guestsCanModify': True,
        #  'reminders': {'useDefault': True},
        #  'eventType': 'default'}

        list_events = []
        params = {"calendarId": self.calendar_id,
                  "timeMin": datetime.datetime.utcnow().isoformat() + "Z",
                  "singleEvents": True,
                  "orderBy": "startTime"}

        try:
            # Call the Calendar API
            events_result = (self.gservice.events()
                             .list(**params)
                             .execute())
            events = events_result.get("items", [])

            if not events:
                print("No upcoming events found.")

            for event in events:
                list_events.append(event['id'])

            return list_events

        except HttpError as error:
            print(f"An error occurred: {error}")
