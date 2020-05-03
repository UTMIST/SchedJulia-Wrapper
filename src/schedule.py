from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def day(i: int) -> str:
    """Return a valid day from its corresponding int value."""
    return os.getenv("DAYS").split('~')[i//int(os.getenv("DAY_SIZE"))]


def time(i: int) -> str:
    """Return a valid time from its corresponding int value."""
    return f'{i % int(os.getenv("DAY_SIZE")) // 2}:{i % 2 * 3}0'


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
                'credentials.json', os.getenv("SCOPES"))
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

        results = self.sheets.values().batchGet(
            spreadsheetId=os.getenv('SPREADSHEET_ID'),
            ranges=os.getenv("INPUT_RANGES").split('~')).execute()

        values = results.get('valueRanges', [])

        for e in values[0]['values']:
            if e[0] == os.getenv("NULL_NAME") or len(e[1]) == 0 or len(e[2]) == 0 or len(e[3]) == 0:
                continue

            name = e[0]
            self.names.append(name)
            self.interviewers[name] = e[1].split(', ')
            self.durations[name] = e[2]
            self.positions[name] = e[3]
        for f in values[1]['values']:
            name = (f'{f[1]} {f[2]}').strip(' ')
            self.emails[name] = f[3]
            self.platforms[name] = f[4].split(', ')
            self.timeslots[name] = [int((int(j[:2])-12)*2 +
                                        int(j[3])/3 +
                                        int(os.getenv("DAY_SIZE"))*(i-5))
                                    for i in range(5, len(f))
                                    for j in f[i].split(', ')
                                    if f[i]]

    def read_from_sheets(self) -> None:
        """Reads from sheets and writes to appointments.txt and
        availability.txt"""
        with open('data/availability.txt', 'w') as file1:
            file1.write('\n'.join(j+'|'+','.join(
                str(i) for i in self.timeslots[j])
                for j in self.timeslots))

        with open('data/appointments.txt', 'w') as file2:
            lines = '\n'.join(
                n + '|' +
                self.durations[n] + '|' +
                ','.join(str(i) for i in self.interviewers[n]) for n in self.names)

            file2.write(lines)

    def write_to_sheets(self) -> None:
        """Writes schedule.txt data to sheets"""
        with open('data/schedule.txt') as file:
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

        self.sheets.values().update(
            spreadsheetId=os.getenv("SPREADSHEET_ID"),
            range=os.getenv("OUTPUT_RANGE"),
            valueInputOption='RAW',
            body=body).execute()
