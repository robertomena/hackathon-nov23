

import datetime
import os.path

from google.oauth2.credentials import Credentials
from google.oauth2 import service_account

def get_credential_obj(sa_filepath: str, delegation_subject: str, scopes: str) -> Credentials:
    creds = None
    try:
        if os.path.exists(sa_filepath):
            creds = service_account.Credentials.from_service_account_file(
            sa_filepath, scopes=scopes).with_subject(delegation_subject)

            # print(creds.expired, creds.scopes, creds.signer_email)
        else:
            print("No service account key found")

    except e:
        print("Error while authenticating to google: {}".format(e))
    finally:
        return creds

def parse_to_write(summary: str, start_dt: datetime, end_dt: datetime, all_day=False) -> dict:
    def parse_time(dt_obj, all_day):
        if not all_day:
            return {
                'dateTime': dt_obj.isoformat(),
                'timeZone': 'Europe/London',
            }
        else:
            return {
                'date': dt_obj.strftime("%Y-%m-%d"),
            }

    body = {
        'summary': summary,
        'description': '',
        'location': '',
        'reminders': {
            'useDefault': True,
        },
        'attendees': [],
        'start': parse_time(start_dt, all_day),
        'end': parse_time(end_dt, all_day)
    }
    return body
