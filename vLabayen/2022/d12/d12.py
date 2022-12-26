#!/bin/python3
from domain import *
import logging
import math

def read_file(file: str) -> HeightMap:
	with open(file, 'r') as f:
		lines = [line.strip() for line in f]

	return HeightMap.from_lines(lines)

def p1(args):
	hmap = read_file(args.file)
	path_len = hmap.find_path_lenght(hmap.starting_location, hmap.best_signal_location)
	print(path_len)

def p2(args):
	hmap = read_file(args.file)
	possible_starting_locations = [location for location in hmap.locations.values() if location.height == 1]

	min_path_len = math.inf
	for i, location in enumerate(possible_starting_locations):
		logging.debug(f'Computing path for starting location {i}: {location}')
		path_len = hmap.find_path_lenght(location, hmap.best_signal_location)

		if path_len != None:
			min_path_len = min(min_path_len, path_len)

	print(min_path_len)



if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, default='input.txt')
	parser.add_argument('-v', '--verbose', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}, default='WARNING')
	args = parser.parse_args()

	logging.basicConfig(level=args.verbose)

	p1(args)
	p2(args)
