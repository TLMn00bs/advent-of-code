#!/bin/python3
import json
from math import floor, ceil, inf
from itertools import product

def expand(number, nest_level = 0):
	if not isinstance(number, list): return [number, nest_level]
	for pair_element in number:
		if not isinstance(pair_element, list):
			yield [pair_element, nest_level + 1]
			continue

		for num, nest in expand(pair_element, nest_level + 1): yield [num, nest]

def reduce(expanded):
	reduced, has_changed = expanded, None
	while has_changed != False:
		has_changed = False
		#print(reduced)

		data_gen = ((i, num, nest) for i, (num, nest) in enumerate(expanded))
		for i, num, nest in data_gen:
			if nest > 4:
				_, next_num, _ = next(data_gen)
				if i != 0: reduced[i - 1][0] += num
				if i != len(expanded) - 2: reduced[i + 2][0] += next_num
				reduced = reduced[:i] + [[0, nest - 1]] + reduced[i+2:]
				has_changed = True
				break
		else:
			data_gen = ((i, num, nest) for i, (num, nest) in enumerate(expanded))
			for i, num, nest in data_gen:
				if num >= 10:
					reduced = reduced[:i] + [[floor(num / 2), nest + 1], [ceil(num / 2), nest + 1]] + reduced[i+1:]
					has_changed = True
					break

		expanded = reduced

#	print()
	return reduced

def add(a, b): return [[num, nest + 1] for num, nest in a] + [[num, nest + 1] for num, nest in b]

def magnitude(expanded):
	mag, has_changed = expanded, None
	while has_changed != False:
		has_changed = False
		#print(mag)

		data_gen = ((i, num, nest) for i, (num, nest) in enumerate(expanded))
		next(data_gen)
		for i, num, nest in data_gen:
			past_num, past_nest = expanded[i - 1]
			if nest == past_nest:
				mag = mag[:i-1] + [[3 * past_num + 2 * num, nest - 1]] + mag[i+1:]
				has_changed = True
				break

		expanded = mag
	return mag[0][0]

def p1(args):
	with open(args.file, 'r') as f: numbers = [json.loads(line) for line in f]

	curr_sum = reduce(list(expand(numbers[0])))
	for number in numbers[1:]:
		expanded = list(expand(number))
		reduced = reduce(expanded)
		curr_sum = reduce(add(curr_sum, reduced))
	#print(curr_sum)

	print(magnitude(curr_sum))

def p2(args):
	with open(args.file, 'r') as f: numbers = [json.loads(line) for line in f]

	max_mag_sum = -inf
	all_opts = [(x, y) for x,y in product(range(len(numbers)), range(len(numbers))) if x != y]
	for x, y in ((numbers[x], numbers[y]) for x, y in all_opts):
		rx, ry = reduce(list(expand(x))), reduce(list(expand(y)))
		mag = magnitude(reduce(add(rx, ry)))
		if mag > max_mag_sum: max_mag_sum = mag
	print(max_mag_sum)

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str)
	args = parser.parse_args()

	p1(args)
	p2(args)
