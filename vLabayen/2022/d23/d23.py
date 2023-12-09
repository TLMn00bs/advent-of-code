#!/bin/python3
import logging
from attrs import define, field
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

@define
class SoilMap:
	elves: Set[Coordinate]

	has_neighbours   : Dict[Coordinate, bool] = field(init=False, factory=dict)
	should_move_north: Dict[Coordinate, bool] = field(init=False, factory=dict)
	should_move_south: Dict[Coordinate, bool] = field(init=False, factory=dict)
	should_move_west : Dict[Coordinate, bool] = field(init=False, factory=dict)
	should_move_east : Dict[Coordinate, bool] = field(init=False, factory=dict)

	def __attrs_post_init__(self):
		for (x, y) in self.elves:
			self.has_neighbours[(x, y)] = any((
				(x - 1, y - 1) in self.elves,
				(x    , y - 1) in self.elves,
				(x + 1, y - 1) in self.elves,
				(x - 1, y    ) in self.elves,
				(x + 1, y    ) in self.elves,
				(x - 1, y + 1) in self.elves,
				(x    , y + 1) in self.elves,
				(x + 1, y + 1) in self.elves,
			))
			self.should_move_north[(x, y)] = not any((
				(x - 1, y - 1) in self.elves,
				(x    , y - 1) in self.elves,
				(x + 1, y - 1) in self.elves,
			))
			self.should_move_south[(x, y)] = not any((
				(x - 1, y + 1) in self.elves,
				(x    , y + 1) in self.elves,
				(x + 1, y + 1) in self.elves,
			))
			self.should_move_west[(x, y)] = not any((
				(x - 1, y - 1) in self.elves,
				(x - 1, y    ) in self.elves,
				(x - 1, y + 1) in self.elves,
			))
			self.should_move_east[(x, y)] = not any((
				(x + 1, y - 1) in self.elves,
				(x + 1, y    ) in self.elves,
				(x + 1, y + 1) in self.elves,
			))

	def update(self, remove: Set[Coordinate], add: Set[Coordinate]):
		self.elves.difference_update(remove)
		self.elves.update(add)

		for (x, y) in self.elves:
			self.has_neighbours[(x, y)] = any((
				(x - 1, y - 1) in self.elves,
				(x    , y - 1) in self.elves,
				(x + 1, y - 1) in self.elves,
				(x - 1, y    ) in self.elves,
				(x + 1, y    ) in self.elves,
				(x - 1, y + 1) in self.elves,
				(x    , y + 1) in self.elves,
				(x + 1, y + 1) in self.elves,
			))
			self.should_move_north[(x, y)] = not any((
				(x - 1, y - 1) in self.elves,
				(x    , y - 1) in self.elves,
				(x + 1, y - 1) in self.elves,
			))
			self.should_move_south[(x, y)] = not any((
				(x - 1, y + 1) in self.elves,
				(x    , y + 1) in self.elves,
				(x + 1, y + 1) in self.elves,
			))
			self.should_move_west[(x, y)] = not any((
				(x - 1, y - 1) in self.elves,
				(x - 1, y    ) in self.elves,
				(x - 1, y + 1) in self.elves,
			))
			self.should_move_east[(x, y)] = not any((
				(x + 1, y - 1) in self.elves,
				(x + 1, y    ) in self.elves,
				(x + 1, y + 1) in self.elves,
			))

def p2(args):
	soil_map = SoilMap(set(read_file(args.file)))
	proposing_order: List[Tuple[Dict[Coordinate, bool], int, int]] = [
		(soil_map.should_move_north,  0, -1),
		(soil_map.should_move_south,  0, +1),
		(soil_map.should_move_west , -1,  0),
		(soil_map.should_move_east , +1,  0),
	]

	# print_elves(soil_map.elves, 'Initial State')

	for round in count():
		if round % 10 == 0: print(round)

		round_proposing_order = [proposing_order[(round + i) % 4] for i in range(4)]
		elves_proposed_destinations: Dict[Coordinate, Coordinate] = {}
		requested_destinations = defaultdict(lambda: 0)

		for (x, y) in soil_map.elves:
			if not soil_map.has_neighbours[(x, y)]: continue

			for should_move, dx, dy in round_proposing_order:
				if should_move[(x, y)]:
					new_location = (x + dx, y + dy)
					requested_destinations[new_location] += 1
					elves_proposed_destinations[(x, y)] = new_location
					break
			else: continue

		new_destinations = set(destination for destination, num_times_requested in requested_destinations.items() if num_times_requested == 1)
		moving_elves = set(elve for elve, destination in elves_proposed_destinations.items() if destination in new_destinations)

		if len(new_destinations) == 0:
			print(round + 1)
			return

		soil_map.update(moving_elves, new_destinations)
		# print_elves(soil_map.elves, f'End of Round {round + 1}')


if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str, default='input.txt')
	parser.add_argument('-v', '--verbose', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}, default='WARNING')
	args = parser.parse_args()

	logging.basicConfig(level=args.verbose)

	p1(args)
	p2(args)
