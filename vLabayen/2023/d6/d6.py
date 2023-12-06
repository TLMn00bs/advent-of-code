import logging
from typing import List, Tuple
import re
from attrs import define
import math
from functools import reduce

@define
class Race:
	time    : int
	distance: int

parse_numbers_rgx = re.compile('[0-9]+')
def read_file(file: str) -> List[Race]:
	with open(file, 'r') as f:
		lines = (l.strip() for l in f)
		times     = (int(n) for n in parse_numbers_rgx.findall(next(lines)))
		distances = (int(n) for n in parse_numbers_rgx.findall(next(lines)))
		return [Race(time, distance) for time, distance in zip(times, distances)]

def get_first_and_last_winning_holding_times(race: Race) -> Tuple[int, int]:
	'''
	holding_time * (time - holding_time) = holding_time * time - holding_time^2 = distance
	-1 * holding_time^2 + time * holding_time - distance = 0 
	holding_time = (-b +- sqrt(b^2 - 4ac)) / 2a 

	a = -1, b = time, c = -distance
	holding_time = (-time +- sqrt(time^2 - 4 * distance)) / -2 
	holding_time = time/2 -+ sqrt(time^2 - 4 * distance) / 2 
	'''
	first_term = race.time / 2
	second_term = math.sqrt((race.time ** 2) - (4 * race.distance)) / 2

	solutions = (first_term + second_term, first_term - second_term)
	first, last = sorted(solutions)
	return math.ceil(first + 1e-9), math.floor(last - 1e-9)

def get_number_of_wining_options(race: Race) -> int:
	first, last = get_first_and_last_winning_holding_times(race)
	return last - first + 1


def p1(args):
	races = read_file(args.file)

	number_of_winning_options = (get_number_of_wining_options(race) for race in races)
	print(reduce(lambda acc, next: acc * next, number_of_winning_options, 1))

def p2(args):
	_ = read_file(args.file)

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str, default='input.txt')
	parser.add_argument('-v', '--verbose', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}, default='WARNING')
	args = parser.parse_args()

	logging.basicConfig(level=args.verbose)

	p1(args)
	p2(args)
