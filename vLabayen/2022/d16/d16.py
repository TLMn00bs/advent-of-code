#!/bin/python3
from domain import *
import logging

def read_file(file: str):
	with open(file, 'r') as f:
		lines = [line.strip() for line in f]
	
	return parse_tunnels_layout(lines)

def p0(args):
	w = Wrapper('example.txt', 'AA', 30)
	choices = ['DD', 'BB', 'JJ', 'HH', 'EE', 'CC']

	for i in range(len(choices)):
		c = choices[:i+1]
		up_upper_limit = w.get_upper_limit(c, variant='up')
		down_upper_limit = w.get_upper_limit(c, variant='down')
		logging.debug(f'{up_upper_limit} >= {down_upper_limit} >= ?: {c}')

def p1(args):
	w = Wrapper(args.file, 'AA', 30)
	num_valves = len(list(w.valves()))

	lower_limit = w.get_lower_limit()
	logging.info(f'{lower_limit=}')

	required_choices = [[valve] for valve in w.valves()]
	for i in range(num_valves - 1):
		next_choices = []
		for choices in required_choices:
			next_choices += [opt for opt in w.get_choices_options(choices, lower_limit)]

		required_choices = next_choices
		logging.debug(f'{len(required_choices)=}')

	print(max(w.get_released_pressure(c) for c in required_choices))

def p2(args):
	_ = read_file(args.file)

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, default='input.txt')
	parser.add_argument('-v', '--verbose', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}, default='WARNING')
	args = parser.parse_args()

	logging.basicConfig(level=args.verbose)

	# p0(args)
	p1(args)
	# p2(args)
