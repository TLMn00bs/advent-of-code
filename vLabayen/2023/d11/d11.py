import logging
from attrs import define
from typing import Tuple, Iterable, Set
from itertools import combinations
import math

Coordinate = Tuple[int, int]

@define(hash=True, eq=True)
class Galaxy:
	x: int
	y: int

def manhattan_distance(g1: Galaxy, g2: Galaxy) -> int:
	return abs(g1.x - g2.x) + abs(g1.y - g2.y)

def read_file(file: str) -> Iterable[Galaxy]:
	with open(file, 'r') as f:
		for y, line in enumerate(l.strip() for l in f):
			for x, c in enumerate(line):
				if c == '#': yield Galaxy(x, y)

def sortest_distance(g1: Galaxy, g2: Galaxy, galaxies_in_x: Set[int], galaxies_in_y: Set[int]) -> int:
	pre_expanded_distane = manhattan_distance(g1, g2)
	expanded_x = sum(1 for x in range(g1.x, g2.x, 1 if g2.x > g1.x else -1) if x not in galaxies_in_x)
	expanded_y = sum(1 for y in range(g1.y, g2.y, 1 if g2.y > g1.y else -1) if y not in galaxies_in_y)
	return pre_expanded_distane + expanded_x + expanded_y

def p1(args):
	galaxies = set(read_file(args.file))

	galaxies_in_x = set(g.x for g in galaxies)
	galaxies_in_y = set(g.y for g in galaxies)
	print(sum(sortest_distance(g1, g2, galaxies_in_x, galaxies_in_y) for g1, g2 in combinations(galaxies, 2)))

def p2(args):
	_ = read_file(args.file)

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str, default='input.txt')
	parser.add_argument('-v', '--verbose', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}, default='WARNING')
	args = parser.parse_args()

	logging.basicConfig(level=args.verbose)

	p1(args)
	p2(args)
