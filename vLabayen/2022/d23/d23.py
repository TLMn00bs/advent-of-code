#!/bin/python3
import logging
from typing import Tuple, Iterable, Set, List, Callable, Dict
from enum import Enum
from collections import defaultdict
from itertools import count

Coordinate = Tuple[int, int]

class Direction(Enum):
	N  = ( 0, -1)
	S  = ( 0, +1)
	W  = (-1,  0)
	E  = (+1,  0)
	NE = (+1, -1)
	NW = (-1, -1)
	SE = (+1, +1)
	SW = (-1, +1)

def move(position: Coordinate, direction: Direction) -> Coordinate:
	x, y = position
	dx, dy = direction.value
	return (x + dx, y + dy)

def adyacent_positions(position: Coordinate) -> Iterable[Coordinate]:
	for direction in Direction: yield move(position, direction)

def is_position_occupied(position: Coordinate, direction: Direction, elves: Set[Coordinate]) -> bool:
	return move(position, direction) in elves

def should_propose_move(position: Coordinate, elves: Set[Coordinate]) -> bool:
	return any(is_position_occupied(position, d, elves) for d in Direction)

def propose_move_in_direction(position: Coordinate, elves: Set[Coordinate], directions: List[Direction]) -> bool:
	return not any(is_position_occupied(position, d, elves) for d in directions)

def should_propose_move_north(position, elves): return propose_move_in_direction(position, elves, [Direction.N, Direction.NE, Direction.NW])
def should_propose_move_south(position, elves): return propose_move_in_direction(position, elves, [Direction.S, Direction.SE, Direction.SW])
def should_propose_move_west (position, elves): return propose_move_in_direction(position, elves, [Direction.W, Direction.NW, Direction.SW])
def should_propose_move_east (position, elves): return propose_move_in_direction(position, elves, [Direction.E, Direction.NE, Direction.SE])

def print_elves(elves: Set[Coordinate], title: str) -> None:
	max_x, min_x = max(x for x, y in elves), min(x for x, y in elves)
	max_y, min_y = max(y for x, y in elves), min(y for x, y in elves)

	xrange = range(min_x - 1, max_x + 2)
	yrange = range(min_y - 1, max_y + 2)
	repr = lambda c: '#' if c in elves else '.'

	print(f'== {title} ==')
	for y in yrange: print(''.join(repr((x, y)) for x in xrange))
	print()

def get_containing_rectangle_area(elves: Set[Coordinate]) -> int:
	max_x, min_x = max(x for x, y in elves), min(x for x, y in elves)
	max_y, min_y = max(y for x, y in elves), min(y for x, y in elves)

	return (max_x - min_x + 1) * (max_y - min_y + 1)

def read_file(file: str) -> Iterable[Coordinate]:
	with open(file, 'r') as f:
		for y, line in enumerate((l.strip() for l in f)):
			for x, c in enumerate(line):
				if c == '#': yield x, y

def p1(args):
	elves = set(read_file(args.file))
	proposing_order: List[Tuple[Callable[[Coordinate, Set[Coordinate]], bool], Direction]] = [
		(should_propose_move_north, Direction.N),
		(should_propose_move_south, Direction.S),
		(should_propose_move_west , Direction.W),
		(should_propose_move_east , Direction.E),
	]
	
	# print_elves(elves, 'Initial State')

	for round in range(10):
		round_proposing_order = [proposing_order[(round + i) % 4] for i in range(4)]

		elves_proposing_to_move = sorted([elve for elve in elves if should_propose_move(elve, elves)], key = lambda elve: elve[::-1])

		elves_proposed_destinations: Dict[Coordinate, Coordinate] = {}
		requested_destinations = defaultdict(lambda: 0)
		for elve in elves_proposing_to_move:
			for propose_to_move, direction in round_proposing_order:
				if propose_to_move(elve, elves):
					destination = move(elve, direction)
					elves_proposed_destinations[elve] = destination
					requested_destinations[destination] += 1
					break

		new_destinations = set(destination for destination, num_times_requested in requested_destinations.items() if num_times_requested == 1)
		moving_elves = set(elve for elve, destionation in elves_proposed_destinations.items() if destionation in new_destinations)

		elves.difference_update(moving_elves)
		elves.update(new_destinations)
		# print_elves(elves, f'End of Round {round + 1}')

	print(get_containing_rectangle_area(elves) - len(elves))

def p2(args):
	_ = read_file(args.file)

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, default='input.txt')
	parser.add_argument('-v', '--verbose', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}, default='WARNING')
	args = parser.parse_args()

	logging.basicConfig(level=args.verbose)

	p1(args)
	p2(args)
