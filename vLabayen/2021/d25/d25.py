#!/bin/python3
from itertools import count

def parse(file):
	east_sea_cucumbers = set()
	south_sea_cucumbers = set()
	with open(args.file, 'r') as f:
		for y, line in enumerate(l.strip() for l in f):
			for x, sea_cucumber in ((c, s) for c,s in enumerate(line) if c != '.'):
				if sea_cucumber == '>': east_sea_cucumbers.add((x, y))
				if sea_cucumber == 'v': south_sea_cucumbers.add((x, y))

	return east_sea_cucumbers, south_sea_cucumbers, x + 1, y + 1

def next_east_position(x, y, len_x):
	if x + 1 == len_x: return 0, y
	return x + 1, y
def next_south_position(x, y, len_y):
	if y + 1 == len_y: return x, 0
	return x, y + 1

def next_position(x, y, len_x, len_y, direction):
	if direction == 'E': return next_east_position(x, y, len_x)
	if direction == 'S': return next_south_position(x, y, len_y)

def display(east, south, len_x, len_y):
	for y in range(len_y):
		print(''.join('>' if (x, y) in east else ('v' if (x, y) in south else '.') for x in range(len_x)))

def p1(args):
	east, south, len_x, len_y = parse(args.file)

#	for i in range(1):
	for i in count():
		new_east, new_south, has_moved = set(), set(), False

		for pos in east:
			next_pos = next_position(*pos, len_x, len_y, 'E')
			if next_pos in east or next_pos in south: new_east.add(pos)
			else:
				new_east.add(next_pos)
				has_moved = True
		east = new_east

		for pos in south:
			next_pos = next_position(*pos, len_x, len_y, 'S')
			if next_pos in east or next_pos in south: new_south.add(pos)
			else:
				new_south.add(next_pos)
				has_moved = True
		south = new_south

		print(i + 1)
		if not has_moved: return

def p2(args):
	pass

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str)
	args = parser.parse_args()

	p1(args)
	p2(args)
