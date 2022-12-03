import requests, json
from datetime import datetime, timezone
from dateutil import tz
from os import environ
from tabulate import tabulate


COOKIES = { 'session': environ['SESSION'] }
YEAR = 2022
BOARD = 673955
URL = f'https://adventofcode.com/{YEAR}/leaderboard/private/view/{BOARD}.json'


def str_time(unix_time):
    return datetime.fromtimestamp(unix_time, tz=timezone.utc) \
                   .astimezone(tz.tzlocal()) \
                   .strftime('%d/%m %H:%M')

members = requests.get(URL, cookies=COOKIES).json()['members'].values()
# members = json.load(open('cache.json'))['members'].values()

members_play = [member for member in members if member['local_score'] > 0]
members_sorted = sorted(members_play,
                        key=lambda member: member['local_score'],
                        reverse=True)

members_table = []
for member in members_sorted:
    puzzle_endtimes = {}
    for day, day_value in member['completion_day_level'].items():
        for part, part_value in day_value.items():
            star_str_time = str_time(part_value['get_star_ts'])
            puzzle_endtimes[f'Day {day} - part {part}'] = star_str_time

    members_table.append({**{
        'Name': member['name'],
        'Global Score': member['global_score'],
        'Local Score': member['local_score'],
        'Stars': member['stars']
    }, **dict(sorted(puzzle_endtimes.items()))})

print(tabulate(members_table, headers='keys', tablefmt='rounded_grid'))
