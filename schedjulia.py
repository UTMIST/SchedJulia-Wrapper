from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

SPREADSHEET_ID = '1X2yLsEdG45wdGddJ3uVlRKciVGtfSoGp9nmwVH1OvqA'
INPUT_RANGES = ['Interview List!A23:D', 'Interview Availability!A2:K']
OUTPUT_RANGE = 'Interview Schedule!A2:C'
DAYS = ['Tuesday, May 5th', 'Wednesday, May 6th', 'Thursday, May 7th',
        'Friday, May 8th', 'Saturday, May 9th']


def day(i: int) -> str:
    """Return a valid day from its corresponding int value."""
    return DAYS[i//16]


def time(i: int) -> str:
    """Return a valid time from its corresponding int value."""
    return f'{i % 16 // 2}:{i % 2 * 3}0'


def read_data():
    """Read the applications spreadsheets and return API Resource."""
    creds = None
    # The file token.pickle stores the user's access and refresh tokens,
    # and is created automatically when the authorization flow completes
    # for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('sheets', 'v4', credentials=creds).spreadsheets()


class Schedule:
    """Schedule class. Contains all relevant info on a student based on their
    unique identifier.
    names: all applicant names
    interviewers: {name: [interviewers]}
    positions: {name: [applied positions]}
    emails: {name: email}
    platforms: {name: [preferred platforms]}
    timeslots: {name: [available time slots]
    sheets: Resource object for making sheet API calls"""

    def __init__(self) -> None:
        self.names = []
        self.interviewers = {}
        self.positions = {}
        self.durations = {}
        self.emails = {}
        self.platforms = {}
        self.timeslots = {}
        self.sheets = read_data()
        results = self.sheets.values().batchGet(spreadsheetId=SPREADSHEET_ID,
                                                ranges=INPUT_RANGES).execute()
        values = results.get('valueRanges', [])
        for e in values[0]['values']:
            self.names.append(name := e[0])
            self.interviewers[name] = e[1].split(', ')
            self.positions[name] = e[2].split(', ')
            self.durations[name] = 1 if len(e) != 4 else e[3]
        for f in values[1]['values']:
            name = f'{f[1]} {f[2]}'
            self.emails[name] = f[3]
            self.platforms[name] = f[4].split(', ')
            self.timeslots[name] = [int((int(j[:2])-12)*2+int(j[3])/3+16*(i-5))
                                    for i in range(5, 10)
                                    for j in f[i].split(', ')
                                    if f[i]]

    def read_from_sheets(self) -> None:
        """Reads from sheets and writes to appointments.txt and
        availability.txt"""
        with open('SchedJulia/data/availability.txt', 'w') as file1:
            file1.write('\n '.join(j+'|'+','.join(
                str(i) for i in self.timeslots[j])
                       for j in self.timeslots))
        durations = {v: [k for k in self.durations if self.durations[k] == v]
                     for k, v in self.durations.items()}
        with open('SchedJulia/data/appointments.txt', 'w') as file2:
            file2.write('\n '.join(str(j) + '|' + ','.join(
                str(i) for i in durations[j])
                                  for j in durations))

    def write_to_sheets(self) -> None:
        """Writes schedule.txt data to sheets"""
        with open('SchedJulia/data/schedule.txt') as file:
            interviews = file.readlines()
        values = []
        body = {'values': values}
        for i in interviews:
            t, n = tuple(i.split('|'))
            t1, t2 = tuple(t.split('-'))
            datetime = f'{time(int(t1))}-{time(int(t2))}, {day(int(t1))}'
            names = n.rstrip().split(',')
            interviewee = ''
            for n1 in names:
                if ' ' in n1:
                    interviewee = n1
            names.remove(interviewee)
            values.append([datetime, interviewee, ', '.join(names)])
        self.sheets.values().update(spreadsheetId=SPREADSHEET_ID,
                                    range=OUTPUT_RANGE,
                                    valueInputOption='RAW',
                                    body=body).execute()


if __name__ == '__main__':
    a = Schedule()
    a.read_from_sheets()
    a.write_to_sheets()

