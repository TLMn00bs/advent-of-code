#!/bin/python3
import re
from collections import Counter
from itertools import product

def parse_file(file):
	parse_coords = re.compile('([0-9]+),([0-9]+) -> ([0-9]+),([0-9]+)')
	with open(file, 'r') as f:
		for i,line in enumerate(l.strip() for l in f):
			x1,y1,x2,y2 = parse_coords.match(line).groups()
			yield int(x1), int(y1), int(x2), int(y2)

def coords2vhlines(x1, y1, x2, y2):
	x_offset = 1 if x2 > x1 else -1
	y_offset = 1 if y2 > y1 else -1
	x_range = [*range(x1, x2 + x_offset, x_offset)]
	y_range = [*range(y1, y2 + y_offset, y_offset)]
	return [*product(x_range, y_range)]

def coords2diaglines(x1, y1, x2, y2):
	x_offset = 1 if x2 > x1 else -1
	y_offset = 1 if y2 > y1 else -1
	x_range = [*range(x1, x2 + x_offset, x_offset)]
	y_range = [*range(y1, y2 + y_offset, y_offset)]
	return [*zip(x_range, y_range)]

def display_grid(vents_coords):
	x, y = zip(*vents_coords.keys())
	max_x, max_y = max(x), max(y)

	grid = [[0 for x in range(max_x + 1)] for y in range(max_y + 1)]
	for (x, y), n in vents_coords.items(): grid[y][x] += n

	for row in grid:
		print(''.join([str(n) if n > 0 else '.' for n in row]))


def p1(args):
	vents_coords = Counter()
	for x1, y1, x2, y2 in parse_file(args.file):
		if not (x1 == x2 or y1 == y2): continue
		vhlines = coords2vhlines(x1, y1, x2, y2)
		vents_coords.update(vhlines)

	#display_grid(vents_coords)
	dangerous_points = [(x,y) for (x,y), n in vents_coords.items() if n >= 2]
	print(len(dangerous_points))

def p2(args):
	vents_coords = Counter()
	for x1, y1, x2, y2 in parse_file(args.file):
		fnc = coords2vhlines if (x1 == x2 or y1 == y2) else coords2diaglines
		vents_coords.update(fnc(x1, y1, x2, y2))

	#display_grid(vents_coords)
	dangerous_points = [(x,y) for (x,y), n in vents_coords.items() if n >= 2]
	print(len(dangerous_points))


if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str)
	args = parser.parse_args()

	p1(args)
	p2(args)
