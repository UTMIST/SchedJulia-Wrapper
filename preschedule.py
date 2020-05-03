from src import schedule

from os.path import join, dirname
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv(join(dirname(__file__), '.env'))
    a = schedule.Schedule()
    a.read_from_sheets()
    # a.write_to_sheets()
