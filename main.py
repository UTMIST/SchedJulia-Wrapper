from dotenv import load_dotenv
from os.path import join, dirname
from src import schedule

import os

commands = [
    'mv data/*.txt SchedJulia/data/',
    'cd SchedJulia',
    'julia schedjulia.jl',
    'cp data/*.txt ../data/',
    'cd ../',
]

if __name__ == '__main__':
    load_dotenv(join(dirname(__file__), '.env'))
    a = schedule.Schedule()
    a.read_from_sheets()
    os.system(' && '.join(commands))
    a.write_to_sheets()
