#!/bin/python3
from typing import Generator, Set, Tuple, List
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

def fall(rock: Rock, jets: Generator[Jet, None, None], rocks: Set[Tuple[int, int]]):
	while True:
		jet = next(jets)

		if jet == Jet.left and not rock.collide_left(occuped_places=rocks):
			rock.move(delta_x = -1, delta_y = 0)

		if jet == Jet.right and not rock.collide_right(occuped_places=rocks):
			rock.move(delta_x = +1, delta_y = 0)

		if not rock.collide_down(occuped_places=rocks):
			rock.move(delta_x = 0, delta_y = -1)
		else: break

def p1(args):
	jets = jets_gen(args.file)

	highest_rock = 0
	rocks: Set[Tuple[int, int]] = set()
	for rock in falling_rocks(2022, start_x = 2, start_y = lambda: highest_rock + 3):
		# print_rocks(rocks, highest_rock=highest_rock, flying_rock=[*rock.rocks])
		# input()

		fall(rock, jets, rocks)

		highest_rock = max(highest_rock, rock.highest_y)
		rocks.update(rock.rocks)
	
	print(highest_rock)

# def p2(args):
# 	_ = read_file(args.file)

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, default='input.txt')
	parser.add_argument('-v', '--verbose', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}, default='WARNING')
	args = parser.parse_args()

	logging.basicConfig(level=args.verbose)

	p1(args)
	# p2(args)
