
import datetime
from utils import parse_to_write
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



class GSheet():
    def __init__(self, credentials: Credentials, sheet_id: str, range_name: str):
        self.gservice = build("sheets", "v4", credentials=credentials)
        self.sheet_id = sheet_id
        self.range_name = range_name

    def _parse_scanned_rota(self, list_rows: list) -> list:
        """
        :param list_rows: list of list, where each inner list has the following schema
             [0] Name, [1] from date in format <TODO>, [2] to date in format <TODO>
        """
        current_day = datetime.datetime.utcnow()
        dpbi_rota = []
        for row in list_rows:
            if '' in row:
                print("Cannot Parse this row {}".format(row))
                continue
            else:
                summary = '{} is on Rota'.format(row[0])
                start =  datetime.datetime.strptime(row[1], '%a, %b %d %Y')
                start_dt = datetime.datetime.combine(start, datetime.datetime.min.time())
                end = datetime.datetime.strptime(row[2], '%a, %b %d %Y')
                end_dt = datetime.datetime.combine(end, datetime.datetime.max.time())
            # only returns the list where date are from current_date to the future
            if start > current_day:
                tmp = parse_to_write(summary, start_dt, end_dt, False)
                dpbi_rota.append(tmp)
        return dpbi_rota

    def get_data_from_sheet(self):
        params = {"spreadsheetId": self.sheet_id,
                  "range": self.range_name}

        try:
            # Call the Calendar API
            events_result = (self.gservice.spreadsheets()
                             .values()
                             .get(**params)
                             .execute())
            values = events_result.get("values", [])

            if not values:
                print("No data found.")
                return

            return self._parse_scanned_rota(values)

        except HttpError as error:
            print(f"An error occurred: {error}")
