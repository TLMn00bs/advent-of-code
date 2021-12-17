#!/bin/python3
import re
import math
from itertools import count

def valid_hvel(x1, x2):
	x_range = set(range(x1, x2 + 1))
	for v in range(1, x2 + 1):
		xpos, curr_v, first_step = 0, v, None
		for step in count():
			if xpos in x_range and first_step is None: first_step = step

			xpos += curr_v
			curr_v -= 1
			if xpos > x2:
				if first_step is not None: yield v, (first_step, step)
				break

			if curr_v == 0:
				if first_step is not None: yield v, (first_step, math.inf)
				break

def valid_yvel(y1, y2):
	min_y, max_y = min(y1, y2), max(y1, y2)
	y_range = set(range(min_y, max_y + 1))
	for i in count():
		v = min_y + i
		ypos, curr_v = 0, v
		for step in count():
			if ypos in y_range: yield v, step

			ypos += curr_v
			curr_v -= 1
			if ypos < min_y: break

		# If we start at y=0 and shot upwards, we will return to y=0 with v=-v0
		# for v0 = 3
		# y: 0, 3, 5, 6, 6,  5,  3,  0
		# v:    3, 2, 1, 0, -1, -2, -3
		# So any starting velocity gt than min_y, will skip the target area
		if v > abs(min_y): break

def reached_y(yvel): return sum(range(yvel + 1))

parse_rgx = re.compile('target area: x=(-?[0-9]+)..(-?[0-9]+), y=(-?[0-9]+)..(-?[0-9]+)')
def p1(args):
	with open(args.file, 'r') as f: x1, x2, y1, y2 = [int(n) for n in parse_rgx.match(f.readline().strip()).groups()]
	hvel_step = [*valid_hvel(x1, x2)]
	yvel_step = [*valid_yvel(y1, y2)]

	for yvel, step in sorted(yvel_step, reverse=True):
		for xvel, (first_step, last_step) in hvel_step:
			if first_step <= step <= last_step:
				print(reached_y(yvel))
				return

def p2(args):
	with open(args.file, 'r') as f: x1, x2, y1, y2 = [int(n) for n in parse_rgx.match(f.readline().strip()).groups()]
	hvel_step = [*valid_hvel(x1, x2)]
	yvel_step = [*valid_yvel(y1, y2)]

	opts = set()
	for yvel, step in yvel_step:
		for xvel, (first_step, last_step) in hvel_step:
			if first_step <= step <= last_step: opts.update([(xvel, yvel)])
	print(len(opts))

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str)
	args = parser.parse_args()

	p1(args)
	p2(args)
