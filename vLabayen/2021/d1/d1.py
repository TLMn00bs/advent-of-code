#!/bin/python3
from common.window_iterator import iter_window

def p1(args):
	n = 0
	with open(args.file, 'r') as f:
		data_gen = (int(line.strip()) for line in f)
		current = next(data_gen)
		for depth in data_gen:
			if current < depth: n += 1
			current = depth

	print(n)

def p2(args):
	n = 0
	with open(args.file, 'r') as f:
		data_gen = iter_window((int(line.strip()) for line in f), n = 3)
		current = sum(next(data_gen))
		for depth in (sum(w) for w in data_gen):
			if current < depth: n += 1
			current = depth

	print(n)

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str)
	args = parser.parse_args()

	p1(args)
	p2(args)
