#!/bin/pyhon3
import sys
import json
import tabulate
import requests
from datetime import datetime as dt

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('person')
parser.add_argument('session')
args = parser.parse_args()

r = json.loads(requests.get('https://adventofcode.com/2021/leaderboard/private/view/1065002.json', cookies={'session': args.session}).text)
try: person_id = [key for key, member in r['members'].items() if member['name'] == args.person][0]
except: sys.exit(f'{args.person} not found')

person = r['members'][person_id]
completion_day_level = sorted([(int(day), obj) for day, obj in person['completion_day_level'].items()])

raw_table = [[day, obj['1']['get_star_ts'], obj['2']['get_star_ts']] for day, obj in completion_day_level]
table = [[day, dt.fromtimestamp(first_star), dt.fromtimestamp(second_star), second_star - first_star] for (day, first_star, second_star) in raw_table]

print(tabulate.tabulate(table, headers=['Day', 'First star', 'Second star', 'Elapsed (s)']))
