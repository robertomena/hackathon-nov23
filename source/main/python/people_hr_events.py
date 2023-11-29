
import datetime
from utils import parse_to_write
from icalendar import Calendar
import requests

class PeopleHREvents:
    def __init__(self, remote_url, local_ical=None):
        self.remote_url = remote_url
        self.local_ical = local_ical
        self.calendar = None

    def _read_file_from_url(self):
        try:
            response = requests.get(self.remote_url)
            if response.status_code == 200:
                return response.text
            else:
                raise Exception(f"Failed to read file from URL: {self.remote_url}")
        except e:
            print("error while reading ical from {}. Error: {}".format(self.remote_url, e))

    def get_ical(self, is_remote: bool):
        # testing purposes
        if not is_remote:
            with open(self.local_ical) as file:
                self.calendar = Calendar.from_ical(file.read())
        else:
            self.calendar = Calendar.from_ical(self._read_file_from_url())

    def parse_ical(self, dpbi_names):
        dpbi_events = []

        for event in self.calendar.walk('VEVENT'):
            if any(map(event.get("DESCRIPTION").__contains__, dpbi_names)):

                start_dt = event.get("DTSTART").dt
                end_dt = event.get("DTEND").dt
                if isinstance(start_dt, (datetime.datetime)):
                    all_day = False
                else:
                    all_day = True
                    start_dt = datetime.datetime.combine(start_dt, datetime.datetime.min.time())
                    end_dt = datetime.datetime.combine(end_dt, datetime.datetime.min.time())

                tmp = parse_to_write(event.get("SUMMARY"), start_dt, end_dt, all_day)
                dpbi_events.append(tmp)
        return dpbi_events
