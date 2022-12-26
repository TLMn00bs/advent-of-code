#!/bin/python3
from domain import *
import logging
import time

def read_file(file: str):
	with open(file, 'r') as f:
		lines = [line.strip() for line in f]
	
	return Cave.from_lines(lines)

def p1(args):
	cave = read_file(args.file)

	status = None
	while (status != SandStatus.VOID):
		status = cave.add_grain()

	print(len(cave.sand_grains))

def p2(args):
	cave = read_file(args.file)

	# The further a grain can go is in diagonal from the source to each side
	# to the floor level
	floor_level = max(y for x, y in cave.rocks) + 2
	origin_x, origin_y = cave.sand_origin
	floor_start_x = origin_x - (floor_level - origin_y + 1)
	floor_end_x   = origin_x + (floor_level - origin_y + 1)
	cave.add_path((floor_start_x, floor_level), (floor_end_x, floor_level))

	while (cave.sand_origin not in cave.sand_grains):
		cave.add_grain()

	print(len(cave.sand_grains))

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, default='input.txt')
	parser.add_argument('-v', '--verbose', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}, default='WARNING')
	args = parser.parse_args()

	logging.basicConfig(level=args.verbose)

	p1(args)
	p2(args)
