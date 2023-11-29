
from utils import get_credential_obj
from g_sheet import GSheet
from g_calendar import GCalendar
from people_hr_events import PeopleHREvents

# Copy variables here

def get_peoplehr_events():
    ical_obj = PeopleHREvents(PEOPLE_HR_SKIM_URL, ICAL_FILE)
    _ = ical_obj.get_ical(False)
    body = ical_obj.parse_ical(dpbi_names)

    return body

def get_gsheet_events():
    creds = get_credential_obj(SERVICE_ACCOUNT_FILE, DOMAIN_WIDE_DELEGATION_SUBJECT, SHEET_SCOPES)
    sheet_obj = GSheet(creds, SHEET_ID, RANGE_NAME)
    body = sheet_obj.get_data_from_sheet()

    return body

def delete_all_future_calendar_events():
    creds = get_credential_obj(SERVICE_ACCOUNT_FILE, DOMAIN_WIDE_DELEGATION_SUBJECT, CALENDAR_SCOPES)
    calendar_obj = GCalendar(creds, CALENDAR_ID)
    events_id = calendar_obj.get_future_events_id()
    for event_id in events_id:
        calendar_obj.delete_event(event_id)

def append_all_future_calendar_events(list_body_events):
    creds = get_credential_obj(SERVICE_ACCOUNT_FILE, DOMAIN_WIDE_DELEGATION_SUBJECT, CALENDAR_SCOPES)
    calendar_obj = GCalendar(creds, CALENDAR_ID)
    for event_body in list_body_events:
        calendar_obj.write_event(event_body)

if __name__ == "__main__":
    delete_all_future_calendar_events()

    rota_events = get_gsheet_events()
    append_all_future_calendar_events(rota_events)

    holiday_events = get_peoplehr_events()
    append_all_future_calendar_events(holiday_events)
