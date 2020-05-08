import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def day(i: int) -> str:
    """Return a valid day from its corresponding int value."""
    return os.getenv("DAYS").split('~')[i//int(os.getenv("DAY_SIZE"))]


def time(index: int) -> str:
    """Return a valid time from its corresponding int value."""

    start_hour, start_minute = os.getenv("START_TIME").split(':')
    start_hour, start_minute = int(start_hour), int(start_minute)
    if not 0 <= start_hour < 24 or not 0 <= start_minute < 60:
        exit(1)

    unit = int(os.getenv("TIME_UNIT"))
    index_of_day = index % int(os.getenv("DAY_SIZE"))
    hour = start_hour + (unit*index_of_day)//60
    minute = (start_minute + unit*index_of_day) % 60

    return "{:02d}".format(hour) + ':' + "{:02d}".format(minute)


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
            if len(e) < 5 or e[0] == os.getenv("NULL_NAME"):
                continue
            if len(e[1]) == 0 or len(e[2]) == 0 or len(e[3]) == 0:
                continue
            if e[3] != os.getenv("WEEK"):
                continue

            name = e[0]
            actual_name = name
            if ' [' in actual_name:
                actual_name = name[:name.index(' [')]

            self.names.append(name)
            self.interviewers[name] = e[1].split(
                ', ') + [actual_name]
            self.durations[name] = e[2]
            self.positions[name] = e[4]

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
        for i in interviews:
            interviewee, times, names = tuple(i.split('|'))
            names = names.rstrip().split(',')

            start, end = tuple(times.split('-'))
            duration = int(end)-int(start)+1
            duration = f'{duration//2}:{"30" if duration%2 == 1 else "00" }'
            datetime = f'{day(int(start))}, {time(int(start))}'

            for j in range(len(names)-1, -1, -1):
                if len(names[j]) == 0:
                    continue
                if ' ' in names[j] or names[j][0] == '!':
                    names.pop(j)

            interviewers = [name for name in names if ' ' not in name]
            interviewers.sort()
            values.append([
                datetime,
                duration,
                interviewee,
                ', '.join(interviewers),
                self.positions[interviewee]])

        body = {'values': values}
        self.sheets.values().update(
            spreadsheetId=os.getenv("SPREADSHEET_ID"),
            range=os.getenv("OUTPUT_RANGE"),
            valueInputOption='RAW',
            body=body).execute()
