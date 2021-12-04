#!/bin/python3

def p1(args):
	actions = {
		'forward': lambda h, d, x: (h + x, d),
		'down'   : lambda h, d, x: (h, d + x),
		'up'     : lambda h, d, x: (h, d - x)
	}
	horizontal, depth = 0, 0

	with open(args.file, 'r') as f:
		for action, x in (line.strip().split(' ') for line in f):
			horizontal, depth = actions[action](horizontal, depth, int(x))

	print(f'{horizontal=} * {depth=}: {horizontal*depth}')

def p2(args):
	actions = {
		'forward': lambda h, d, a, x: (h + x, d + x * a, a),
		'down': lambda h, d, a, x: (h, d, a + x),
		'up': lambda h, d, a, x: (h, d, a - x)
	}
	horizontal, depth, aim = 0, 0, 0

	with open(args.file, 'r') as f:
		for action, x in (line.strip().split(' ') for line in f):
			horizontal, depth, aim = actions[action](horizontal, depth, aim, int(x))

	print(f'{horizontal=} * {depth=} = {horizontal*depth}')


if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str)
	args = parser.parse_args()

	p1(args)
	p2(args)
