#!/bin/python3
import re

parse_fold = re.compile('fold along (x|y)=([0-9]+)')
def parse_input(file):
	dots, folds = set(), []
	with open(file, 'r') as f:
		for line in (l.strip() for l in f):
			if line == "": break
			x,y = [int(n) for n in line.split(',')]
			dots.update([(x, y)])

		for line in f:
			fold_axis, fold_coord = parse_fold.match(line).groups()
			folds.append((fold_axis, int(fold_coord)))
	return dots, folds

def fold(dots, axis, coord):
	if axis == 'x': return {(x, y) if x < coord else (coord * 2 - x, y) for x,y in dots}
	if axis == 'y': return {(x, y) if y < coord else (x, coord * 2 - y) for x,y in dots}

def display_paper(dots):
	x_size, y_size = max(x for x,y in dots) + 1, max(y for x,y in dots) + 1
	for y in range(y_size): print(''.join('#' if (x,y) in dots else '.' for x in range(x_size)))

def p1(args):
	dots, folds = parse_input(args.file)
	fold_axis, fold_coord = folds[0]
	dots = fold(dots, *fold_axis, fold_coord)
	print(len(dots))

def p2(args):
	dots, folds = parse_input(args.file)
	for fold_axis, fold_coord in folds: dots = fold(dots, fold_axis, fold_coord)
	display_paper(dots)

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str)
	args = parser.parse_args()

	p1(args)
	p2(args)
