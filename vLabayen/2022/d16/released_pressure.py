import argparse
from domain import *

parser = argparse.ArgumentParser()
parser.add_argument('choices', type=str, nargs='+', default=[])
parser.add_argument('-f', '--file', type=str, default='example.txt')
args = parser.parse_args()

w = Wrapper(args.file, 'AA', 30)
upper_limit = w.get_upper_limit(args.choices)
released_pressure = w.get_released_pressure(args.choices)

print(f'{upper_limit=}')
print(f'{released_pressure=}')
