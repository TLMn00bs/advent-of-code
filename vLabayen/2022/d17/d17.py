#!/bin/python3
from typing import Set, Tuple, List
from collections import Counter, defaultdict
import logging
from jets import jets_gen, Jet
from rocks import falling_rocks, Rock


def print_rocks(rocks: Set[Tuple[int, int]], highest_rock: int, flying_rock: List[Tuple[int, int]] = []):
	for y in range(highest_rock + 7, 0, -1):
		print('|', end='')
		for x in range(1, 8):
			c = '#' if (x, y) in rocks else (
				'@' if (x, y) in flying_rock else '.'
			)
			print(c, end='')

		print('|')

	print('+-------+')

def push(rock: Rock, jet: Jet, rocks: Set[Tuple[int, int]]):
	if jet == Jet.left and not rock.collide_left(occuped_places=rocks):
		rock.move(delta_x = -1, delta_y = 0)

	if jet == Jet.right and not rock.collide_right(occuped_places=rocks):
		rock.move(delta_x = +1, delta_y = 0)

def fall(rock: Rock, rocks: Set[Tuple[int, int]]) -> bool:
	if not rock.collide_down(occuped_places=rocks):
		rock.move(delta_x = 0, delta_y = -1)
		return True
	
	return False

def p1(args):
	jets = jets_gen(args.file)

	highest_rock = 0
	rocks: Set[Tuple[int, int]] = set()
	for rock in falling_rocks(2022, start_x = 2, start_y = lambda: highest_rock + 3):
		_, jet = next(jets)

		while True:
			push(rock, jet, rocks)
			falling = fall(rock, rocks)
			if not falling: break
			_, jet = next(jets)

		highest_rock = max(highest_rock, rock.highest_y)
		rocks.update(rock.rocks)
	
	print(highest_rock)

def find_loop(file: str):
	jets = jets_gen(args.file)

	starts = Counter()
	heights = defaultdict(list)

	highest_rock = 0
	rocks: Set[Tuple[int, int]] = set()
	for i, rock in enumerate(falling_rocks(10_000, start_x = 2, start_y = lambda: highest_rock + 3)):
		idx, jet = next(jets)
		start = (idx, rock.__class__)

		starts.update({start: 1})
		heights[start].append((highest_rock, i))

		while True:
			push(rock, jet, rocks)
			falling = fall(rock, rocks)
			if not falling: break
			_, jet = next(jets)

		highest_rock = max(highest_rock, rock.highest_y)
		rocks.update(rock.rocks)
	
	(start, _), *_ = starts.most_common(1)
	h1, idx1 = heights[start][-2]
	h2, idx2 = heights[start][-1]

	remaining_rocks = (1000000000000 - idx2)
	complete_loops = remaining_rocks // (idx2 - idx1)
	delta_h = complete_loops * (h2 - h1)

	starting_height = h2 + delta_h
	rocks_from_last_complete_loop = remaining_rocks % (idx2 - idx1)
	return starting_height, rocks_from_last_complete_loop, idx2, h2


def p2(args):
	starting_height, do_rocks, skip_rooks, skip_height = find_loop(args.file)

	jets = jets_gen(args.file)

	highest_rock = 0
	rocks: Set[Tuple[int, int]] = set()
	for rock in falling_rocks(skip_rooks + do_rocks, start_x = 2, start_y = lambda: highest_rock + 3):
		_, jet = next(jets)

		while True:
			push(rock, jet, rocks)
			falling = fall(rock, rocks)
			if not falling: break
			_, jet = next(jets)

		highest_rock = max(highest_rock, rock.highest_y)
		rocks.update(rock.rocks)
	
	print(starting_height + (highest_rock - skip_height))

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, default='input.txt')
	parser.add_argument('-v', '--verbose', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}, default='WARNING')
	args = parser.parse_args()

	logging.basicConfig(level=args.verbose)

	# p1(args)
	p2(args)
