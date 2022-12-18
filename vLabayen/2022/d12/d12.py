#!/bin/python3
from domain import *
import logging

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

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, default='input.txt')
	parser.add_argument('-v', '--verbose', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}, default='WARNING')
	args = parser.parse_args()

	logging.basicConfig(level=args.verbose)

	p1(args)
	p2(args)
