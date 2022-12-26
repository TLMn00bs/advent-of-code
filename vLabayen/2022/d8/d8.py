#!/bin/python3
from domain import *
from itertools import product

def read_file(file: str):
	with open(file, 'r') as f:
		lines = [line.strip() for line in f]
	
	return Grid.from_text(lines)

def p1(args):
	grid = read_file(args.file)
	rows, cols = grid.size()
	coords = product(range(rows), range(cols))
	num_visible_trees = sum(1 for x, y in coords if is_visible(x, y, grid))
	print(num_visible_trees)

def p2(args):
	grid = read_file(args.file)
	rows, cols = grid.size()
	coords = product(range(rows), range(cols))
	scenic_scores = [scenic_score(x, y, grid) for x, y in coords]
	print(max(scenic_scores))

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, default='input.txt')
	args = parser.parse_args()

	p1(args)
	p2(args)
